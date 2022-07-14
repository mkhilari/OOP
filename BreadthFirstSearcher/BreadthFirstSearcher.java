import java.util.Arrays;
import java.util.Deque;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Set;
import java.util.Stack;

public class BreadthFirstSearcher {

    public static final char UNKNOWN_TILE = '*';
    public static final char SHIP_TILE = '1';
    public static final char WATER_TILE = '0';

    private char[][] knownValues;
    private char[][] trueValues;

    public BreadthFirstSearcher(char[][] trueValues) {

        this.trueValues = trueValues;

        // Initialise knownValues 
        int numRows = this.getNumRows();
        int numCols = this.getNumCols();

        this.knownValues = new char[numRows][numCols];

        for (int row = 0; row < numRows; row++) {

            for (int col = 0; col < numCols; col++) {

                this.knownValues[row][col] = UNKNOWN_TILE;
            }
        }
    }

    public String toString(char[][] values) {

        String s = "";

        for (char[] row : values) {

            s += Arrays.toString(row) + "\n";
        }

        return s;
    }

    public int getNumRows() {

        return this.trueValues.length;
    }

    public int getNumCols() {

        return (this.getNumRows() > 0 ? 
        this.trueValues[0].length : 0);
    }

    public int getIndex(int row, int col) {

        // Returns the unique index representing 
        // the given location (row, col) 

        return (row * this.getNumCols() + col);
    }

    public void reveal(int row, int col) {

        // Reveals the given location (row, col) 

        this.knownValues[row][col] = this.trueValues[row][col];

        System.out.println(this.toString(this.knownValues));
    }

    public void expand(int startRow, int startCol) {

        // Expands the given board 
        // at the given ship tile (row, col) 

        int numRows = this.getNumRows();
        int numCols = this.getNumCols();

        // BFS 
        Queue<Integer> q = new LinkedList<>();
        q.add(this.getIndex(startRow, startCol));

        Set<Integer> seen = new HashSet<>();

        while (!q.isEmpty()) {

            int curr = q.poll();

            if (seen.contains(curr)) {

                continue;
            }

            seen.add(curr);

            int row = curr / numCols;
            int col = curr % numCols;

            if (this.knownValues[row][col] == WATER_TILE) {

                // No need to continue expanding after water is reached 
                continue;
            }

            // Expand curr and reveal new locations 
            boolean validTop = (row > 0);

            if (validTop) {

                q.add(this.getIndex(row - 1, col));
                this.reveal(row - 1, col);
            }

            boolean validBottom = (row <= numRows - 2);

            if (validBottom) {

                q.add(this.getIndex(row + 1, col));
                this.reveal(row + 1, col);
            }

            boolean validLeft = (col > 0);

            if (validLeft) {

                q.add(this.getIndex(row, col - 1));
                this.reveal(row, col - 1);
            }

            boolean validRight = (col <= numCols - 2);

            if (validRight) {

                q.add(this.getIndex(row, col + 1));
                this.reveal(row, col + 1);
            }
        }
    }

    public void search(int row, int col) {

        // Searches the given board at 
        // the given location (row, col) 

        if (this.knownValues[row][col] != UNKNOWN_TILE) {

            // Location already searched 
            return;
        }

        // Reveal the given location 
        this.reveal(row, col);

        if (this.knownValues[row][col] == WATER_TILE) {

            // No ship at the given location 
            return;
        }

        // Ship found at the given location 
        this.expand(row, col);
    }

    public void search() {

        int numRows = this.getNumRows();
        int numCols = this.getNumCols();

        for (int row = 0; row < numRows; row++) {

            for (int col = 0; col < numCols; col++) {

                this.search(row, col);
            }
        }
    }

    public static void main(String[] args) {

        int numRows = 5;
        int numCols = 5;

        char[][] trueValues = new char[numRows][];

        trueValues[0] = new char[]{'0', '1', '0', '1', '1'};
        trueValues[1] = new char[]{'0', '1', '0', '0', '0'};
        trueValues[2] = new char[]{'0', '1', '0', '1', '0'};
        trueValues[3] = new char[]{'0', '1', '0', '1', '0'};
        trueValues[4] = new char[]{'0', '0', '0', '1', '0'};

        BreadthFirstSearcher aSearcher 
        = new BreadthFirstSearcher(trueValues);

        aSearcher.search();
    }
}