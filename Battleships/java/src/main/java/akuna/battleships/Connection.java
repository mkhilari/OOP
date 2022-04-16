package akuna.battleships;

import java.io.*;
import java.net.Socket;

class Connection implements AutoCloseable {
    private static int DEFAULT_PORT = 50008;

    private final Socket socket;
    private final BufferedReader reader;
    private final Writer writer;

    private Connection(String host, int port) throws IOException {
        System.out.println(String.format("Connecting to %s:%d", host, port));
        this.socket = new Socket(host, port);
        this.reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        this.writer = new OutputStreamWriter(this.socket.getOutputStream());
    }

    Connection(String host) throws IOException {
        this(host, DEFAULT_PORT);
    }

    void send(String msg) throws IOException {
        System.out.println(String.format("> %s", msg));
        this.writer.write(msg);
        this.writer.write(System.lineSeparator());
        this.writer.flush();
    }

    String getLine() throws IOException {
        String line;
        do {
            line = this.reader.readLine();
            System.out.println(String.format("< %s", line));
            if (line == null) {
                return null;
            }
        } while (line.isEmpty() || line.charAt(0) == ' ');
        return line;
    }

    public void close() throws IOException {
        this.writer.close();
        try {
            this.reader.close();
        } finally {
            this.socket.close();
        }
    }
}
