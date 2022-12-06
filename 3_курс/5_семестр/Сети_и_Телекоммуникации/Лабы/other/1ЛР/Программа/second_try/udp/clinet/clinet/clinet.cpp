#include <WinSock2.h>
#include <iostream>

#pragma warning(disable : 4996)

int main()
{
	//загрузка библиотеки
	WSADATA wsaData;
	int err = WSAStartup(0x0101, &wsaData);
	if (err == SOCKET_ERROR) return 1;

	//параметры сокета сервера
	SOCKADDR_IN sin;
	sin.sin_addr.S_un.S_addr = inet_addr("192.168.43.66");
	sin.sin_family = AF_INET;
	sin.sin_port = htons(8500);

	SOCKET s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP); //сокет клиента

	char buff[256] = "Hello, server!";
	sendto(s, buff, sizeof(buff), 0, (LPSOCKADDR)&sin, sizeof(sin));
	system("pause");

	return 0;
}