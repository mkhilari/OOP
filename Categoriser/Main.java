package Categoriser;

public class Main {
    
    public static void main(String[] args) {

        CategoryMap<Character, Word> categoryMap = new CategoryMap<>();

        categoryMap.put(new Word("Hello"));
        categoryMap.put(new Word("There"));
        categoryMap.put(new Word("Wise"));
        categoryMap.put(new Word("Words"));

        System.out.println(categoryMap);
    }
}
