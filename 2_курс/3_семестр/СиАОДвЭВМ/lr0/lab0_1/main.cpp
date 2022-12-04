#include <iostream>
#include <fstream>


int main(int argc, char** argv)
{
    setlocale(LC_ALL, "rus"); // корректное отображение Кириллицы
    int x, sum = 0;
    std::ifstream fin("inputDATA.txt"); //открыли файл для чтения

    if (!fin.is_open()) // если файл не открыт
        std::cout << "Файл не может быть открыт!\n"; // сообщить об этом
    else
    {
        while(!fin.eof())
        {
            fin >> x;
            std::cout << x << " ";
            sum += x;
        }
        fin.close(); // закрываем файл
        std::cout << std::endl << sum << std::endl;
    }
    std::ofstream fout("outputDATA.txt"); //открыли файл для записи результата
    if (!fout.is_open()) // если файл не открыт
        std::cout << "Файл не может быть открыт!\n"; // сообщить об этом
    else
    {
         fout << sum;
         fout.close(); // закрываем файл
    }

    system("pause");

    return 0;
}
