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

        # self.shipSquares is a set of integers representing 
        # the locations of placed ships 
        self.shipSquares : set[int] = set() 
        self.shipRows : set[int] = set() 
        self.shipCols : set[int] = set() 

        # self.hits and self.misses are sets of integers 
        # representing the locations of previous hits and misses 
        # by both this player and the enemy 
        self.launchedHits : set[int] = set() 
        self.launchedMisses : set[int] = set() 

        self.takenHits : set[int] = set() 
        self.takenMisses : set[int] = set() 

    def configure(self):
        self.conn.send('id {}'.format(self.name))  # self identify
        self.conn.send('autodump')  # turn on dumping the board after every move

    def place_ships(self): 

        """
        Place ships in their location. 

        Place each ship at a random (row, col) location, 
        ensuring that no ships overlap. 

        When the enemy hits a ship, they are likely to target 
        adjacent squares to find the endpoints of 
        the hit ship. 

        Ships are placed in non adjacent rows so that 
        the likelihood of the enemy hitting a new ship 
        after finding a first ship in an adjcanet row is reduced. 
        """ 

        ships = map(operator.itemgetter(0), sorted(SHIPS.items(), key=operator.itemgetter(1), reverse=True))
        for row, ship in enumerate(ships, start=1): 

            print(f"(row, ship) = ({row}, {ship}") 

            # Get valid non adjacent row 
            row = 0 
            rowNonAdjacent = False 

            while (not rowNonAdjacent): 

                rowNonAdjacent = True 

                row = random.randint(0, len(ROWS) - 1) 

                if (self.shipRows.__contains__(row)): 

                    rowNonAdjacent = False 

                # Get valid topRow 
                topRow = row - 1 

                if (topRow >= 0 \
                    and self.shipRows.__contains__(topRow)): 

                    rowNonAdjacent = False 
                
                # Get valid bottomRow 
                bottomRow = row + 1 
                if (bottomRow  < len(ROWS) \
                    and self.shipRows.__contains__(bottomRow)): 

                    rowNonAdjacent = False 
            
            self.shipRows.add(row) 

            # Get ship length 
            shipLength = SHIPS[ship] 
            print(f"shipLength = {shipLength}") 

            # Ensure ship endpoint is not out of bounds 
            shipLeftmostCol = shipLength - 1 

            shipRightmostCol = len(COLS) - shipLength 

            # Get random col 
            col = random.randint(shipLeftmostCol, shipRightmostCol) 

            self.shipCols.add(col) 
            
            # Update placed ship squares 
            self.shipSquares.add(self.getIndex(row, col)) 

            self.conn.send('place {} {}{} horizontal'
            .format(ship, COLS[col], ROWS[row])) 
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
        self.handle_player_result(self.conn.get_line(), row, col) 

    def await_partner_turn(self):
        """
        Await our partner's turn.
        """
        self.handle_partner_result(self.conn.get_line(), row = 0, col = 0) 

    def getCheckerboardBlack(self, row, col): 

        """Returns true if (row, col) is a black sqaure on a 
        checkerboard, where a checkerboard is 
        B W B W ... 
        W B W B ... 
        ... 
        
        Since ships occupy at least 2 adjacent squares, 
        only non adjacent squares need to be searched until a 
        successful hit, indicating an enemy ship is found """ 

        return ((row + col) % 2 == 0) 
    
    def getIndex(self, row, col): 

        """Returns an index representing a (row, col) location 
        given a square board of size len(COLS) """ 

        return row * len(COLS) + col 

    def handle_player_result(self, result, row, col): 

        """
        Handle the result of our turn.

        :type result: str
        """ 

        launchedIndex = self.getIndex(row, col) 
        print(f"launchedIndex = {launchedIndex}") 

        if result.startswith('hit'): 

            # Update launchedHits 
            self.launchedHits.add(launchedIndex) 
            print(f"launchedHits = {self.launchedHits} ") 

            print('Yay!') 

        elif result.startswith('miss'): 

            # Update launchedMisses 
            self.launchedMisses.add(launchedIndex) 
            print(f"launchedMisses = {self.launchedMisses} ") 

            print('Boo') 

        elif result.startswith('sunk'): 

            # Update launchedHits as a ship was sunk 
            self.launchedHits.add(launchedIndex) 
            print(f"launchedHits = {self.launchedHits}") 

            print('HA! I sunk your {}'.format(get_ship_name(result[-2]))) 

        elif result.startswith('won'): 

            # Update launchedHits as all ships were sunk 
            self.launchedHits.add(launchedIndex) 
            print(f"launchedHits = {self.launchedHits}") 

            print('HA! I sunk your {}'.format(get_ship_name(result[-2])))
            print('HOORAY!!!')
            self.game_over = True 

        else:
            print('Unknown result: {}'.format(result))

    def handle_partner_result(self, result, row, col): 

        """
        Handle the result of our partner's turn.

        :type result: str
        """ 

        takenIndex = self.getIndex(row, col) 

        if result.startswith('partner hit'): 

            # Update takenHits 
            self.takenHits.add(takenIndex) 
            print(f"takenHits = {self.takenHits}") 

            print('Darn') 

        elif result.startswith('partner miss'): 

            # Update takenMisses 
            self.takenMisses.add(takenIndex) 
            print(f"takenMisses = {self.takenMisses}") 

            print('Nah nah nay') 

        elif result.startswith('partner sunk'): 

            # Update takenHits as a ship was sunk 
            self.takenHits.add(takenIndex) 
            print(f"takenHits = {self.takenHits}") 

            print('AH! You sunk my {}'.format(get_ship_name(result[-2]))) 

        elif result.startswith('partner won'): 

            # Update takenHits as all ships were sunk 
            self.takenHits.add(takenIndex) 
            print(f"takenHits = {self.takenHits}") 

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
    name = 'Manish Khilari' # set this to your name 

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
