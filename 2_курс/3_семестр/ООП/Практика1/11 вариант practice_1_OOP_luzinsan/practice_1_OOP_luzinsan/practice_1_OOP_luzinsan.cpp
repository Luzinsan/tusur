#include <iostream>
#include "Data.h"

//Вариант 11

/*
* 11)	Класс инкапсулирует дату (в виде номера дня, месяца и года – D, M, Y). 
* Определить операции сравнения дат (<, >), 
* а также увеличения и уменьшения даты на целое количество дней (+=, –=).
*/

using namespace luzinsan;

int main()
{
    setlocale(LC_ALL, "Rus");
    std::cout << "Вызов конструктора по умолчанию с уведомляющим сообщением." << std::endl;
    Data data30; 
    std::cout << "Тестирование сеттера с тремя параметрами: 30,9,2021." << std::endl;
    data30.SetData(30,9,2021);
    std::cout << "Тестирование геттеров." << std::endl;
    std::cout << "День: " << data30.GetDay() << "\nМесяц: " << data30.GetMonth() << "\nГод: " << data30.GetYear() << std::endl;
     
    std::cout<< "Создание объекта через копирующий конструктор." << std::endl;
    Data data(data30); 
    std::cout << "Тестирование перегрузки оператора вывода '<<' для объектов класса Data." << std::endl;
    std::cout << data;

    std::cout << "Тестирование сеттеров по отдельным параметрам." << std::endl;
    int temp;
    std::cout << "\nВведите день: " << std::endl;
    std::cin >> temp;
    data.SetDay(temp);
    std::cout << "\nВведите месяц: " << std::endl;
    std::cin >> temp;
    data.SetMonth(temp);
    std::cout << "\nВведите год: " << std::endl;
    std::cin >> temp;
    data.SetYear(temp);

    std::cout << data;

    std::cout << "Тестирование перегрузки оператора присваивания '='" << std::endl;
    data30 = data;
    std::cout << data30;
    std::cout << "Введите, сколько дней прибавить к текущей дате: " << std::endl;
    std::cin >> temp;
    
    data += temp;
    std::cout << "Сработала перегрузка оператора '+='\n"
        << "Результат: ";
    std::cout << data;
    data -= temp;
    std::cout << "Сработала перегрузка оператора '-='\n"
        << "Результат: ";
    std::cout << data << std::endl;

    data += temp;
    std::cout << "Сравним даты:" << data << " и " << data30 << std::endl;
    std::cout << "Тестирование логического оператора '>': объект " << data << " > " << data30 << " = " << std::boolalpha << (data > data30) << std::endl;
    std::cout << "Тестирование логического оператора '<': объект " << data << " < " << data30 << " = " << std::boolalpha << (data < data30) << std::endl;
    return 0;
}

