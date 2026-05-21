using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Change_Color_of_Terminal
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.ForegroundColor = ConsoleColor.DarkBlue;
            Console.BackgroundColor = ConsoleColor.White;
            Console.Clear();
            Console.WriteLine("Hello, World!");
            Console.WriteLine("|nThis text is dark blue on a white background.|n");
            Console.ForegroundColor = ConsoleColor.DarkGreen;
            Console.WriteLine("Press alt+F4 to exit...");
            Console.Read();
        }
    }
}
