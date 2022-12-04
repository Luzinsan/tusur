#include <iostream>
constexpr int MAX_BITS = 8;


void binary(unsigned char* ptr, int bytes)
{
	
	for(int i = bytes - 1; i >= 0; --i)
	{
		for (int j = MAX_BITS - 1; j >= 0; --j)
			// Смотрим на двоичное представление: 
			// выбираем i-й байт числа (отсчёт идёт с самого правого(младшего) байта)(теперь указываем на самый левый бит этого байта); 
		    // сдвигаем число на j бит вправо (интересующий бит для вывода теперь находится в самой правой ячейке) и делением по модулю на 2 получаем этот бит 
			// например число: 8589 = 0010'0001 0110'0010 
			// 4 байта по 8 бит                           =>          0010'0001              ptr->0.110'0010
			// ptr[1]                                     =>  ptr[1]->0010'0001                   (0110'0010)
			// (ptr[1] >> 7) = (сместить вправо на 7 бит) =>                  0/010'0001          (0110'0010)
			// (ptr[1] >> 6) = (сместить вправо на 6 бит) =>                 00/10'0001           (0110'0010)
			// (ptr[1] >> 5) = (сместить вправо на 5 бит) =>                001/0'0001            (0110'0010)
			// (ptr[1] >> 4) = (сместить вправо на 4 бит) =>               0010/'0001             (0110'0010)
			// (ptr[1] >> 3) = (сместить вправо на 3 бит) =>              00100/001               (0110'0010)
			// (ptr[1] >> 2) = (сместить вправо на 2 бит) =>             001000/01                (0110'0010)
			// (ptr[1] >> 1) = (сместить вправо на 1 бит) =>            0010000/1                 (0110'0010)
			// (ptr[1] >> 0) = (сместить вправо на 0 бит) =>           00100001/                  (0110'0010)
			

			std::cout << (ptr[i] >> j) % 2; 
		std::cout << " ";
	}
	std::cout << std::endl;
}

int main()
{
	signed int si = -2'147'483'647;
	unsigned int u = 8589;

	char c = -128;
	unsigned char uc = 255;

	short s = -32'768;
	unsigned short us = 65'535;

	long long ll = 9'223'372'036'854'775'808;
	unsigned long long ull = 18'446'744'073'709'551'615;

	float f = 1.512;
	double d = 8.256;

	std::cout << "signed int " << (signed int)si << " = ";
	binary((unsigned char*)&si, sizeof(si));
	std::cout << "unsigned int " << (unsigned int)u << " = ";
	binary((unsigned char*)&u, sizeof(u));
	std::cout << "char " << (short)c << " = ";
	binary((unsigned char*)&c, sizeof(c));
	std::cout << "unsigned char " << (unsigned short)uc << " = ";
	binary((unsigned char*)&uc, sizeof(uc));
	std::cout << "short " << (short)s << " = ";
	binary((unsigned char*)&s, sizeof(s));
	std::cout << "unsigned short " << (unsigned short)us << " = ";
	binary((unsigned char*)&us, sizeof(us));
	std::cout << "long long " << (long long)ll << " = ";
	binary((unsigned char*)&ll, sizeof(ll));
	std::cout << "unsigned long long " << (unsigned long long)ull << " = ";
	binary((unsigned char*)&ull, sizeof(ull));
	std::cout << "float " << (float)f << " = ";
	binary((unsigned char*)&f, sizeof(f));
	std::cout << "double " << (double)d << " = ";
	binary((unsigned char*)&d, sizeof(d));

	return 0;
}
