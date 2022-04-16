#!/usr/bin/env python3
##############################################################################
# Akuna Capital Python Battleships Server
#
# Pair up clients as they connect and let them play.  The protocol is a text
# based protocol that can be run via telnet.  For help, telnet to the server
# (port 50008) and type "help"
##############################################################################
import copy
import multiprocessing
import select
import socket
import threading
import traceback

# List of ships
SHIPS = {
    'a': 5,  # aircraft carrier
    'b': 4,  # battleship
    's': 3,  # submarine
    'c': 3,  # cruiser
    'd': 2,  # destroyer
}
NICE = 'abcdefghij'  # used to translate column numbers to characters
HOST = ''  # Symbolic name meaning the local host
PORT = 50008  # Arbitrary non-privileged port


##############################################################################
# Game class.  Most functions called by the thread class return a pair of
# results.  The first one is sent to the user, the second one is sent to
# our partner thread.  Either one can be None.
#
# doc strings are sent in response to the help command
#
# We throw exceptions like crazy when things don't work and expect our caller
# to do the right thing
##############################################################################
class Game:
    """
    Battle Room Server

    Pair up connections to this server and play battleships. The protocol for
    interacting with the server is lines of text separated by carriage returns.
    Any line starting with a space (to or from the server) is ignored.

    Lines are space-separated words.  Generic responses from the server are:
    - "ok ..." which is the word ok, followed by some descriptive text.
    - "error ..." which is the word error, followed by some descriptive text.

    Each command (described below) can have its own additional responses.

    The battleships board is a 10x10 board, that can be addressed using two
    character strings of the form xn, where x is a character from "a"-"j", and
    n is a digit 0-9.  For example, a0, c9, j2.

    The ships in battleships are as follows:
    - aircraftcarrier: 5 long
    - battleship:      4 long
    - submarine:       3 long
    - cruiser:         3 long
    - destroyer:       2 long

    When sending ship names to the server, only the first character is used and
    the remainder of the ship name is ignored.

    Finally, when it is time for your FIRST move, the server will send "go".
    After that, the expectation is that users will take turns shooting.
    """

    ##############################################################################
    # Game class constructor...just takes a color, which should be "white" or
    # something other that white for each pair
    ##############################################################################
    def __init__(self, color):
        self.active_ships = set()
        self.my_move = color == 'white'
        self.color = color
        self.other_ready = False
        self.ready = False
        self.id = 'UNKNOWN'
        self.auto_dump = False
        self.shots = 0

        self.my_board = []
        for r in range(10):
            row = []
            for c in range(10):
                row.append('.')
            self.my_board.append(row)

        self.their_board = copy.deepcopy(self.my_board)

    # clever debug printer that includes your color
    def my_print(self, *args):
        print(self.color, *args)

    # sees whether a ship still exists on our board. Used to determine
    # "sunk"
    def find(self, ship):
        try:
            [item for sublist in self.my_board for item in sublist].index(ship)
            return True
        except ValueError:
            return False

    # turns a col/row like "00" into character based like "a0"
    @staticmethod
    def nice_row_col(row_col):
        if row_col[0] in '0123456789':
            row_col[0] = NICE[ord(row_col[0])]
        return row_col

    # turns a col/row like "00" into character based like "a0"
    def parse_col_row(self, col_row):
        try:
            if len(col_row) != 2:
                raise Exception("Invalid location")

            col = col_row[0]
            row = col_row[1]

            row = int(row)
            if row < 0 or row > 9:
                raise Exception('Invalid row %s' % row)

            if col in NICE:
                col = ord(col) - ord('a')
            else:
                col = int(col)

            if col < 0 or col > 9:
                raise Exception('Invalid col %s' % col)

            return row, col
        except Exception as ex:
            self.my_print("parse_col_row error " + str(ex))
            self.my_print("======================")
            traceback.print_tb(ex.__traceback__)
            self.my_print("======================")
            raise Exception("Invalid location %s" % col_row)

    # place a ship
    def user_place(self, data):
        """
        Place a ship on the board.  the syntax is:
        - place [ship] [location] [horizontal/vertical]

        for example "place battleship a2 horizontal"
        (this can be shortened to "place b a2 h")

        On success, this command returns "ok".

        The server will not accept moves until all ships have
        been successfully placed.  Once all ships have been placed,
        by both players, the server will additionally return "go"
        to the player whose turn it is.
        """
        ship, col_row, direction = [x.strip() for x in data.split(' ')]

        if self.ready:
            raise Exception("Ships already placed")

        ship = ship[0]
        if ship not in SHIPS:
            raise Exception('Invalid ship %s' % ship)

        row, col = self.parse_col_row(col_row)

        direction = direction[0]
        if direction not in "hv":
            raise Exception('Invalid direction %s' % direction)

        if ship in self.active_ships:
            raise Exception("Ship %s already placed" % ship)

        # we work on a copy of the board, in case something goes wrong
        new_board = copy.deepcopy(self.my_board)

        for x in range(SHIPS[ship]):
            if row > 9 or col > 9:
                raise Exception("Ship fell off the board")

            if new_board[row][col] != '.':
                raise Exception("Ship fell off the board")

            new_board[row][col] = ship

            if direction == 'h':
                col += 1
            else:
                row += 1

        self.my_board = new_board
        self.active_ships.add(ship)

        ret = "ok %s at %s (%d %d) %s" % (ship, self.nice_row_col(col_row), row, col, direction)

        if not len(self.active_ships) == 5:
            return ret, None

        self.ready = True

        if self.other_ready:
            if self.my_move:
                ret += "\ngo"
            else:
                ret += "\n  other player's move"
        else:
            ret += "\n  waiting for other player"

        return ret, "ready"

    # Set the user's name
    def user_id(self, line):
        """
        Provide and ID used to record results
        - id [id]

        for example "id Mickey Mouse"
        """
        if line != '':
            self.id = line
        self.my_print("Got id %s" % self.id)

        return " Welcome %s" % self.id, None

    # turn on auto_dumping
    # noinspection PyUnusedLocal
    def user_autodump(self, line):
        """
        Automatically dump the board after each move.  This is
        intended for interactive use

        for example "autodump"
        """
        self.auto_dump = True

        return " autodump on", None

    # shot by the user
    def user_shoot(self, line):
        """
        Shoot at a square.
        - id [location]

        for example "shoot a1"

        This will return one of:
        - hit
        - miss
        - sunk
        - won
        """
        if not self.my_move:
            raise Exception("Not our move")

        if not (self.ready and self.other_ready):
            raise Exception("Board not ready")

        _, _ = self.parse_col_row(line)

        self.my_move = False
        self.shots += 1

        return None, 'shoot ' + line

    # dump the board
    def user_dump(self, _):
        """
        Display the current board, both your board and your view of the
        opponent's board.  Each line begins with a space, and thus should
        be ignored by any client software
        """
        ret = ''

        ret += '     a b c d e f g h i j  | a b c d e f g h i j\n'
        ret += '     ===================  | ===================\n'

        for x in range(10):
            ret += "  %d |" % x
            for y in range(10):
                ret += self.my_board[x][y] + " "

            ret += " | "

            for y in range(10):
                ret += self.their_board[x][y] + " "

            ret += '\n'

        return ret, None

    # return help. Return the class's docstring, and then introspect for all
    # methods starting "user_" that have docstrings and return those
    def user_help(self, _):
        ret = ''
        ret += self.__doc__
        for a in dir(self):
            if a.startswith('user_') and hasattr(getattr(self, a), '__doc__') and getattr(self, a).__doc__:
                ret += '   ' + a[5:] + '\n'
                ret += getattr(self, a).__doc__ + '\n'
        return ret, None

    # other thread is alive
    # noinspection PyUnusedLocal
    def partner_ready(self, line):
        if self.other_ready:
            self.my_print("Got multiple ready messages from our partner (%s)", str(self.other_ready))
            return None, None

        self.other_ready = True

        if self.my_move and self.ready:
            return "go partner ready", None
        else:
            return None, None

    # other thread shot...tell them what happened
    def partner_shoot(self, line):
        if self.my_move:
            raise Exception("Not the your move")

        row, col = self.parse_col_row(line)

        contents = self.my_board[row][col]

        self.my_move = True

        if contents == '.':
            result = 'miss %s%d' % (NICE[col], row)
            self.my_board[row][col] = '*'
        elif contents == '*' or contents == 'X':
            result = 'miss %s%d' % (NICE[col], row)
        else:
            self.my_board[row][col] = 'X'

            # see if there is any of this ship left
            if self.find(contents):
                result = 'hit %s%d' % (NICE[col], row)
            else:
                self.active_ships.remove(contents)

                result = 'sunk %s%d %s' % (NICE[col], row, contents)

                if len(self.active_ships) == 0:
                    result = 'won ' + result
                    self.my_move = False

        # if this is the first shot from our partner, it is now
        # our firs turn
        user_result = 'partner ' + result
        if self.shots == 0:
            user_result += '\ngo'

        return user_result, result

    # other thread won
    @staticmethod
    def partner_won(line):
        return "won " + line, None

    # store the result in our board
    def store_result(self, row_col, result):
        row, col = self.parse_col_row(row_col[:2])
        self.their_board[row][col] = result

    # partner said we hit
    def partner_hit(self, line):
        self.store_result(line, 'X')

        return "hit " + line, None

    # partner said we sunk
    def partner_sunk(self, line):
        self.store_result(line, 'X')

        return "sunk " + line, None

    # partner said we missed
    def partner_miss(self, line):
        self.store_result(line, '*')

        return "miss " + line, None

    # handle a command by introspecting.  prefix can
    # be "partner" or "user" depending on where the
    # command came from
    def handle_command(self, prefix, line):
        if line[0] == ' ':
            return None, None

        command = line.split(' ', 1)[0].strip()

        if line.find(' ') >= 0:
            rest = line.split(' ', 1)[1].strip()
        else:
            rest = ''

        full_command = prefix + '_' + command

        if not hasattr(self, full_command):
            raise Exception("error unknown command %s" % command)

        u, p = getattr(self, full_command)(rest)

        if u and self.auto_dump and not command == 'dump':
            d, _ = self.user_dump('')
            u += '\n' + d

        return u, p

    # handle a command from our user
    def handle_user(self, line):
        return self.handle_command('user', line)

    # handle a command from our partner thread
    def handle_partner(self, line):
        self.my_print("partner receive: %s" % (str(line)))
        return self.handle_command('partner', line)


