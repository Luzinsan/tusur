#include <iostream>
#include <ws2tcpip.h>
#include <winsock2.h>

using namespace std;

int main()
{
    WSADATA WsaData;
    int err = WSAStartup(0x0101, &WsaData);
    if (err == SOCKET_ERROR) 
    {
        cout << "WSAStartup() failed: % ld\n" << GetLastError() << endl;
        return 1;
    }
    int s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    SOCKADDR_IN sin;
    sin.sin_family = AF_INET;
    sin.sin_port = htons(10080);
    inet_pton(AF_INET, "172.17.11.31", &sin.sin_addr.s_addr);
    err = bind(s, (LPSOCKADDR)&sin, sizeof(sin));
    err = listen(s, SOMAXCONN);
    while (1)
    {
        SOCKADDR_IN from;
        int fromlen = sizeof(from);
        int s1 = accept(s, (struct sockaddr*)&from, &fromlen);
        if (s1 >= 0)
        {
            cout << "Connect is ok" << endl;
            cout << ntohs(from.sin_port) << '\n' << ntohl(from.sin_addr.s_addr) << endl;
        }
        char buf[] = "First SiT laba";
        int sz = send(s1, buf, sizeof(buf), 0);
        char* buf1 = new char[100];
        int sz_r = recv(s1, buf1, 100, 0);
        cout << buf1 << ' ' << sz_r << endl;
        closesocket(s1);
    }
}