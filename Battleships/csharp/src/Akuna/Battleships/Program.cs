using System;

namespace Akuna.Battleships
{
    public class Program
    {
        public static void Main(string[] args)
        {
            if (args.Length != 1)
            {
                Console.WriteLine("provide server host as the only argument");
                return;
            }

            var host = args[0];
            var name = "Daisy Duck";  // set this to your name
            using (var conn = new Connection(host))
            {
                var client = new BattleshipClient(conn, name);
                client.Configure();
                client.PlaceShips();
                client.WaitForGo();
                do
                {
                    client.Shoot();
                    if (client.GameOver)
                    {
                        break;
                    }
                    client.AwaitPartnerTurn();
                }
                while (!client.GameOver);
            }
        }
    }
}
