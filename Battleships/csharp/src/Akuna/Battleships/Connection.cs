using System;
using System.IO;
using System.Net.Sockets;

namespace Akuna.Battleships
{
    public class Connection : IDisposable
    {
        private static readonly int DEFAULT_PORT = 50008;

        private readonly TcpClient _client;
        private readonly StreamReader _reader;
        private readonly StreamWriter _writer;

        public Connection(String host, int port)
        {
            System.Console.WriteLine($"Connecting to {host}:{port}");
            _client = new TcpClient(host, port);
            _reader = new StreamReader(_client.GetStream());
            _writer = new StreamWriter(_client.GetStream());
        }

        public Connection(String host)
            : this(host, DEFAULT_PORT)
            { }

        public void Send(String msg)
        {
            Console.WriteLine($"> {msg}");
            _writer.WriteLine(msg);
            _writer.Flush();
        }

        public String GetLine()
        {
            String line;
            do
            {
                line = _reader.ReadLine();
                Console.WriteLine($"< {line}");
                if (line == null)
                {
                    return null;
                }
            }
            while (line == "" || line[0] == ' ');
            return line;
        }

        public void Dispose()
        {
            _writer.Close();
            _reader.Close();
            _client.Close();
        }
    }
}
