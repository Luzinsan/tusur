#include "mpi.h"
#include <cstdio>
#include <math.h>
#include <iostream>
#include <cassert>
#include <fstream>


static double f(double a);
static double fi(double a);


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
        std::cout << "\tProcess " << PID << " on " << processor_name << "\n"; fflush(stdout);
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

    void broadcast(void *buffer, int from_PID=Process::INIT, 
              MPI_Datatype type=MPI_INT, int count_data=1,  
              MPI_Comm comm = MPI_COMM_WORLD)
    {
        MPI_Bcast (buffer,             /* buffer              */
                   count_data,          /* one data            */
                   type,                /* type                */
                   from_PID,            /* to which node       */
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
};



class Integral: public Process
{
private:
    int intervals = 0;
    double xl = -0.2,	// low  bordert
	       xh =  1.0;	// high border
    double step;
    double sum = 0.0;
    double startwtime, endwtime;
    FILE* fout;
public:
    Integral(int argc, char *argv[], int numIntervals): Process(argc, argv) { intervals = numIntervals; }
    Integral(int argc, char *argv[], MPI_Comm comm = MPI_COMM_WORLD,
             std::string filename = "output.txt")
             : Process(argc, argv, comm) 
    {
        fflush(NULL);
        fout = fopen(filename.c_str(), "a+");
        fflush(NULL);
    }
    ~Integral(){ fclose(fout); }

    int getIntervals()
    {
        if (PID == Process::INIT)
        {
            std::cout << "Enter the number of intervals (0 quit) "; fflush(NULL);
            int n;
            std::cin >> n; fflush(stdin);
            intervals = n;
            if (n != 0) 
            {
                fprintf(fout, "\nNumber of processes: %d\nNumber of intervals: %d\n", 
                                numprocs, intervals);  fflush(NULL);
            }
            startwtime = MPI_Wtime();
        }
        broadcast(&intervals);
        return intervals;
    }

    /* Calculate of integral  */
    double evalIntegral()
    {
        step  = (xh-xl) / static_cast<double>(intervals);
        for (int i = PID + 1; i <= intervals; i += numprocs)
        {
            double x = xl + step * ((double)i - 0.5);
            sum += f(x);
        }
        sum *= step;
        printf("Process %d SUMM %.16f\n", PID, sum);  fflush(NULL);
        return sum;
    }


    double summarazing()
    {
        double integral = 0;
        reduce(&sum, &integral, MPI_DOUBLE);
        
        endwtime = MPI_Wtime();

        if (PID == Process::INIT)
        {
            printf("Integral is approximately  %.16f, Error   %.16f\n", integral, integral - fi(xh) + fi(xl));
            printf("Time of calculation = %f\n", endwtime-startwtime); fflush(NULL);
            fprintf(fout, "Integral is approximately  %.16f, Error   %.16f\n", integral, integral - fi(xh) + fi(xl)); fflush(NULL);
            fprintf(fout, "Time of calculation = %f\n\n", endwtime-startwtime); fflush(NULL);
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


static double f(double a)
{
      return 1/(1 + pow(0.9 * a, 2));
}

static double fi(double a)
{
	return (10/(double)9)*atan(0.9 * a);
}
