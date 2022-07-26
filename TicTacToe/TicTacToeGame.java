

public class TicTacToeGame {

    public static char BLANK_TILE = ' ';
    public static char PLAYER_1_TILE = 'X';
    public static char PLAYER_2_TILE = 'O';

    private int[][] board;
    private int numTurnsFinished = 0;

    public TicTacToeGame(int boardSize) {

        this.board = new int[boardSize][boardSize];

        this.generateMoves();
    }

    public int[][] getBoard() {

        return this.board;
    }

    public int getBoardSize() {

        return this.getBoard().length;
    }

    public static char getPlayer(int n) {

        return (n % 2 == 0 ? PLAYER_1_TILE : PLAYER_2_TILE);
    }

    public char getCurrentPlayer() {

        return getPlayer(this.numTurnsFinished);
    }

    public boolean rowWon(int row) {

        int boardSize = this.getBoardSize();

        if (this.getBoard()[row][0] == BLANK_TILE) {

            return false;
        }

        for (int col = 1; col < boardSize; col++) {

            if (this.getBoard()[row][col] 
            != this.getBoard()[row][col - 1]) {

                // Incomplete row 
                return false;
            }
        }

        return true;
    }

    public boolean colWon(int col) {

        int boardSize = this.getBoardSize();

        if (this.getBoard()[0][col] == BLANK_TILE) {

            return false;
        }

        for (int row = 1; row < boardSize; row++) {

            if (this.getBoard()[row][col] 
            != this.getBoard()[row - 1][col]) {

                // Incomplete col 
                return false;
            }
        }

        return true;
    }

    public boolean topLeftDiagonalWon() {

        int boardSize = this.getBoardSize();

        if (this.getBoard()[0][0] == BLANK_TILE) {

            return false;
        }

        for (int i = 1; i < boardSize; i++) {

            if (this.getBoard()[i][i] 
            != this.getBoard()[i - 1][i - 1]) {

                // Incomplete diagonal 
                return false;
            }
        }

        return true;
    }

    public boolean bottomLeftDiagonalWon() {

        int boardSize = this.getBoardSize();

        if (this.getBoard()[boardSize - 1][0] == BLANK_TILE) {

            return false;
        }

        for (int i = 1; i < boardSize; i++) {

            if (this.getBoard()[boardSize - 1 - i][i] 
            != this.getBoard()[boardSize - 2 - i][i - 1]) {

                return false;
            }
        }

        return true;
    }

    public boolean diagonalWon() {

        return (this.topLeftDiagonalWon() 
        || this.bottomLeftDiagonalWon());
    }

    public boolean gameWon() {

        int boardSize = this.getBoardSize();

        // Get win rows 
        for (int row = 0; row < boardSize; row++) {

            if (this.rowWon(row)) {

                return true;
            }
        }

        // Get win cols 
        for (int col = 0; col < boardSize; col++) {

            if (this.colWon(col)) {

                return true;
            }
        }

        // Get win diagonals 
        if (this.diagonalWon()) {

            return true;
        }

        return false;
    }

    public void generateMoves() {

        this.generateMoves(0);
    }

    public void generateMoves(int numTurnsFinished) {

        int boardSize = this.getBoardSize();

        if (numTurnsFinished == boardSize * boardSize) {

            System.out.println(this);

            return;
        }

        for (int row = 0; row < boardSize; row++) {

            for (int col = 0; col < boardSize; col++) {

                if (this.getBoard()[row][col] != 0) {

                    // Tile already occupied 
                    continue;
                }

                // Make move 
                this.getBoard()[row][col] = numTurnsFinished;

                generateMoves(numTurnsFinished + 1);

                // Backtrack 
                this.getBoard()[row][col] = 0;
            }
        }
    }

    public String toString() {

        String s = "";

        for (int[] row : board) {

            for (int value : row) {

                s += " " + getPlayer(value) + " ";
            }

            s += "\n";
        }

        s += "\n";

        return s;
    }

    public static void main(String[] args) {

        int boardSize = 10;

        TicTacToeGame aGame = new TicTacToeGame(boardSize);
    }
}