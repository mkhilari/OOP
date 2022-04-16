#include "game_interface.h"

void game_interface::place_a_ship(const std::string &ship_name, const char &col, int row, const std::string &direction){
    stream << "place " << ship_name << " " << col << row << " " << direction << std::endl;
}

response game_interface::shoot(char col, int row){
	stream << "shoot " << col << row << std::endl;
	std::cout << "shoot " << col << row << std::endl;
	stream.flush();

	std::string input;
	while (getline(stream, input, '\n')) {
	    std::cout << "> " << input << std::endl;
	    if ((input.length() > 0) && (input[0] != ' '))
	        break;
	}
	return decode_response(input);
}

void game_interface::wait_for_go(){
	std::string input;
	while (getline(stream, input, '\n')) {
	    std::cout << "> " << input << std::endl;
	    if (input.find("go") != std::string::npos)
	        return;
	}
    exit(-1);
}

response game_interface::wait_for_partner(){
	std::string input;
	while (getline(stream, input, '\n')) {
	    std::cout << "> " << input << std::endl;
	    if ((input.length() > 0) && (input[0] != ' '))
	        break;
	}
	return decode_response(input);
}

response game_interface::decode_response(std::string &resp_string) const {
	if      (resp_string.find("hit") != std::string::npos){
		return response(hit, -1);
	}
	else if (resp_string.find("miss") != std::string::npos){
		return response(miss, -1);
	}
 	else if (resp_string.find("won") != std::string::npos){
 		return response(won, -1);
 	}
	else if (resp_string.find("sunk") != std::string::npos){
		std::cout << resp_string.length() << std::endl;
		const char ship_sunk = resp_string[resp_string.length()-1];
		switch(ship_sunk){
			case 'a': //aircraftcarrier
				return response(sunk, 0);
			case 'b': //battleship
				return response(sunk, 1);
			case 'c': //cruiser
				return response(sunk, 2);
			case 's': //submarine
				return response(sunk, 3);
			case 'd': //destroyer
				return response(sunk, 4);
			default:
				std::cout << "Unknown ship type sunk : " << ship_sunk << std::endl;
				return response(sunk, -1);
		}

	}
	else{
		return response(unknown, -1);
	}
}