# thread representing a single user.  It talks to
# its user via the socket s, and its partner via
# the pipe P
class IOThread(threading.Thread):
    # Take the pipe, socket, and color
    def __init__(self, p, s, color):
        threading.Thread.__init__(self)
        self.p = p
        self.s = s
        self.buf = ''
        self.game = Game(color)

    # read a line from the socket.  There are classes to do
    # this, but it is just open coded here to reduce dependencies.
    # read from the socket until a \n is received and return the
    # result WITHOUT the \n.  Return None if a full line has not been received
    # and throw an I/O error if
    # noinspection SpellCheckingInspection
    def readline(self):
        if self.buf.find('\n') < 0:
            # First, get some input and bail if the other end closed
            data = self.s.recv(256)
            if len(data) == 0:
                self.p.close()
                self.game.my_print("user closed")
                raise Exception("User closed!")

            # append the input to our buffer
            self.buf += data.decode()

        # now see if we can get a full line from it
        parts = self.buf.split('\n', 1)

        # Didn't get a full line, return nothing
        if len(parts) == 1:
            return None

        # yay! got a full line, put the remainder back in our buffer and
        # return the line
        if len(parts) == 2:
            self.buf = parts[1]
            return parts[0].lower()

        # we shouldn't actually get here
        self.game.my_print("WIERD...split returned something wrong")

    # send a string on the socket.  We append a \n and encode it
    def s_send(self, s):
        if s is None:
            return
        s += '\n'
        self.s.send(s.encode())

    # send a string on the pipe
    def p_send(self, s):
        if s is None:
            return
        self.p.send(s)

    # process input from the socket
    def process_socket(self):
        line = self.readline()
        if line is None:
            return

        try:
            self.game.my_print("socket got: ", line)
            user_out, partner_out = self.game.handle_user(line)
            self.s_send(user_out)
            self.p_send(partner_out)
        except Exception as ex:
            self.game.my_print("error " + str(ex))
            self.game.my_print("======================")
            traceback.print_tb(ex.__traceback__)
            self.game.my_print("======================")
            self.s_send("error " + str(ex))

    # process input from the pipe
    def process_pipe(self):
        if self.p.closed:
            self.game.my_print("partner closed")
            self.s_send("error partner closed")
            self.s.close()
            raise Exception("Partner closed!")

        try:
            data = self.p.recv()
        except EOFError:
            self.game.my_print("partner closed")
            self.s_send("error partner closed")
            self.s.close()
            raise Exception("Partner closed!")

        try:
            user_out, partner_out = self.game.handle_partner(data)
            self.s_send(user_out)
            self.p_send(partner_out)
        except Exception as ex:
            self.game.my_print("error " + str(ex))
            self.game.my_print("======================")
            traceback.print_tb(ex.__traceback__)
            self.game.my_print("======================")
            self.s_send("error internal partner exception " + str(ex))

    # main thread
    def run(self):
        try:
            self.game.my_print("running battleground thread")

            while True:
                if len(self.buf):
                    input_ready = [self.s]
                else:
                    input_ready, _, _ = select.select([self.p, self.s], [], [])

                for f in input_ready:
                    if f == self.p:
                        self.process_pipe()
                    elif f == self.s:
                        self.process_socket()
                    else:
                        self.game.my_print("WEIRD..unknown socket on select!!!")
        except Exception as ex:
            self.game.my_print("Ending")
            self.game.my_print("error " + str(ex))
            self.game.my_print("======================")
            traceback.print_tb(ex.__traceback__)
            self.game.my_print("======================")


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    pipes = list(multiprocessing.Pipe())

    while True:
        conn, addr = s.accept()
        print('Connected by', addr)

        p = pipes.pop()

        if len(pipes) == 1:
            print("got first partner")
            color = 'white'
        else:
            print("got second partner")
            color = 'red'
            pipes = list(multiprocessing.Pipe())

        t = IOThread(p, conn, color)
        t.daemon = True
        t.start()


if __name__ == '__main__':
    main()
