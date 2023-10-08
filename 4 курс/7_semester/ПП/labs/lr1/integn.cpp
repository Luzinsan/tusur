#include "mpi.h"
#include <cstdio>
#include <math.h>
#include <iostream>
#include <cassert>
#include <fstream>
#include <sstream>
#include <stdio.h>
#include <stdarg.h>

static double f(double a, double c = 0.9);
static double fi(double a, double c = 0.9);

/**
 * @brief Класс коммуникатора, содержащий информацию о коммуникаторе, 
 * количеству запущенных процессов,
 * имени хоста.
 */
class Communicator
{
protected:
    MPI_Comm comm;
    int numprocs;
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int namelen;

protected:
    /**
     * @brief Конструктор коммуникатора
     * 
     * @param argc
     * @param argv 
     * @param _comm Инициализируемый коммуникатор 
     */
    Communicator(int argc, char *argv[], MPI_Comm _comm = MPI_COMM_WORLD)
    {
        int error;
        if (error = MPI_Init(&argc, &argv))
            throw error;

        comm = _comm;
        MPI_Comm_size(comm, &numprocs);
        MPI_Get_processor_name(processor_name, &namelen);
    }

    virtual void printInfo(std::string accompanying_message = "", std::ostream &out = std::cout)
    {
        out << "\n\tProcessor name: " << processor_name
            << "\n\tNumber of processes: " << numprocs
            << "\n\t" << accompanying_message;
        fflush(NULL);
    }

    ~Communicator() { MPI_Finalize(); }
};


class Process : public Communicator
{
protected:
    int PID;
    enum PIDs
    {
        INIT
    };

public:
    int getPID() { return PID; }

public:
    /**
     * @brief Конструктор процесса 
     * для инициализации родительского класса - коммуникатора 
     * 
     * @param argc
     * @param argv 
     * @param _comm Инициализируемый коммуникатор 
     */
    Process(int argc, char *argv[], MPI_Comm _comm = MPI_COMM_WORLD)
        : Communicator(argc, argv, _comm)
    {
        MPI_Comm_rank(_comm, &PID);
    }

    void printInfo(std::string accompanying_message = "", std::ostream &out = std::cout)
    {
        out << "\n"
            << PID << ": " << accompanying_message;
        fflush(NULL);
    }

    /**
     * @brief Метод передачи сообщения: в стандартном режиме (неблокирующий)
     * 
     * Метод выполняет посылку count_data элементов типа type сообщения buffer
     * с идентификатором tag процессу to_PID в области связи коммуникатора comm. 
     * Переменная buffer - это, как правило, массив или скалярная переменная. 
     * В последнем случае значение count = 1.
     * 
     * @param buffer адрес отправляемого буфера памяти
     * @param to_PID ранг процесса, которому пересылается сообщение
     * @param type тип данных пересылаемых сообщений
     * @param count_data количество элементов памяти типа type
     * @param tag идентификатор отправляемого сообщения: целое число от 0 до 32767 
     * - определяет смысл отправляемого сообщения.
     * - Сообщения, пришедшие в неизвестном порядке, 
     * могут извлекаться из общего входного потока в нужном алгоритму порядке.
     */
    void send(void *buffer, int to_PID,
              MPI_Datatype type = MPI_INT, int count_data = 1,
              int tag = 1)
    {
        MPI_Send(buffer,
                 count_data,
                 type,
                 to_PID,
                 tag,
                 comm);
    }

    /**
     * @brief Метод приёма сообщения: блокирующий
     * 
     * Метод выполняет прием count_data элементов типа type сообщения  buffer
     * с идентификатором tag от процесса from_PID в области связи коммуникатора comm.
     * 
     * @param buffer адрес заполняемого буфера памяти
     * @param from_PID ранг процесса, от которого ожидать сообщение
     * @param type тип данных принимаемого сообщений
     * @param count_data _максимальное_ количество элементов памяти типа type
     * @param tag идентификатор принимаемого сообщения: целое число от 0 до 32767 
     * - определяет смысл принятого сообщения.
     * - Сообщения, пришедшие в неизвестном порядке, 
     * могут извлекаться из общего входного потока в нужном алгоритму порядке.
     * @return status MPI_Status получения сообщения
     */
    MPI_Status receive(void *buffer, int from_PID,
                       MPI_Datatype type = MPI_INT, int count_data = 1,
                       int tag = 1)
    {
        MPI_Status status;
        MPI_Recv(buffer,
                 count_data,
                 type,
                 from_PID,
                 tag,
                 comm,
                 &status);
        return status;
    }

