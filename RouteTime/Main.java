import java.util.Collections;
import java.util.PriorityQueue;

class Route implements Comparable<Route> {

    public int routeSpeed;
    public int upTime = 0;

    public Route(int routeSpeed) {

        this.routeSpeed = routeSpeed;
    }

    public int compareTo(Route other) {

        // Sort by upTime ascending then routeSpeed ascending 
        if (this.upTime != other.upTime) {

            return (this.upTime - other.upTime);
        }

        return (this.routeSpeed - other.routeSpeed);
    }

    public int send(int packetSize) {

        // Update upTime 
        this.upTime += this.routeSpeed * packetSize;

        return this.upTime;
    }
}

public class Main {
    
    public static List<Route> getNextRoutes(PriorityQueue<Route> routes) {

        List<Route> nextRoutes = new ArrayList();
        int nextUpTime = routes.peek().upTime;

        while (!routes.isEmpty() && routes.peek().upTime == nextUpTime) {

            nextRoutes.add(routes.poll());
        }

        return nextRoutes;
    }

    public static List<Integer> getNextPackets(List<Integer> packetSizes, 
    int left, int numPackets) {

        int n = packetSizes.size();

        List<Integer> nextPackets = new ArrayList();

        for (int i = left; i < left + numPackets; i++) {

            nextPackets.add(i < n ? 
            packetSizes.get(i) : 0);
        }

        return nextPackets;
    }

    public static int sendTime(List<Integer> routeSpeeds, List<Integer> packetSizes) {

        int r = routeSpeeds.size();
        int n = packetSizes.size();

        int sendTime = 0;

        PriorityQueue<Route> routes = new PriorityQueue<>();

        for (int routeSpeed : routeSpeeds) {

            routes.add(new Route(routeSpeed));
        }

        int i = 0;

        while (i < n) {

            List<Route> nextRoutes = getNextRoutes(routes);

            List<Integer> nextPackets = getNextPackets(packetSizes, 
            i, nextRoutes.size());

            Collections.sort(nextPackets);
            Collections.reverse(nextPackets);

            for (int j = 0; j < nextRoutes.size(); j++) {

                int newTime = nextRoutes.get(j).send(nextPackets.get(j));

                // Update sendTime 
                sendTime = Math.max(sendTime, newTime);

                routes.add(nextRoutes.get(j));
            }
        }

        System.out.println(routes.toString());

        return sendTime;
    }

    public static void main(String[] args) {

        List<Integer> routeSpeeds = new ArrayList(
            Arrays.asList(1, 5, 2, 3)
        );
        
        List<Integer> packetSizes = new ArrayList(
            Arrays.asList(3, 2, 4, 1, 5, 4, 3, 7, 2, 3, 1)
        );

        int sendTime = sendTime(routeSpeeds, packetSizes);

        System.out.println(sendTime);
    }
}
