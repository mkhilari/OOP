import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class BracketGenerator {

    public static char OPEN_BRACKET = '(';
    public static char CLOSE_BRACKET = ')';

    public void getBracketSequences(List<String> bracketSequences, 
    char[] bracketSequence, int i, int numOpens, int numPairs) {

        if (numOpens < 0) {

            // Invalid closing brackets 
            return;
        }

        if (i == numPairs * 2) {

            // Bracket sequence completed 

            if (numOpens == 0) {

                // Valid bracket sequence 
                bracketSequences.add(new String(bracketSequence));
            }

            return;
        }

        for (char move : Arrays.asList(OPEN_BRACKET, CLOSE_BRACKET)) {

            // Make move 
            bracketSequence[i] = move;

            int newNumOpens = numOpens 
            + (move == OPEN_BRACKET ? 1 : -1);

            getBracketSequences(bracketSequences, bracketSequence, 
            i + 1, newNumOpens, numPairs);

            // Backtrack 
        }
    }

    public List<String> getBracketSequences(int numPairs) {

        // Returns a list of all valid bracket sequences  
        // with the given numPairs representing 
        // the number of valid bracket pairs 

        List<String> bracketSequences = new ArrayList<>();

        getBracketSequences(bracketSequences, new char[2 * numPairs], 
        0, 0, numPairs);

        return bracketSequences;
    }

    public static void main(String[] args) {

        int numPairs = 4;

        BracketGenerator aBracketGenerator = new BracketGenerator();

        List<String> bracketSequences = aBracketGenerator
        .getBracketSequences(numPairs);

        for (String bracketSequence : bracketSequences) {

            System.out.println(bracketSequence);
        }
    }
}