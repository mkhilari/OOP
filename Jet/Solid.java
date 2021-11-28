package Jet;

import java.util.ArrayList;

public abstract class Solid implements Upgradeable {

    private String name;
    private double speed;
    private double weight;

    private ArrayList<Upgrade> upgrades = new ArrayList<>();

    public Solid(String name, double speed, double weight) {

        this.name = name;
        this.speed = speed;
        this.weight = weight;
    }
    
    public String getName() {
        return this.name;
    }

    public double getSpeed() {
        return this.speed;
    }

    public double getWeight() {
        return this.weight;
    }

    public ArrayList<Upgrade> getUpgrades() {
        return this.upgrades;
    }

    public void setSpeed(double speed) {
        this.speed = speed;
    }

    public void setWeight(double weight) {
        this.weight = weight;
    }

    public void upgrade(Upgrade newUpgrade) {

        this.getUpgrades().add(newUpgrade);
        
        this.setSpeed(this.getSpeed() + newUpgrade.getSpeed());
        this.setWeight(this.getWeight() + newUpgrade.getWeight());
    }

    public String toString() {

        String s = this.getName() + " (";

        for (Upgrade upgrade : this.getUpgrades()) {

            s += upgrade + ", ";
        }

        s = s.substring(0, s.length() - ", ".length());
        s += ")";

        return s;
    }
}
