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
    err = connect(s, (LPSOCKADDR)&sin, sizeof(sin));
    char* buf1 = new char[100];
    int sz_r = recv(s, buf1, 100, 0);
    cout << buf1 << endl;
    char buf[] = "First SiT laba";
    int sz = send(s, buf, sizeof(buf), 0);
    closesocket(s);
}