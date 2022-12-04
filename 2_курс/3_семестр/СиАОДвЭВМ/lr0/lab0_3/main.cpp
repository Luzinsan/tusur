#include <iostream>
#include <fstream>


int main(int argc, char** argv)
{
    setlocale(LC_ALL, "rus"); // корректное отображение Кириллицы
    int x, multiplication = 1;
    std::ifstream fin("inputDATA.txt"); //открыли файл для чтения

    if (!fin.is_open()) // если файл не открыт
        std::cout << "Файл не может быть открыт!\n"; // сообщить об этом
    else
    {
        while(!fin.eof())
        {
            fin >> x;
            std::cout << x << " ";
            multiplication *= x;
        }
        fin.close(); // закрываем файл
        std::cout << std::endl << multiplication << std::endl;
    }
    std::ofstream fout("outputDATA.txt"); //открыли файл для записи результата
    if (!fout.is_open()) // если файл не открыт
        std::cout << "Файл не может быть открыт!\n"; // сообщить об этом
    else
    {
         fout << multiplication;
         fout.close(); // закрываем файл
    }

    system("pause");

    return 0;
}
