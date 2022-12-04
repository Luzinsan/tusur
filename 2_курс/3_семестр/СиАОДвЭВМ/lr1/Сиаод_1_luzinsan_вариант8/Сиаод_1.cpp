#include <iostream>
#include <fstream>

#define MAX_SIZE_STACK 100
/**
8. Используя стек, решить следующую задачу.
В текстовом файле F записана без ошибок формула следующего вида:
<формула> ::= <цифра> | М(<формула>, <формула>) | m(<формула>, <формула>)
<цифра> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9,
где М обозначает функцию max, а m - min. Вычислить как целое число значение данной формулы.
Например, М(M(4,5),m(6,M(8,3))).
Для реализации АТД Стек использовать массив.
*/

int Stack[MAX_SIZE_STACK];
int t;
void init(); // инициализация стека
void Push(int); // положить в стек
int Pop(); // забрать из стека
int Top(); // получить значение верхнего элемента стека
bool IsEmpty(); // проверить, является ли стек пустым

void M(std::ifstream& fin);
void m(std::ifstream& fin);



void m(std::ifstream& fin)
{
    while (!fin.eof())
    {
        char k; int a, b;
        fin >> k;
        switch (k)
        {
        case 'M':
            M(fin);
            break;
        case 'm':
            m(fin);
            break;
        case '0':case '1':case '2':case '3':case '4':case '5':case '6':case '7':case '8':case '9':  Push(k - '0'); break;
        case ')':  a = Pop(); b = Pop(); Push(a < b ? a : b); return;
        }
    }
}

void M(std::ifstream& fin)
{
    while (!fin.eof())
    {
        char k; int a, b;
        fin >> k;
        switch (k)
        {
        case 'M':
            M(fin);
            break;
        case 'm':
            m(fin);
            break;
        case '0':case '1':case '2':case '3':case '4':case '5':case '6':case '7':case '8':case '9':  Push(k - '0'); break;
        case ')':  a = Pop(); b = Pop(); Push(a > b ? a : b); return;
        }
    }
}

int main()
{
    std::ifstream fin("F.txt"); //открыли файл для чтения
   
    if (!fin.is_open()) // если входной файл не открыт
        std::cout << "Входной файл не может быть открыт!\n"; // сообщить об этом
    else
    {
        char k;
        init(); // инициализация стека
        fin >> k;
        switch (k)
        {
        case 'M':
            M(fin);
            break;
        case 'm':
            m(fin);
            break;
        }
        std::ofstream fout("outputDATA.txt"); //открыли файл для записи
        if (!fout.is_open()) // если выходной файл не открыт
            std::cout << "Выходной файл не может быть открыт!\n"; // сообщить об этом
        else
        {
            fout << Pop();
            fout.close(); // закрываем выходной файл
        }
        fin.close(); // закрываем входной файл
    }
    
    return 0;
}


void init() { t = -1; }// инициализация стека
void Push(int a) // положить в стек
{
    if (t == MAX_SIZE_STACK) // проверка на попытку занесения элемента в полный стек
    {
        std::cout << "Попытка занесения значения в полный стек";
        exit(EXIT_FAILURE);
    }
    else Stack[++t] = a;
}
int Pop() // забрать из стека
{
    if (t == -1) // проверка на попытку забрать элемент из пустого стека
    {
        printf("Попытка чтения из пустого стека");
        exit(EXIT_FAILURE);
    }
    else return(Stack[t--]);
}
int Top() { if (!IsEmpty()) return(Stack[t]); else return EOF; } // получить значение верхнего элемента стека
bool IsEmpty() { return(t == -1); } // проверить, является ли стек пустым
