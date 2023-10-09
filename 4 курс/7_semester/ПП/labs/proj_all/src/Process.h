#pragma once
#include "mpi.h"
#include "Communicator.h"

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