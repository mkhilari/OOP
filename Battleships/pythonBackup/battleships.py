#!/usr/bin/env python3
import operator
import random
import socket
import sys

SHIPS = {
    'aircraftcarrier': 5,
    'battleship': 4,
    'submarine': 3,
    'cruiser': 3,
    'destroyer': 2,
}
COLS = tuple('abcdefghij')
ROWS = tuple('0123456789')


def get_ship_name(identifier):
    """
    :type identifier: str
    :rtype: str
    """
    for ship_name in SHIPS:
        if ship_name.startswith(identifier):
            return ship_name
    return 'unknown'


class Connection:
    def __init__(self, host, port=50008):
        """
        :type host: str
        :type port: int
        """
        print('Connecting to {}:{}.'.format(host, port))
        self.conn = socket.create_connection((host, port))
        self.in_stream = self.conn.makefile('r')
        self.out_stream = self.conn.makefile('w')

    def send(self, msg):
        """
        Utility function to send to the output file and flush.

        :type msg: str
        """
        print('> {}'.format(msg))  # log the message before it is sent
        print(msg, file=self.out_stream)
        self.out_stream.flush()

    def get_line(self):
        """
        Wait for a response, ignoring lines starting with a space.

        :rtype: str
        """
        while True:
            line = self.in_stream.readline()
            print('< {}'.format(line), end='')
            if not line:
                return None
            first_char = line[0]
            if first_char != ' ' and first_char != '\n':
                return line

    def close(self):
        """
        Close the connection.
        """
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class BattleshipClient:
    def __init__(self, conn, name):
        """
        :type conn: Connection
        :type name: str
        """
        self.conn = conn
        self.name = name
        self.game_over = False

    def configure(self):
        self.conn.send('id {}'.format(self.name))  # self identify
        self.conn.send('autodump')  # turn on dumping the board after every move

    def place_ships(self):
        """
        Place ships in their location.
        """
        col = 'a'
        ships = map(operator.itemgetter(0), sorted(SHIPS.items(), key=operator.itemgetter(1), reverse=True))
        for row, ship in enumerate(ships, start=1):
            self.conn.send('place {} {}{} horizontal'.format(ship, col, row))
            self.conn.get_line()

    def wait_for_go(self):
        """
        Await our first turn by waiting until go.
        """
        while True:
            if self.conn.get_line().startswith('go'):
                break

    def shoot(self):
        """
        Take our turn.
        """
        col = random.choice(COLS)
        row = random.choice(ROWS)
        self.conn.send('shoot {}{}'.format(col, row))
        self.handle_player_result(self.conn.get_line())

    def await_partner_turn(self):
        """
        Await our partner's turn.
        """
        self.handle_partner_result(self.conn.get_line())

    def handle_player_result(self, result):
        """
        Handle the result of our turn.

        :type result: str
        """
        if result.startswith('hit'):
            print('Yay!')
        elif result.startswith('miss'):
            print('Boo')
        elif result.startswith('sunk'):
            print('HA! I sunk your {}'.format(get_ship_name(result[-2])))
        elif result.startswith('won'):
            print('HA! I sunk your {}'.format(get_ship_name(result[-2])))
            print('HOORAY!!!')
            self.game_over = True
        else:
            print('Unknown result: {}'.format(result))

    def handle_partner_result(self, result):
        """
        Handle the result of our partner's turn.

        :type result: str
        """
        if result.startswith('partner hit'):
            print('Darn')
        elif result.startswith('partner miss'):
            print('Nah nah nay')
        elif result.startswith('partner sunk'):
            print('AH! You sunk my {}'.format(get_ship_name(result[-2])))
        elif result.startswith('partner won'):
            print('AH! You sunk my {}'.format(get_ship_name(result[-2])))
            print('drats')
            self.game_over = True
        else:
            print('Unknown partner result: {}'.format(result))


def main():
    if len(sys.argv) != 2:
        print('Provide server host as the only argument')
        return

    host = sys.argv[1]
    name = 'Mickey Mouse'  # set this to your name
    with Connection(host) as conn:
        client = BattleshipClient(conn, name)
        client.configure()
        client.place_ships()
        client.wait_for_go()
        while True:
            client.shoot()
            if client.game_over:
                break
            client.await_partner_turn()
            if client.game_over:
                break


if __name__ == '__main__':
    main()
