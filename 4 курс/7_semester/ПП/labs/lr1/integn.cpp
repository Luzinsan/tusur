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
 

class Communicator
{
protected:
    int numprocs;
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int  namelen;
protected:
    Communicator(int argc, char *argv[], MPI_Comm comm)
    {
        int error;
        if(error = MPI_Init(&argc, &argv))
            std::cerr << error;            

        MPI_Comm_size(comm, &numprocs);
        MPI_Get_processor_name(processor_name, &namelen);
    }

    virtual void printInfo(std::string accompanying_message="", std::ostream &out=std::cout)
    {
        out << "\n\t\t\tProcessor name: " << processor_name
            << "\n\t\t\tNumber of processes: " << numprocs
            << "\n\t\t\t" << accompanying_message; fflush(NULL);
    }

    ~Communicator(){ MPI_Finalize(); }
};


class Process: public Communicator
{
protected:
    int PID;
    enum PIDs
        {  INIT  };
public: 
    
    int getPID(){ return PID; }
public:
    Process(int argc, char *argv[], MPI_Comm comm = MPI_COMM_WORLD)
        : Communicator(argc, argv, comm)
    {
        MPI_Comm_rank(comm, &PID);
    }

    void printInfo(std::string accompanying_message="", std::ostream &out=std::cout)
    {
        out << "\n" << PID << ": " << accompanying_message; fflush(NULL);
    }

    void send(void *buffer, int to_PID, 
              MPI_Datatype type=MPI_INT, int count_data=1,  
              int tag = 1, MPI_Comm comm = MPI_COMM_WORLD)
    {
        MPI_Send (buffer,              /* buffer              */
                  count_data,          /* one data            */
                  type,                /* type                */
                  to_PID,              /* to which node       */
                  tag,                 /* number of message   */
                  comm);               /* common communicator */
    }

    MPI_Status receive(void *buffer, int from_PID, 
                      MPI_Datatype type=MPI_INT, int count_data=1, 
                      int tag = 1, MPI_Comm comm = MPI_COMM_WORLD)
    {
        MPI_Status status;
        MPI_Recv (buffer,               /* buffer              */
                  count_data,           /* one data            */
                  type,                 /* type                */
                  from_PID,             /* to which node       */
                  tag,                  /* number of message   */
                  comm,                 /* common communicator */
                  &status);             /* status of errors    */
        return status;
    }

    void broadcast(void *buffer, MPI_Datatype type=MPI_INT,
              int count_data=1,  
              int root=Process::INIT, 
              MPI_Comm comm = MPI_COMM_WORLD)
    {
        MPI_Bcast (buffer,             /* buffer              */
                   count_data,          /* one data            */
                   type,                /* type                */
                   root,                /* to which node       */
                   comm);               /* common communicator */
    }

    void reduce(void *sendbuf, void *recvbuf, 
              MPI_Datatype type=MPI_INT,
              int to_PID=Process::INIT,
              MPI_Op _operator=MPI_SUM, 
              int count_data=1,  
              MPI_Comm comm = MPI_COMM_WORLD)
    {
        MPI_Reduce (sendbuf,             /* buffer              */
                    recvbuf,
                    count_data,          /* one data            */
                    type,                /* type                */
                    _operator,
                    to_PID,            /* to which node       */
                    comm);               /* common communicator */
    }


    void pack(void *data, int count_data, 
              void *buf, int count_buf,
              MPI_Datatype type=MPI_INT,
              int *bufpos = NULL,
              MPI_Comm comm = MPI_COMM_WORLD)
    {
        MPI_Pack   (data,             /* buffer              */
                    count_data,
                    type,          /* one data            */
                    buf,                /* type                */
                    count_buf,
                    bufpos,
                    comm);    
    }


    char* multiplePack(int lenBytes, 
                      MPI_Comm comm, std::string szTypes, ...) 
    {
        va_list vl;
        va_start(vl, szTypes);
        char* buf = (char *)malloc(lenBytes);
        int buffpos = 0;
        
        for(int i = 0; szTypes[i] != '\0'; ++i) 
        {
            union Printable_t 
            {
                int     i;
                float   f;
                double  d;
                char    c;
                char   *s;
            } Printable;
            switch( szTypes[i] ) 
            {   // Type to expect.
                case 'i':
                    Printable.i = va_arg( vl, int );
                    pack(&Printable.i, 1, buf, lenBytes, MPI_INT, &buffpos, comm);
                    break;
                case 'f':
                    Printable.f = va_arg( vl, double );
                    pack(&Printable.f, 1, buf, lenBytes, MPI_FLOAT, &buffpos, comm);
                    break;
                case 'd':
                    Printable.d = va_arg( vl, double );
                    pack(&Printable.d, 1, buf, lenBytes, MPI_DOUBLE, &buffpos, comm);
                    break;
                case 'c':
                    Printable.c = va_arg( vl, int );
                    pack(&Printable.c, 1, buf, lenBytes, MPI_CHAR, &buffpos, comm);
                    break;
                case 's':
                    Printable.s = va_arg( vl, char *);
                    pack(&Printable.s, 1, buf, lenBytes, MPI_CHAR, &buffpos, comm);
                    break;
                default:
                break;
            }
        }
        va_end( vl );
        return buf;
    }

