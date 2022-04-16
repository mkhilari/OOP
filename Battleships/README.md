battleships
===========

Battleships game.
Contains both the battle server as well
as clients for various languages

Setup
=====

Run the server with "./server/battleroom.py" from the battleships directory.

Make the c++ client with 'make' in the 'c++' directory

Run the binary with './battleships localhost'

The server requires two players, so
Open a new terminal and run the binary again

Once both client binaries have connected to the server and placed their
ships, the server will give the clients a 'go' signal and the two clients
will play against each other with 'random' shooting. The board state after
each move will be displayed in the terminal output.

Once the game is over, the server will output 'Ending' for the
white and red players.
(There will also be an exception traceback. You can ignore this.)

To play again, just run two instances of the binaries again.

Copyright Akuna Capital LLC 2017