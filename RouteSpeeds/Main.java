
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;

class Route {

    public int routeSpeed;
    public int upTime = 0;

    public Route(int routeSpeed) {

        this.routeSpeed = routeSpeed;
    }

    public void send(int packetSize) {

        this.upTime += this.routeSpeed * packetSize;
    }
}


public class Main {

    public static List<Route> getNextRoutes(PriorityQueue<Route> routes) {

        // Returns all routes up at the next up time 

        List<Route> nextRoutes = new ArrayList();
        int nextUpTime = routes.peek().upTime;

        while (!routes.isEmpty() && routes.peek().upTime == nextUpTime) {

            nextRoutes.add(routes.poll());
        }

        return nextRoutes;
    }

    public static List<Integer> getNextPackets(List<Integer> packets, 
    int left, int numPackets) {

        // Returns the next numPackets packets 

        List<Integer> nextPackets = new ArrayList();

        for (int i = left; i < left + numPackets; i++) {

            nextPackets.add(i < packets.size() ? 
            packets.get(i) : 0);
        }

        return nextPackets;
    }

    public static Route getFinalRoute(PriorityQueue<Route> routes) {

        Route finalRoute = routes.poll();

        while (!routes.isEmpty()) {

            finalRoute = routes.poll();
        }

        return finalRoute;
    }

    public static int sendTime(List<Integer> routeSpeeds, List<Integer> packetSizes) {

        int r = routeSpeeds.size();
        int n = packetSizes.size();

        PriorityQueue<Route> routes = new PriorityQueue<>(
            (a, b) -> a.upTime != b.upTime ? 
            Integer.compare(a.upTime, b.upTime) 
            : Integer.compare(a.routeSpeed, b.routeSpeed)
        );

        for (int routeSpeed : routeSpeeds) {

            routes.add(new Route(routeSpeed));
        }

        for (int i = 0; i < n;) {

            List<Route> nextRoutes = getNextRoutes(routes);

            List<Integer> nextPackets = getNextPackets(packetSizes, 
            i, nextRoutes.size());
            i += nextPackets.size();

            // Send the largest packet first 
            nextPackets.sort((a, b) -> -Integer.compare(a, b));

            for (int j = 0; j < nextRoutes.size(); j++) {

                nextRoutes.get(j).send(nextPackets.get(j));

                routes.add(nextRoutes.get(j));
            }
        }

        Route finalRoute = getFinalRoute(routes);

        return finalRoute.upTime;
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