import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
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

    public String toString() {

        return "(" + this.routeSpeed + ", " + this.upTime + ")";
    }
}

public class RouteSpeeds {

    public static int sendTime(List<Integer> routeSpeeds, 
    List<Integer> packetSizes) {

        int r = routeSpeeds.size();
        int n = packetSizes.size();

        int sendTime = 0;

        // Get routes by upTime ascending 
        // then routeSpeed ascending 
        PriorityQueue<Route> routes = new PriorityQueue<>(
            (a, b) -> (a.upTime != b.upTime ? 
            (a.upTime - b.upTime) : (a.routeSpeed - b.routeSpeed)));
        
        for (int routeSpeed : routeSpeeds) {

            routes.add(new Route(routeSpeed));
        }

        // Send packets 
        int i = 0;

        while (i < n) {

            // Get next routes 
            List<Route> nextRoutes = new ArrayList<>();
            int nextUpTime = routes.peek().upTime;

            List<Integer> nextPackets = new ArrayList<>();

            while (!routes.isEmpty() && routes.peek().upTime == nextUpTime) {

                nextRoutes.add(routes.poll());

                nextPackets.add(packetSizes.get(i++));
            }

            // Send the largest packet first 
            Collections.sort(nextPackets);
            Collections.reverse(nextPackets);

            System.out.println(nextRoutes);
            System.out.println(nextPackets);

            for (int j = 0; j < nextRoutes.size(); j++) {

                nextRoutes.get(j).send(nextPackets.get(j));
                routes.add(nextRoutes.get(j));

                sendTime = Math.max(sendTime, nextRoutes.get(j).upTime);
            }
        }
        
        return sendTime;
    }

    public static void main(String[] args) {

        List<Integer> routeSpeeds = new ArrayList<>(
            Arrays.asList(2, 3, 5));
        
        List<Integer> packetSizes = new ArrayList<>(
            Arrays.asList(4, 5, 10, 3, 4, 6, 10));
        
        int sendTime = sendTime(routeSpeeds, packetSizes);

        System.out.println(sendTime);
    }
}