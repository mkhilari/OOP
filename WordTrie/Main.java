
import java.util.*;

class TrieNode {
    
    public char value;
    public boolean isWord = false;

    public Map<Character, TrieNode> nexts = new HashMap<>();

    public TrieNode(char value) {

        this.value = value;
    }

    public TrieNode() {

        this(' ');
    }

    public void add(String word) {

        TrieNode curr = this;

        for (char c : word.toCharArray()) {

            if (curr.nexts.get(c) == null) {

                curr.nexts.put(c, new TrieNode(c));
            }

            curr = curr.nexts.get(c);
        }

        curr.isWord = true;
    }

    public boolean search(String word) {

        TrieNode curr = this;

        for (char c : word.toCharArray()) {

            if (curr.nexts.get(c) == null) {

                return false;
            }

            curr = curr.nexts.get(c);
        }

        return curr.isWord;
    }

    public boolean startsWith(String prefix) {

        TrieNode curr = this;

        for (char c : prefix.toCharArray()) {

            if (curr.nexts.get(c) == null) {

                return false;
            }

            curr = curr.nexts.get(c);
        }

        return true;
    }
}


public class Main {

    public static void main(String[] args) {

        TrieNode wordTrie = new TrieNode();

        wordTrie.add("hello");
        wordTrie.add("there");
        wordTrie.add("general");

        System.out.println(wordTrie.search("hello"));
        System.out.println(wordTrie.search("gen"));

        System.out.println(wordTrie.startsWith("gen"));
    }
}