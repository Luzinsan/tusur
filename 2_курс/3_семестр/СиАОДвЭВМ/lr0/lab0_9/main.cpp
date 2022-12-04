#include <iostream>
#include <fstream>


int main(int argc, char** argv)
{
    setlocale(LC_ALL, "rus"); // корректное отображение Кириллицы
    int x;
    std::ifstream fin("inputDATA.txt"); //открыли файл для чтения
    std::ofstream fout("outputDATA.txt"); //открыли файл для записи результата


    if (!fin.is_open() && !fout.is_open()) // если файлы не открыты
        std::cout << "Входной или выходной файлы не могут быть открыты!\n"; // сообщить об этом
    else
    {
        while(!fin.eof())
        {
            fin >> x;
            if(x % 2 == 0)
            {
                std::cout << x << " - evennumber\n";
                fout      << x << " - evennumber\n";
            }
            else
            {
                std::cout << x << " - oddnumber\n";
                fout      << x << " - oddnumber\n";
            }
        }
        fin.close(); // закрываем входной файл
        fout.close(); // закрываем выходной файл
    }

    system("pause");
    return 0;
}
