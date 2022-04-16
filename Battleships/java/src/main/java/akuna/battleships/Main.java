package akuna.battleships;

import java.io.IOException;

public final class Main {
    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            System.out.println("Provide server host as the only argument");
            return;
        }

        final var host = args[0];
        final var name = "Minnie Mouse";  // set this to your name
        try (final var conn = new Connection(host)) {
            final var client = new BattleshipClient(conn, name);
            client.configure();
            client.placeShips();
            client.waitForGo();
            do {
                client.shoot();
                if (client.isGameOver()) {
                    break;
                }
                client.awaitPartnerTurn();
            } while (!client.isGameOver());
        }
    }
}
