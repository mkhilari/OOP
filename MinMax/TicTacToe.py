


from pyrsistent import b


class Player: 

    NONE = 0 
    A = 1 
    B = -1 

    symbol = {0 : " ", 1 : "X", -1 : "O"} 

class GameState: 

    BOARD_LENGTH = 3 

    def __init__(self, player, board): 

        self.player = player 
        
        self.board = board 
    
        self.nexts = [] 
        
        if (self.getWinner() == Player.NONE): 

            self.nexts = self.getNexts() 
    
    def getNexts(self): 

        """Returns next game states given a player """ 

        print(self) 
        
        nexts = [] 

        newBoard = [[self.board[row][col] 
        for col in range(GameState.BOARD_LENGTH)] 
        for row in range(GameState.BOARD_LENGTH)] 

        for row in range(GameState.BOARD_LENGTH): 

            for col in range(GameState.BOARD_LENGTH): 

                if (newBoard[row][col] != Player.NONE): 
                    
                    # (row, col) already taken 
                    continue 
                
                # Create new game state 
                newBoard[row][col] = self.player 

                # New game state is the other player's move 
                newGameState = GameState(player = -self.player, 
                board = newBoard) 

                nexts.append(newGameState) 
        
        return nexts 
    
    def getWinner(self): 

        """Returns the winning player if the game is won """
        
        for player in [Player.A, Player.B]: 

            if (self.playerWin(player)): 

                return player 
        
        return Player.NONE 

    def playerWin(self, player): 

        """Returns true if the given plaer has won """ 

        # Check rows 
        for row in range(GameState.BOARD_LENGTH): 

            for col in range(GameState.BOARD_LENGTH): 

                if (self.board[row][col] != player): 

                    break 

                if (col == GameState.BOARD_LENGTH - 1): 

                    return True 
        
        # Check cols 
        for col in range(GameState.BOARD_LENGTH): 

            for row in range(GameState.BOARD_LENGTH): 

                if (self.board[row][col] != player): 

                    break 

                if (row == GameState.BOARD_LENGTH - 1): 

                    return True 
        
        # Check \ diagonal 
        for i in range(GameState.BOARD_LENGTH): 

            if (self.board[i][i] != player): 

                break 
                
            if (i == GameState.BOARD_LENGTH - 1): 

                return True 
        
        # Check / diagonal 
        for i in range(GameState.BOARD_LENGTH): 

            if (self.board[GameState.BOARD_LENGTH - 1 - i]
            [i] != player): 

                break 
                
            if (i == GameState.BOARD_LENGTH - 1): 

                return True 
        
        return False 

    def __str__(self): 

        s = "" 
        
        for row in range(GameState.BOARD_LENGTH): 

            line = "" 

            for col in range(GameState.BOARD_LENGTH): 

                line += Player.symbol[self.board[row][col]] 

            s += f"{line}\n" 

        return s 

def main(): 

    initialBoard = [[Player.NONE 
    for col in range(GameState.BOARD_LENGTH)] 
    for row in range(GameState.BOARD_LENGTH)] 

    initialGameState = GameState(player = Player.A, 
    board = initialBoard) 

main() 