    /**
     * @brief Широковещательная рассылка 
     * - Коллективная операция 
     * - передача данных от одного процесса всем процессам программы
     * - должен быть осуществлен всеми процессами указываемого коммуникатора
     * 
     * Метод осуществляет рассылку данных из буфера buffer, 
     * содержащего count_data элементов типа type  с процесса, 
     * имеющего номер root, всем процессам, входящим в коммуникатор comm
     * 
     * Указываемый буфер памяти имеет различное назначение в разных процессах:
     * - Для процесса с рангом root, 
     * с которого осуществляется рассылка данных, 
     * в этом буфере должно находиться рассылаемое сообщение
     * - Для всех остальных процессов указываемый буфер предназначен 
     * для приема передаваемых данных.
     * 
     * @param buffer буфер памяти с отправляемым
         сообщением (для процесса с рангом 0), и для
         приема сообщений для всех остальных процессов
     * @param type тип данных пересылаемого/принимаемого сообщения
     * @param count_data количество элементов памяти типа type
     * @param root ранг процесса, выполняющего рассылку данных
     */
    void broadcast(void *buffer, MPI_Datatype type = MPI_INT,
                   int count_data = 1,
                   int root = Process::INIT)
    {
        MPI_Bcast(buffer,
                  count_data,
                  type,
                  root,
                  comm);
    }

    /**
     * @brief Коллективная операция передачи данных от всех процессов одному процессу.
     * Вызывается на всех процессах.
     * 
     * Метод объединяет элементы входного буфера длиной count_data 
     * каждого процесса в группе, используя операцию _operator, 
     * и возвращает объединенное значение 
     * в выходной буфер процесса с номером root..
     * 
     * @param sendbuf буфер памяти с отправляемым сообщением 
     * (все процессы в коммутаторе, кроме root)
     * @param recvbuf буфер памяти для результирующего сообщения 
     * (только для процесса с рангом root)
     * @param type тип данных элементов сообщения
     * @param root ранг
     * @param _operator операция редукции: 
     * - MPI_MAX -- определение максимального значения,
     * - MPI_MIN -- определение минимального значения,
     * - MPI_SUM -- определение суммы значений,
     * - MPI_PROD -- определение произведения значений,
     * - MPI_LAND -- выполнение логической операции "И" над значениями сообщений,
     * - MPI_BAND -- выполнение битовой операции "И" над значениями сообщений,
     * - MPI_LOR -- выполнение логической операции "ИЛИ" над значениями сообщений,
     * - MPI_BOR -- выполнение битовой операции "ИЛИ" над значениями сообщений,
     * - MPI_LXOR -- выполнение логической операции исключающего "ИЛИ" над значениями сообщений,
     * - MPI_BXOR -- выполнение битовой операции исключающего "ИЛИ" над значениями сообщений,
     * - MPI_MAXLOC -- определение максимальных значений и их индексов,
     * - MPI_MINLOC -- определение минимальных значений и их индексов.
     * @param count_data количество элементов в бефере с отправляемым сообщением
     */
    void reduce(void *sendbuf, void *recvbuf,
                MPI_Datatype type = MPI_INT,
                int root = Process::INIT,
                MPI_Op _operator = MPI_SUM,
                int count_data = 1)
    {
        MPI_Reduce(sendbuf,
                   recvbuf,
                   count_data,
                   type,
                   _operator,
                   root,
                   comm);
    }

    /**
     * @brief  Запаковка сообщения из буфера data, длиной count_data типа данных type
    в буферное пространство, описанное аргументами buf и count_buf (в байтах). 

    Параметр position определяет номер ячейки в выходном буфере, с которого будет заполняться buf.
    После заполнения значение position инкрементируется в количестве заполненных байтов. 
     * 
     * @param data буфер памяти с сообщением для запаковки
     * @param count_data количество значений этого буфера типа type
     * @param buf буфер памяти для запакованных значений
     * @param count_buf общее количество байтов этого буфера
     * @param type MPI_Datatype (тип) данных пакуемого сообщения
     * @param bufpos позиция в выходном буфере, с которого необходимо начать заполнение
     */
    void pack(void *data, int count_data,
              void *buf, int count_buf,
              MPI_Datatype type = MPI_INT,
              int *bufpos = NULL)
    {
        MPI_Pack(data,
                 count_data,
                 type,
                 buf,
                 count_buf,
                 bufpos,
                 comm);
    }

