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
	sin.sin_port = htons(80);

	//сокет сервера
	SOCKET s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

	//подключение сокета к коммуникационной среде
	if (bind(s, (LPSOCKADDR)&sin, sizeof(sin)) != 0) return 2;

	//связь с клиентом

	err = listen(s, SOMAXCONN); //поиск
	if (err != 0) return 3;

	SOCKADDR_IN from; //парраметры сокета клиента
	int fromLength = sizeof(from);

	SOCKET s1; //сокет клиент

	s1 = accept(s, (LPSOCKADDR)&from, &fromLength); //извлечение клиента из очереди
	if (s1 == 0) return 4;
	else
	{
		char buff[] = "Hello, client!";
		send(s1, buff, sizeof(buff), 0); //сообщение клиенту
		closesocket(s1); //разрываем соединение
	}

	system("pause");
	return 0;
}