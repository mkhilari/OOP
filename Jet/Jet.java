package Jet;

public class Jet extends Solid {
    
    public Jet(String name, double speed, double weight) {

        super(name, speed, weight);
    }

    public double race(Jet other, double distance) {

        // Races other jet over distance 
        // Returns time that this jet won by 

        try {

            double thisTime = distance / this.getSpeed();
            double otherTime = distance / other.getSpeed();

            return (otherTime - thisTime);
        } catch (Exception e) {

            System.out.println(e.getMessage());
        }

        return 0;
    }
}
