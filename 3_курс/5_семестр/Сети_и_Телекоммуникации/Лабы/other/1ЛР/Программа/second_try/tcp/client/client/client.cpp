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
	sin.sin_addr.S_un.S_addr = inet_addr("192.168.1.22");
	sin.sin_family = AF_INET;
	sin.sin_port = htons(80);

	SOCKET s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); //сокет клиента

	err = connect(s, (LPSOCKADDR)&sin, sizeof(sin));
	if (err != 0) return 1;
	else
	{
		std::cout << "Connected!\n";
		char buff[256];
		recv(s, buff, sizeof(buff), 0);
		std::cout << buff << std::endl;
		system("pause");
	}

	return 0;
}