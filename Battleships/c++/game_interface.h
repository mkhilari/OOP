#include <iostream>
#include <string>
#include "boost/asio/ip/tcp.hpp"

enum status{
	hit,
	miss,
	sunk,
	won,
	unknown
};

using tcp_stream = boost::asio::ip::tcp::iostream;
using response = std::pair<status, int>;

class game_interface
{
public:

	game_interface(int argc, char **argv, const std::string &name){
		// Make sure we got a hostname on the command line
		if (argc != 2) {
		    std::cerr << "Provide server host name as an argument" << std::endl;
		    exit(-1);
		}

		// Connect to the server
		stream.connect(argv[1], "50008");
		if (!stream) {
		    std::cerr << "Can't connect" << std::endl;
            exit(-1);
		}

		// Tell the other side who we are and turn on automatically dumping the board
		stream << "id " << name << std::endl;
		stream << "autodump" << std::endl;
		stream.flush();
	}
	~game_interface(){};

	void place_a_ship(const std::string &ship_name, const char &col, int row, const std::string &direction);
	response shoot(char col, int row);

	void wait_for_go();
	response wait_for_partner();

private:

	tcp_stream stream;

	response decode_response(std::string &response_string) const;
};