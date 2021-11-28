package Categoriser;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class CategoryMap<K, V extends Categorisable<K>> {
    
    private HashMap<K, ArrayList<V>> map = new HashMap<>();

    public CategoryMap() {

    }

    public HashMap<K, ArrayList<V>> getMap() {
        return this.map;
    }

    public ArrayList<V> get(K key) {
        
        return this.getMap().get(key);
    }

    public ArrayList<V> getCategory(V value) {

        K key = value.categorise();

        return this.get(key);
    }

    public void put(V value) {

        K key = value.categorise();

        if (!this.getMap().containsKey(key)) {

            // Create new category 
            this.getMap().put(key, new ArrayList<>());
        }

        this.getMap().get(key).add(value);
    }

    public int size() {

        return this.getMap().size();
    }

    public boolean isEmpty() {

        return (this.size() == 0);
    }

    public Set<K> keySet() {

        return this.getMap().keySet();
    }

    public boolean containsKey(K key) {

        return this.getMap().containsKey(key);
    }

    public ArrayList<V> values() {

        ArrayList<V> values = new ArrayList<>();

        for (ArrayList<V> list : this.getMap().values()) {

            values.addAll(list);
        }

        return values;
    }

    public boolean containsValue(V value) {

        return this.values().contains(value);
    }

    public String toString() {

        String s = "";

        for (K key : this.keySet()) {

            String line = key + ": ";

            for (V value : this.get(key)) {

                line += value + ", ";
            }

            line = line.substring(0, line.length() - ", ".length());

            s += line + "\n";
        }

        return s;
    }
}
