using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;

namespace Akuna.Battleships
{
    class BattleshipClient
    {
        private static readonly Dictionary<string, int> SHIPS = new Dictionary<string, int>
        {
            ["aircraftcarrier"] = 5,
            ["battleship"] = 4,
            ["submarine"] = 3,
            ["cruiser"] = 3,
            ["destroyer"] = 2,
        };
        private static readonly char[] COLS = "abcdefghij".ToCharArray();
        private static readonly char[] ROWS = "0123456789".ToCharArray();

        private static String GetShipName(char identifier)
        {
            foreach (String shipName in SHIPS.Keys)
            {
                if (shipName[0] == identifier)
                {
                    return shipName;
                }
            }
            return "unknown";
        }

        private readonly Connection _conn;
        private readonly string _name;
        private readonly Random _random;

        public BattleshipClient(Connection conn, String name)
        {
            _conn = conn;
            _name = name;
            _random = new Random();
        }

        public bool GameOver { get; private set; }

        public void Configure()
        {
            _conn.Send($"id {_name}");  // self identify
            _conn.Send("autodump");  // turn on dumping the board after every move
        }

        public void PlaceShips()
        {
            var col = "a";
            var row = 1;
            var ships = from kvp in SHIPS
                        orderby kvp.Value descending
                        select kvp.Key;
            foreach (var ship in ships)
            {
                _conn.Send($"place {ship} {col}{row} horizontal");
                _conn.GetLine();
                row++;
            }
        }

        public void WaitForGo()
        {
            String line;
            do
            {
                line = _conn.GetLine();
            }
            while (!line.StartsWith("go"));
        }

        public void Shoot()
        {
            var col = COLS[_random.Next(COLS.Length)];
            var row = ROWS[_random.Next(ROWS.Length)];
            _conn.Send($"shoot {col}{row}");
            HandlePlayerResult(_conn.GetLine());
        }

        public void AwaitPartnerTurn()
        {
            HandlePartnerResult(_conn.GetLine());
        }

        private void HandlePlayerResult(String result)
        {
            if (result.StartsWith("hit"))
            {
                Console.WriteLine("Yay!");
            }
            else if (result.StartsWith("miss"))
            {
                Console.WriteLine("Boo");
            }
            else if (result.StartsWith("sunk"))
            {
                var identifier = result[result.Length - 1];
                Console.WriteLine(string.Format("HA! I sunk your {0}", BattleshipClient.GetShipName(identifier)));
            }
            else if (result.StartsWith("won"))
            {
                var identifier = result[result.Length - 1];
                Console.WriteLine(string.Format("HA! I sunk your {0}", BattleshipClient.GetShipName(identifier)));
                Console.WriteLine("HOORAY!!!");
                GameOver = true;
            }
            else
            {
                Console.WriteLine($"Unknown result: {result}");
            }
        }

        private void HandlePartnerResult(String result)
        {
            if (result.StartsWith("partner hit"))
            {
                Console.WriteLine("Darn");
            }
            else if (result.StartsWith("partner miss"))
            {
                Console.WriteLine("Nah nah nay");
            }
            else if (result.StartsWith("partner sunk"))
            {
                var identifier = result[result.Length - 1];
                Console.WriteLine(string.Format("AH! You sunk my {0}", BattleshipClient.GetShipName(identifier)));
            }
            else if (result.StartsWith("partner won"))
            {
                var identifier = result[result.Length - 1];
                Console.WriteLine(string.Format("AH! You sunk my {0}", BattleshipClient.GetShipName(identifier)));
                Console.WriteLine("drats");
                GameOver = true;
            }
            else
            {
                Console.WriteLine($"Unknown partner result: {result}");
            }
        }
    }
}
