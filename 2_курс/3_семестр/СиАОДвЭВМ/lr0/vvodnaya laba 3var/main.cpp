#include <iostream>
#include <fstream>

// 3 ВАРИАНТ
//Входной файл содержит 15 целых чисел. Программа должна считать
//файл и выполнить операцию умножения. Выходной файл должен
//содержать одно число – результат умножения.

using namespace std;

void proizv()
{
    ifstream FILE_input("in.txt");
    ofstream FILE_output("out.txt");
    int a = 0;
    int b = 1;
    int c = 0;
    FILE_input >> a;
    for (int i = 1; i <= 15; i++)
    {

        FILE_input >> a;
        b=a*b;
        c+=b;

    }
        FILE_output << b;

    FILE_input.close();
    FILE_output.close();

}
int main()
{
    proizv();
}