    /**
     * @brief Метод запаковки переменного количества сообщений
     * 
     * @param lenBytes количество байт выходного буфера
     * @param szTypes строка, определяющая количество запакованных переменных и их типы данных: 
     * - i -- int,
     * - f -- float,
     * - d -- double,
     * - c -- char,
     * - s -- char* (std::string).
     * @param ... передача переменного количества пакуемых переменных
     * @return char* выходной буфер
     */
    char *multiplePack(int lenBytes,
                       std::string szTypes, ...)
    {
        va_list vl;
        va_start(vl, szTypes);
        char *buf = (char *)malloc(lenBytes);
        int buffpos = 0;

        for (int i = 0; szTypes[i] != '\0'; ++i)
        {
            union Printable_t
            {
                int i;
                float f;
                double d;
                char c;
                char *s;
            } Printable;
            switch (szTypes[i])
            { // Type to expect.
            case 'i':
                Printable.i = va_arg(vl, int);
                pack(&Printable.i, 1, buf, lenBytes, MPI_INT, &buffpos);
                break;
            case 'f':
                Printable.f = va_arg(vl, double);
                pack(&Printable.f, 1, buf, lenBytes, MPI_FLOAT, &buffpos);
                break;
            case 'd':
                Printable.d = va_arg(vl, double);
                pack(&Printable.d, 1, buf, lenBytes, MPI_DOUBLE, &buffpos);
                break;
            case 'c':
                Printable.c = va_arg(vl, int);
                pack(&Printable.c, 1, buf, lenBytes, MPI_CHAR, &buffpos);
                break;
            case 's':
                Printable.s = va_arg(vl, char *);
                pack(&Printable.s, 1, buf, lenBytes, MPI_CHAR, &buffpos);
                break;
            default:
                break;
            }
        }
        va_end(vl);
        return buf;
    }

    /**
     * @brief Распаковка сообщений
     * Метод распаковывает сообщение в приемный буфер, описанный аргументами outbuf, outcount, type 
     * из буферного пространства, описанного аргументами inbuf и insize. 
     * Выходным буфером может быть любой коммуникационный буфер, разрешенный в MPI_RECV. 
     * Входной буфер есть смежная область памяти, содержащая insize байтов, начиная с адреса inbuf. 
     * Входное значение position есть первая ячейка во входном буфере, занятом упакованным сообщением. 
     * рosition инкрементируется размером упакованного сообщения, 
     * так что выходное значение рosition есть первая ячейка во входном буфере после ячеек, 
     * занятых сообщением, которое было упаковано. 
     * сomm есть коммуникатор для приема упакованного сообщения. 
     * 
     * @param inbuf буфер, из которого будет распаковываться сообщение
     * @param insize размер этого буфера в байтах
     * @param outbuf буфер, куда будет распаковываться сообщение
     * @param bufpos позиция во входном буфере, указывающая откуда распаковывать сообщение
     * @param type тип данных распаковываемого сообщения
     * @param outcount число единиц распаковываемого сообщения типа type
     */
    void unpuck(void *inbuf, int insize,
                void *outbuf,
                int *bufpos,
                MPI_Datatype type = MPI_INT,
                int outcount = 1)
    {
        MPI_Unpack(inbuf,
                   insize,
                   bufpos,
                   outbuf,
                   outcount,
                   type,
                   comm);
    }
};

#pragma region lab1

/*!
	@brief Класс, подсчитывающий интегральную сумму методом прямоугольника.
    Точность задаётся количеством разбиений интервала определённого интеграла - n
*/
class Integral : public Process
{
private:
    int intervals = 0;
    double xl = -0.2, // low  bordert
        xh = 1.0;     // high border
    double c = 0.9;
    double step;
    double sum = 0.0;
    double startwtime, endwtime;
    std::ofstream fout;

public:
    Integral(int argc, char *argv[], MPI_Comm comm = MPI_COMM_WORLD,
             std::string filename = "output.txt")
        : Process(argc, argv, comm)
    {
        fflush(NULL);
        fout.open(filename, std::ios::out);
        fflush(NULL);
    }
    ~Integral() { fout.close(); }

    void printInfo(std::string accompanying_message = "", std::ostream &out = std::cout)
    {
        out << "\nNumber of intervals: " << intervals
            << "\nLow border: " << xl
            << "\nHight border: " << xh
            << "\nParameter: " << c
            << "\n"
            << accompanying_message;
        fflush(NULL);
    }

    void unpuckParams(void *buf)
    {
        int length = sizeof(int) + sizeof(double) * 3 + 100;
        int bufpos = 0;
        unpuck(buf, length, &intervals, &bufpos);
        unpuck(buf, length, &xl, &bufpos, MPI_DOUBLE);
        unpuck(buf, length, &xh, &bufpos, MPI_DOUBLE);
        unpuck(buf, length, &c, &bufpos, MPI_DOUBLE);
    }

