//////////////////////////////////////////////////////////////////////////////
// Akuna Capital C++ Battleships Client
//
// Connect to the battleship server, place our ships, and then shoot randomly
// until someone wins
//
// You can telnet to the battleship server and type "help" for more details
// on the protocol
//////////////////////////////////////////////////////////////////////////////
#include <random>
#include "game_interface.h"

// The ship struct contains the ship name and length
struct ship {
    const std::string name_;
    const size_t length_;

    ship(const std::string &name, size_t length):
    name_(name),
    length_(length)
    {}
};

// This is a vector of all of the available ships in the game
const std::vector<ship> ships {
                            {"aircraftcarrier", 5},
                            {"battleship", 4},
                            {"cruiser", 3},
                            {"submarine", 3},
                            {"destroyer", 2}
                        };

// This a vector with the directions you can place your ships on the board
// horizontal - places the rest of the ship to the right of the specified location
// vertical - places the rest of the ship below the specified location
const std::vector<std::string> directions {"horizontal", "vertical"};

// These are the column names from the standard battleship board.
const char cols[10] = {'a','b','c','d','e','f','g','h','i','j'};

// This is a global random number generator, and a uniform distribution
std::default_random_engine generator;
std::uniform_int_distribution<int> distribution(0,9);



////////////////////////////////////////////////////////////////////////////////
// Your code for placing ships goes in here
////////////////////////////////////////////////////////////////////////////////
void place_ships(game_interface &game){

    // This example places ships one below the other at the left side of the board
    // You may want to place your ships more intelligently, but make sure you
    // don't place them off of the board!
    int r = 0;
    for (const auto &ship : ships) {
        game.place_a_ship(ship.name_, cols[0]/*a*/, r, directions[0]/*horizontal*/);
        r++;
    }

}

////////////////////////////////////////////////////////////////////////////////
// Your code for taking a shot goes in here
////////////////////////////////////////////////////////////////////////////////
bool take_shot(game_interface &game){

    // This example picks a random shot location. You may want to shoot more intelligently
    int col = distribution(generator);
    int row = distribution(generator);

    // The response code is a std::pair<status, int>, where the status indicates the result
    // of the shot, and the int indicates the index of the ship in the ships vector
    // that was sunk if a ship was sunk.
    const response resp = game.shoot(cols[col], row);

    // This handles the response code for your shot and outputs messages to the terminal.
    // You may want to do a bit more than this.
    switch(resp.first){
        case hit:
            std::cout << "Yay!" << std::endl;
            break;
        case miss:
            std::cout << "Boo" << std::endl;
            break;
        case sunk:
            std::cout << "HA! I sunk your " << ships[resp.second].name_ << std::endl;
            break;
        case won:
            std::cout << "HOORAY!!!" << std::endl;
            return true;
            break;
        default:
            std::cout << "!!!!! Unknown input !!!!!" << std::endl;
    }
    return false;
}

////////////////////////////////////////////////////////////////////////////////
// Your code for handling your partners move goes in here
////////////////////////////////////////////////////////////////////////////////
bool handle_partner_move(const response &resp){
    // The response code is a std::pair<status, int>, where the status indicates the result
    // of the shot, and the int indicates the index of the ship in the ships vector
    // that was sunk if a ship was sunk.

    // This handles the response code from your partner's shot and outputs messages to the terminal.
    // You may want to do a bit more than this.
    switch(resp.first){
        case hit:
            std::cout << "Darn" << std::endl;
            break;
        case miss:
            std::cout << "Nah nah nay" << std::endl;
            break;
        case sunk:
            std::cout << "AH! You sunk my " << ships[resp.second].name_ << std::endl;
            break;
        case won:
            std::cout << "drats" << std::endl;
            return true;
            break;
        default:
            std::cout << "!!!!! Unknown partner input !!!!!" << std::endl;
    }
    return false;
}


////////////////////////////////////////////////////////////////////////////////
// This is the main game event loop.
// You don't need to modify anything in here.
////////////////////////////////////////////////////////////////////////////////
int main(int argc, char **argv) {

    // Create our game object and give it a name
    game_interface game{argc, argv, "Donald Duck"};

    // Place our ships
    place_ships(game);

    // Wait for the "go" message from the server
    game.wait_for_go();

    // Loop until someone wins!
    bool game_over = false;
    while (!game_over) {
        // Take a shot
        game_over = take_shot(game);
        if(game_over) break;

        // Wait for our partner's move, and handle the response
        game_over = handle_partner_move(game.wait_for_partner());
    }

    return 0;
}
