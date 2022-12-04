#include <iostream>
#include <fstream>


int main(int argc, char** argv)
{
    setlocale(LC_ALL, "rus"); // корректное отображение Кириллицы
    int toSubtraction, start;
    std::ifstream fin("inputDATA.txt"); //открыли файл для чтения
    std::ofstream fout("outputDATA.txt"); //открыли файл для записи результата


    if (!fin.is_open() && !fout.is_open()) // если файлы не открыты
        std::cout << "Входной или выходной файлы не могут быть открыты!\n"; // сообщить об этом
    else
    {
        fin >> start;
        std::cout << start << std::endl;
        while(!fin.eof())
        {
            fin >> toSubtraction;
            std::cout << toSubtraction << " ";
            fout << start-toSubtraction << " ";
        }
        fin.close(); // закрываем входной файл
        fout.close(); // закрываем выходной файл
    }

    system("pause");
    return 0;
}
