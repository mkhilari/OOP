import java.util.HashMap;
import java.util.Map;

class Stock {

    public String name;
    public int price;

    public Stock(String name, int price) {

        this.name = name;
        this.price = price;
    }
}

public abstract class Trader {

    private Map<String, Integer> minPrice = new HashMap<>();
    private Map<String, Integer> maxPrice = new HashMap<>();

    public Trader() {

    }
    
    public abstract boolean shouldBuy(String stockName, int newPrice);

    public boolean goodBuy(String stockName, int newPrice) {

        // Returns true if the given stock is worth buying 
        // at the given price 

        if (minPrice.containsKey(stockName) 
        && minPrice.get(stockName) > newPrice) {

            return true;
        }

        if (maxPrice.containsKey(stockName) 
        && maxPrice.get(stockName) < newPrice) {

            return false;
        }

        boolean buy = shouldBuy(stockName, newPrice);

        if (buy) {

            minPrice.put(stockName, newPrice);

            return true;
        }

        maxPrice.put(stockName, newPrice);

        return false;
    }
}

class FlatTrader extends Trader {

    private int maxPrice;

    public FlatTrader(int maxPrice) {

        this.maxPrice = maxPrice;
    }

    public boolean shouldBuy(String stockName, int newPrice) {

        return (newPrice <= maxPrice);
    }

    public static void main(String args[]) {

        int maxPrice = 15;

        FlatTrader aFlatTrader = new FlatTrader(maxPrice);

        String stockName = "MELB";

        boolean buy1 = aFlatTrader.goodBuy(stockName, 10);
        System.out.println(buy1);

        boolean buy2 = aFlatTrader.goodBuy(stockName, 20);
        System.out.println(buy2);

        boolean buy3 = aFlatTrader.goodBuy(stockName, 5);
        System.out.println(buy3);

        boolean buy4 = aFlatTrader.goodBuy(stockName, 12);
        System.out.println(buy4);
    }
}