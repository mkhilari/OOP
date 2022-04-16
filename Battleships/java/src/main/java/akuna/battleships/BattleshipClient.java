package akuna.battleships;

import java.io.IOException;
import java.util.Comparator;
import java.util.Map;
import java.util.Random;
import java.util.stream.Collectors;

class BattleshipClient {
    private static final Map<String, Integer> SHIPS = Map.of(
            "aircraftcarrier", 5,
            "battleship", 4,
            "submarine", 3,
            "cruiser", 3,
            "destroyer", 2
    );
    private static final char[] COLS = "abcdefghij".toCharArray();
    private static final char[] ROWS = "0123456789".toCharArray();

    private static String getShipName(char identifier) {
        for (final String shipName : SHIPS.keySet()) {
            if (shipName.charAt(0) == identifier) {
                return shipName;
            }
        }
        return "unknown";
    }

    private final Connection conn;
    private final String name;
    private final Random random;
    private boolean gameOver;

    BattleshipClient(Connection conn, String name) {
        this.conn = conn;
        this.name = name;
        this.random = new Random();
    }

    boolean isGameOver() {
        return gameOver;
    }

    void configure() throws IOException {
        this.conn.send(String.format("id %s", this.name));  // self identify
        this.conn.send("autodump");  // turn on dumping the board after every move
    }

    void placeShips() throws IOException {
        final var col = "a";
        var row = 1;
        final var ships = SHIPS.entrySet().stream()
                .sorted(Map.Entry.comparingByValue(Comparator.reverseOrder()))
                .map(Map.Entry::getKey)
                .collect(Collectors.toList());
        for (final var ship : ships) {
            this.conn.send(String.format("place %s %s%d horizontal", ship, col, row));
            this.conn.getLine();
            row++;
        }
    }

    void waitForGo() throws IOException {
        String line;
        do {
            line = this.conn.getLine();
        } while (!line.startsWith("go"));
    }

    void shoot() throws IOException {
        final var col = COLS[this.random.nextInt(COLS.length)];
        final var row = ROWS[this.random.nextInt(ROWS.length)];
        this.conn.send(String.format("shoot %s%s", col, row));
        this.handlePlayerResult(this.conn.getLine());
    }

    void awaitPartnerTurn() throws IOException {
        this.handlePartnerResult(this.conn.getLine());
    }

    private void handlePlayerResult(String result) {
        if (result.startsWith("hit")) {
            System.out.println("Yay!");
        } else if (result.startsWith("miss")) {
            System.out.println("Boo");
        } else if (result.startsWith("sunk")) {
            final var identifier = result.charAt(result.length() - 1);
            System.out.println(String.format("HA! I sunk your %s", BattleshipClient.getShipName(identifier)));
        } else if (result.startsWith("won")) {
            final var identifier = result.charAt(result.length() - 1);
            System.out.println(String.format("HA! I sunk your %s", BattleshipClient.getShipName(identifier)));
            System.out.println("HOORAY!!!");
            this.gameOver = true;
        } else {
            System.out.println(String.format("Unknown result: %s", result));
        }
    }

    private void handlePartnerResult(String result) {
        if (result.startsWith("partner hit")) {
            System.out.println("Darn");
        } else if (result.startsWith("partner miss")) {
            System.out.println("Nah nah nay");
        } else if (result.startsWith("partner sunk")) {
            final var identifier = result.charAt(result.length() - 1);
            System.out.println(String.format("AH! You sunk my %s", BattleshipClient.getShipName(identifier)));
        } else if (result.startsWith("partner won")) {
            final var identifier = result.charAt(result.length() - 1);
            System.out.println(String.format("AH! You sunk my %s", BattleshipClient.getShipName(identifier)));
            System.out.println("drats");
            this.gameOver = true;
        } else {
            System.out.println(String.format("Unknown partner result: %s", result));
        }
    }
}
