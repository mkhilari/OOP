package Routes;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.PriorityQueue;

public class Main {
    
    public static int getMinTime(List<Integer> routeCosts, 
    List<Integer> packetSizes) {

        int n = packetSizes.size();

        // Create min heap of routes 
        PriorityQueue<Route> routes = new PriorityQueue<>();

        for (int routeCost : routeCosts) {

            routes.add(new Route(routeCost));
        }

        // Move through packetSizes 
        int i = 0;

        while (i < n) {

            // Get all next up routes 
            int nextUpTime = routes.isEmpty() ? 
            0 : routes.peek().upTime;

            List<Route> nextUpRoutes = new ArrayList<>();

            while (!routes.isEmpty() 
            && routes.peek().upTime == nextUpTime) {

                nextUpRoutes.add(routes.poll());
            }

            // Get next up packets 
            int[] nextUpPacketSizes = new int[nextUpRoutes.size()];

            for (int j = 0; j < nextUpRoutes.size(); j++) {

                nextUpPacketSizes[j] = i < n ? 
                packetSizes.get(i++) : 0;
            }

            Arrays.sort(nextUpPacketSizes);

            // Send packets 
            for (int j = 0; j < nextUpRoutes.size(); j++) {

                nextUpRoutes.get(j).send(nextUpPacketSizes[j]);

                // Put route back in min heap 
                routes.add(nextUpRoutes.get(j));
            }
        }

        return getFinalRoute(routes).upTime;
    }

    public static Route getFinalRoute(PriorityQueue<Route> routes) {

        Route finalRoute = routes.poll();

        while (!routes.isEmpty()) {

            finalRoute = routes.poll();
        }

        return finalRoute;
    }

    public static void main(String[] args) {

        List<Integer> routeCosts = new ArrayList<>(
            Arrays.asList(2, 3, 4));
            
        List<Integer> packetSizes = new ArrayList<>(
            Arrays.asList(5, 7, 8, 3, 9, 2, 5, 6));

        int minTime = getMinTime(routeCosts, packetSizes);

        System.out.println("minTime = " + minTime);
    }
}
