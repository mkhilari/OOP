

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

    public void generateMoves() {

        this.generateMoves(0);
    }

    public void generateMoves(int numTurnsFinished) {

        System.out.println(this);

        int boardSize = this.getBoardSize();

        if (numTurnsFinished == boardSize * boardSize) {

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

        int boardSize = 5;

        TicTacToeGame aGame = new TicTacToeGame(boardSize);
    }
}