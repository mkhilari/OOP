package Routes;

public class Route implements Comparable<Route> {

    public int cost; 
    public int upTime = 0;

    public Route(int cost) {

        this.cost = cost;
    }

    public void send(int packetSize) {

        this.upTime += this.cost * packetSize;
    }

    public int compareTo(Route other) {

        if (this.upTime != other.upTime) {

            // upTime ascending 
            return (this.upTime - other.upTime);
        }

        // cost descending 
        return (other.cost - this.cost);
    }
}