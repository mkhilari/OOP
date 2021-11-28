package Categoriser;

public class Word implements Categorisable<Character> {
    
    private String value;

    public Word(String value) {

        this.value = value;
    }

    public String getValue() {
        return this.value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    public Character categorise() {

        return this.getValue().toCharArray()[0];
    }

    public String toString() {

        return this.getValue();
    }
}
