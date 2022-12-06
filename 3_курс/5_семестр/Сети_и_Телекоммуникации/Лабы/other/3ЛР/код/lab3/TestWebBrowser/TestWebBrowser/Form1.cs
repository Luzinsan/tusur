using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;
using System.Net.Security;
using System.IO;

namespace TestWebBrowser
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Go_Click(object sender, EventArgs e)
        {
            switch(tabControl1.SelectedIndex)
            {
                case 0:
                    webBrowser1.Navigate(textBox1.Text);
                    break;
                case 1:
                    webBrowser2.Navigate(textBox1.Text);
                    break;
                case 2:
                    webBrowser3.Navigate(textBox1.Text);
                    break;
                default:
                    break;
            }
            
        }

        private void Forward_Click(object sender, EventArgs e)
        {
            switch (tabControl1.SelectedIndex)
            {
                case 0:
                    webBrowser1.GoForward();
                    break;
                case 1:
                    webBrowser2.GoForward();
                    break;
                case 2:
                    webBrowser3.GoForward();
                    break;
                default:
                    break;
            }
        }

        private void Backward_Click(object sender, EventArgs e)
        {
            switch (tabControl1.SelectedIndex)
            {
                case 0:
                    webBrowser1.GoBack();
                    break;
                case 1:
                    webBrowser2.GoBack();
                    break;
                case 2:
                    webBrowser3.GoBack();
                    break;
                default:
                    break;
            }
        }

        private void Exit_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        //Ищу последнюю запись с подстрокой http, вывожу страницу на экран htmlTest
        private void httpButton_Click(object sender, EventArgs e)
        {
            string server = "tusur.ru";
            TcpClient client = new TcpClient(server, 443);
            SslStream sslStream = new SslStream(client.GetStream());
            sslStream.AuthenticateAsClient(server);
            var reader = new StreamReader(sslStream);
            var writer = new StreamWriter(sslStream);
            string navigationString = "/index.html";
            writer.WriteLine("GET " + navigationString + " HTTP/1.0 \r\nHost: " + server + "\r\nConnection: close\r\n\r\n");
            writer.Flush();
            string line;
            int hrefIndex;
            while (!reader.EndOfStream)
            {
                line = reader.ReadLine();
                if ((hrefIndex = line.IndexOf("https")) != -1)
                {
                    string tmp = line.Substring(hrefIndex);
                    hrefIndex = tmp.IndexOf("\"");
                    if(hrefIndex != -1) navigationString = tmp.Remove(hrefIndex, tmp.Length - hrefIndex);
                }
            }
            writer.Close();
            reader.Close();
            client.Close();
            webBrowser4.Navigate(navigationString);
        }

        private void ftpButton_Click(object sender, EventArgs e)
        {
            string server = "ftp.iao.ru";
            TcpClient client = new TcpClient(server, 21);
            var reader = new StreamReader(client.GetStream());
            var writer = new StreamWriter(client.GetStream());
            string second, tmp;

            textBox2.AppendText(reader.ReadLine());
            textBox2.AppendText(Environment.NewLine);

            writer.WriteLine("USER anonymous");
            writer.Flush();
            textBox2.AppendText(reader.ReadLine());
            textBox2.AppendText(Environment.NewLine);

            writer.WriteLine("PASS nope");
            writer.Flush();
            textBox2.AppendText(reader.ReadLine());
            textBox2.AppendText(Environment.NewLine);
            textBox2.AppendText(reader.ReadLine());
            textBox2.AppendText(Environment.NewLine);
            textBox2.AppendText(reader.ReadLine());
            textBox2.AppendText(Environment.NewLine);
            textBox2.AppendText(reader.ReadLine());
            textBox2.AppendText(Environment.NewLine);

            writer.WriteLine("PASV");
            writer.Flush();
            tmp = reader.ReadLine();
            textBox2.AppendText(tmp);
            textBox2.AppendText(Environment.NewLine);

            writer.WriteLine("LIST");
            writer.Flush();

            string portNum1, portNum2;
            int indx;
            tmp = tmp.Substring(tmp.IndexOf("(") + 1);
            second = tmp.Remove(tmp.IndexOf(")"), 2);
            indx = tmp.LastIndexOf(",");
            portNum1 = second.Substring(indx + 1);
            second = second.Remove(indx, second.Length - indx);
            indx = second.LastIndexOf(",");
            portNum2 = second.Substring(indx + 1);
            second = second.Remove(indx, second.Length - indx);

            int port = Convert.ToInt32(portNum2) * 256 + Convert.ToInt32(portNum1);
            second = second.Replace(',','.');
            TcpClient reciever = new TcpClient(second, port);
            var recieverRd = new StreamReader(reciever.GetStream());
            var recieverWr = new StreamWriter(reciever.GetStream());
            while(!recieverRd.EndOfStream)
            {
                textBox2.AppendText(recieverRd.ReadLine());
                textBox2.AppendText(Environment.NewLine);
            }

            recieverRd.Close();
            recieverWr.Close();
            reciever.Close();
            reader.Close();
            writer.Close();
            client.Close();
        }
    }
}
