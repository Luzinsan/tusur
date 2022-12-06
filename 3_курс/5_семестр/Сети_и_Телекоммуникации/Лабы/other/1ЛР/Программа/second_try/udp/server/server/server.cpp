#include <WinSock2.h>
#include <iostream>

int main()
{
	//загрузка библиотеки
	WSADATA wsaData;
	int err = WSAStartup(0x0101, &wsaData);
	if (err == SOCKET_ERROR) return 1;

	//параметры сокета сервера
	SOCKADDR_IN sin;
	sin.sin_addr.s_addr = INADDR_ANY;
	sin.sin_family = AF_INET;
	sin.sin_port = htons(8500);

	//сокет сервера
	SOCKET s = socket(AF_INET, SOCK_DGRAM, 0);

	//подключение сокета к коммуникационной среде
	if (bind(s, (LPSOCKADDR)&sin, sizeof(sin)) != 0) return 2;

	SOCKADDR_IN sfrom;
	int sfromLenght = sizeof(sfrom);

	char buff[256];
	recvfrom(s, buff, sizeof(buff), 0, (LPSOCKADDR)&sfrom, &sfromLenght); //сообщение от клиента
	std::cout << buff;

	closesocket(s); //разрываем соединение

	system("pause");
	return 0;
}