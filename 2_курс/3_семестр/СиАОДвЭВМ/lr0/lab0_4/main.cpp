#include <iostream>
#include <fstream>


int main(int argc, char** argv)
{
    setlocale(LC_ALL, "rus"); // корректное отображение Кириллицы
    int x;
    double division = 1;
    std::ifstream fin("inputDATA.txt"); //открыли файл для чтения

    if (!fin.is_open()) // если файл не открыт
        std::cout << "Файл не может быть открыт!\n"; // сообщить об этом
    else
    {
        fin >> x;
        std::cout << x << " ";
        division = x;
        while(!fin.eof())
        {
            fin >> x;
            std::cout << x << " ";
            division /= x;
        }
        fin.close(); // закрываем файл
        std::cout << std::endl << division << std::endl;
    }
    std::ofstream fout("outputDATA.txt"); //открыли файл для записи результата
    if (!fout.is_open()) // если файл не открыт
        std::cout << "Файл не может быть открыт!\n"; // сообщить об этом
    else
    {
         fout << division;
         fout.close(); // закрываем файл
    }

    system("pause");

    return 0;
}
