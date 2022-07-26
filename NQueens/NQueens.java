import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class NQueens {

    public static final char BLANK_TILE = '_';
    public static final char QUEEN_TILE = 'Q';

    public int n;

    public NQueens(int n) {

        this.n = n;
    }

    public List<List<Integer>> generateNQueens() {

        List<List<Integer>> solutions = new ArrayList<>();

        generateNQueens(solutions, new ArrayList<>(), 0, 
        new HashSet<>(), new HashSet<>(), 
        new HashSet<>(), new HashSet<>());

        return solutions;
    }

    public void generateNQueens(List<List<Integer>> solutions, 
    List<Integer> queens, int start, 
    Set<Integer> usedRows, Set<Integer> usedCols, 
    Set<Integer> usedUpDiagonals, Set<Integer> usedDownDiagonals) {

        if (queens.size() == this.n) {

            // All queens have been placed 
            solutions.add(new ArrayList<>(queens));

            return;
        }

        // Place queens after start to avoid duplicate solutions 
        for (int i = start; i < this.n * this.n; i++) {

            int row = i / this.n;
            int col = i % this.n;
            int upDiagonal = col + row;
            int downDiagonal = col - row;

            if (usedRows.contains(row) || usedCols.contains(col) 
            || usedUpDiagonals.contains(upDiagonal) 
            || usedDownDiagonals.contains(downDiagonal)) {

                // Invalid location 
                continue;
            }

            // Make move 
            queens.add(i);

            usedRows.add(row);
            usedCols.add(col);
            usedUpDiagonals.add(upDiagonal);
            usedDownDiagonals.add(downDiagonal);

            int newStart = i + 1;

            generateNQueens(solutions, queens, newStart, 
            usedRows, usedCols, usedUpDiagonals, usedDownDiagonals);

            // Backtrack 
            queens.remove(queens.size() - 1);

            usedRows.remove(row);
            usedCols.remove(col);
            usedUpDiagonals.remove(upDiagonal);
            usedDownDiagonals.remove(downDiagonal);
        }
    }

    public static String toBoard(List<Integer> queens) {

        int n = queens.size();

        char[][] board = new char[n][n];

        for (int row = 0; row < n; row++) {

            for (int col = 0; col < n; col++) {

                board[row][col] = BLANK_TILE;
            }
        }

        // Set queens 
        for (int queen : queens) {

            int queenRow = queen / n;
            int queenCol = queen % n;

            board[queenRow][queenCol] = QUEEN_TILE;
        }

        String s = "";

        for (char[] row : board) {

            s += "[ ";

            for (char value : row) {

                s += value + " ";
            }

            s += "]\n";
        }

        s += "\n";

        return s;
    }

    public static void main(String[] args) {

        int n = 4;

        NQueens aBoard = new NQueens(n);

        List<List<Integer>> solutions = aBoard.generateNQueens();

        for (List<Integer> queens : solutions) {

            System.out.println(toBoard(queens));
        }
    }
}