    int getIntervals()
    {
        int len_buf = sizeof(int) + sizeof(double) * 3 + 100;
        char *buf;
        if (PID == Process::INIT)
        {
            std::cout << "\nEnter the number of intervals (0 quit): ";
            fflush(NULL);
            int n;
            std::cin >> n;
            fflush(stdin);
            intervals = n;
            if (n != 0)
            {
                double temp;
                std::cout << "Enter the low border: ";
                fflush(NULL);
                std::cin >> temp;
                fflush(stdin);
                xl = temp;
                std::cout << "Enter the hight border: ";
                fflush(NULL);
                std::cin >> temp;
                fflush(stdin);
                xh = temp;
                std::cout << "Enter the parameter of function: ";
                fflush(NULL);
                std::cin >> temp;
                fflush(stdin);
                c = temp;
            }
            else
                xl, xh, c = 0, 0, 0;
            buf = multiplePack(len_buf,
                               "iddd", intervals, xl, xh, c);
            startwtime = MPI_Wtime();
        }
        else
            buf = new char[len_buf];
        broadcast(buf, MPI_PACKED, len_buf);
        if (PID != Process::INIT)
        {
            unpuckParams(buf);
            if (intervals == 0)
                return 0;
        }
        delete[] buf;
        return intervals;
    }

    /**
     * @brief Подсчёт интегральной суммы на изолированном отрезке
     * 
     * @return double интегральная сумма
     */
    double evalIntegral()
    {
        step = (xh - xl) / static_cast<double>(intervals);
        for (int i = PID + 1; i <= intervals; i += numprocs)
        {
            double x = xl + step * ((double)i - 0.5);
            sum += f(x, c);
        }
        sum *= step;
        std::stringstream str;
        str << std::scientific << "SUMM: " << sum;
        Process::printInfo(str.str());
        fflush(NULL);
        str.clear();
        str.str("");
        return sum;
    }

    /**
     * @brief Суммирование результатов со всех процессов
     * 
     * @return double итоговая интегральная сумма
     */
    double summarazing()
    {
        double integral = 0;
        reduce(&sum, &integral, MPI_DOUBLE);

        endwtime = MPI_Wtime();

        if (PID == Process::INIT)
        {
            Communicator::printInfo("", fout);
            printInfo("", fout);
            std::stringstream str;
            str << std::scientific << "Integral is approximately: " << integral;
            Process::printInfo(str.str(), fout);
            fflush(NULL);
            str.clear();
            str.str("");
            str << std::scientific << "Error: " << integral - fi(xh, c) + fi(xl, c);
            Process::printInfo(str.str(), fout);
            fflush(NULL);
            str.clear();
            str.str("");
            str << std::scientific << "Time of calculation: " << endwtime - startwtime;
            Process::printInfo(str.str(), fout);
            fflush(NULL);
            str.clear();
            str.str("");
            return integral;
        }
        else
            return sum;
    }

    /**
     * @brief Вычисление значения подынтегральной функции: 
     * @f$f(x) = \frac{1}{1+(c*a)^2}@f$
     * 
     * @param a абсцисса для вычисления значения в точке x
     * @param c параметр подынтегрального выражения
     * @return double вычисленная ордината
     */
    static double f(double a, double c)
    {
        return 1 / (1 + pow(c * a, 2));
    }

    /**
     * @brief Вычисление значения первообразной функции: 
     * @f$F(x) = \frac{1}{c} * \arctan(c*a)@f$
     * 
     * @param a абсцисса для вычисления значения в точке x
     * @param c параметр первообразной функции
     * @return double вычисленная ордината
     */
    static double fi(double a, double c)
    {
        return (1 / c) * atan(c * a);
    }
};



void lab1(int argc, char *argv[])
{
    Integral proc(argc, argv);
    while (true)
    {
        int success = proc.getIntervals();
        if (!success)
            break;
        else
        {
            proc.evalIntegral();
            proc.summarazing();
        }
    }
}

#pragma endregion

int main(int argc, char *argv[])
{
    lab1(argc, argv);
    return 0;
}

// int lenBytes(std::string szTypes, ...)
// {
//     va_list vl;
//     va_start( vl, szTypes );
//     int length = 0;
//     for(int i = 0; szTypes[i] != '\0'; ++i)
//     {
//         union Printable_t
//         {
//             int     i;
//             float   f;
//             char    c;
//             char   *s;
//         } Printable;
//         switch(szTypes[i])
//         {   // Type to expect.
//             case 'i':{
//                 Printable.i = va_arg( vl, int );
//                 length += sizeof(int);
//                 break;
//             }case 'f':{
//                 Printable.f = va_arg( vl, double );
//                 length += sizeof(double);
//                 break;
//             }case 'c':{
//                 Printable.c = va_arg( vl, int );
//                 length += sizeof(char);
//                 break;
//             }case 's':{
//                 Printable.s = va_arg( vl, char *);
//                 length += sizeof(char) * strlen(Printable.s);
//                 break;
//             }default:
//                 break;
//         }
//     }
//     return length;
// }