    void unpuck(void *buf, int count_buf, 
                void* unbuf,
                int *bufpos,
                MPI_Datatype type=MPI_INT,
                int count_data=1,
                MPI_Comm comm = MPI_COMM_WORLD)
    {
        MPI_Unpack (buf,             /* buffer              */
                    count_buf,
                    bufpos,          /* one data            */
                    unbuf,                /* type                */
                    count_data,
                    type,
                    comm);  
    }
};




class Integral: public Process
{
private:
    int intervals = 0;
    double xl = -0.2,	// low  bordert
	       xh =  1.0;	// high border
    double c = 0.9;
    double step;
    double sum = 0.0;
    double startwtime, endwtime;
    std::ofstream fout;
public:
    Integral(int argc, char *argv[], int numIntervals): Process(argc, argv) { intervals = numIntervals; }
    Integral(int argc, char *argv[], MPI_Comm comm = MPI_COMM_WORLD,
             std::string filename = "output.txt")
             : Process(argc, argv, comm) 
    {
        fflush(NULL);
        fout.open(filename, std::ios::out);
        fflush(NULL);
    }
    ~Integral(){ fout.close(); }

    void printInfo(std::string accompanying_message="", std::ostream &out=std::cout)
    {
        out << "\nNumber of intervals: " << intervals
            << "\nLow border: " << xl
            << "\nHight border: " << xh 
            << "\nParameter: " << c
            << "\n" << accompanying_message; fflush(NULL);
    }

    void unpuckParams(void* buf)
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
            std::cout << "\nEnter the number of intervals (0 quit): "; fflush(NULL);
            int n;
            std::cin >> n; fflush(stdin);
            intervals = n;
            if (n != 0) 
            {
                double temp;
                std::cout << "Enter the low border: "; fflush(NULL);
                std::cin >> temp; fflush(stdin);
                xl = temp;
                std::cout << "Enter the hight border: "; fflush(NULL);
                std::cin >> temp; fflush(stdin);
                xh = temp;
                std::cout << "Enter the parameter of function: "; fflush(NULL);
                std::cin >> temp; fflush(stdin);
                c = temp;
            }
            else 
                xl, xh, c = 0, 0, 0;
            buf = multiplePack(len_buf, MPI_COMM_WORLD, 
                               "iddd",  intervals, xl, xh, c);
            startwtime = MPI_Wtime();
        }
        else buf = new char[len_buf];
        broadcast(buf, MPI_PACKED, len_buf);
        if (PID != Process::INIT)
        {
            unpuckParams(buf);
            if (intervals==0)
                return 0;
        }
        delete[] buf;
        return intervals;
    }

    /* Calculate of integral  */
    double evalIntegral()
    {
        step  = (xh-xl) / static_cast<double>(intervals);
        for (int i = PID + 1; i <= intervals; i += numprocs)
        {
            double x = xl + step * ((double)i - 0.5);
            sum += f(x, c);
        }
        sum *= step;
        std::stringstream str;
        str << std::scientific << "SUMM: " << sum;
        Process::printInfo(str.str());  fflush(NULL); str.clear(); str.str("");
        return sum;
    }


    double summarazing()
    {
        double integral = 0;
        reduce(&sum, &integral, MPI_DOUBLE);
        
        endwtime = MPI_Wtime();

        if (PID == Process::INIT)
        {
            printInfo("", fout);
            std::stringstream str;
            str << std::scientific << "Integral is approximately: " << integral;
            Process::printInfo(str.str(), fout);  fflush(NULL); str.clear(); str.str("");
            str << std::scientific << "Error: " << integral - fi(xh, c) + fi(xl, c);
            Process::printInfo(str.str(), fout);  fflush(NULL); str.clear(); str.str("");
            str << std::scientific << "Time of calculation: " << endwtime-startwtime;
            Process::printInfo(str.str(), fout);  fflush(NULL); str.clear(); str.str("");
            return integral;
        }
        else return sum;
    }
};




int main(int argc, char *argv[])
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
    return 0;
}


static double f(double a, double c)
{
      return 1/(1 + pow(c * a, 2));
}

static double fi(double a, double c)
{
	return (1/c)*atan(c * a);
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
