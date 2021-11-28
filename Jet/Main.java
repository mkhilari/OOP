package Jet;

public class Main {
    
    public static void main(String[] args) {

        Jet jetA = new Jet("McLaren", 320, 1200);
        Jet jetB = new Jet("Porsche", 310, 800);

        jetA.upgrade(new Upgrade("Smooth Fuel", 10, 100));
        jetB.upgrade(new Upgrade("Carbon Fiber", 15, -200));

        double winTime = jetA.race(jetB, 3000);

        System.out.println(jetA);
        System.out.println(jetB);

        System.out.println("Race winTime " + winTime + "s");
    }
}
