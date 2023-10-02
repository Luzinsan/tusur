#include "mpi.h"
#include <stdio.h>
#include <math.h>
#include <iostream>
#include <cassert>


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
        std::cerr << "\tProcess " << PID << " on " << processor_name << "\n";
        fflush(stderr);
    }

    template <typename T>
    void send(T *buffer, int to_PID, 
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

    template <typename T>
    MPI_Status receve(T *buffer, int from_PID, 
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
public:
    Integral(int argc, char *argv[], int numIntervals): Process(argc, argv) { intervals = numIntervals; }
    Integral(int argc, char *argv[], MPI_Comm comm = MPI_COMM_WORLD): Process(argc, argv, comm) {}

    int getIntervals()
    {
        if (PID == Process::INIT)
        {
            std::cout << "Enter the number of intervals (0 quit) "; fflush(stdout);
            int n;
            std::cin >> n;
            intervals = n;
            startwtime = MPI_Wtime();
            /* Sending the number of intervals to other nodes */
            for (int to_PID = 1; to_PID < numprocs; to_PID++)
                send(&intervals, to_PID);
        }
        else
        {
            MPI_Status status = receve(&intervals, Process::INIT);
            assert(status.MPI_ERROR);
        }
        
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
        printf("Process %d SUMM %.16f\n", PID, sum);
        return sum;
    }


    double summarazing()
    {
        /* Sending the local sum to node 0 */
        if (PID != Process::INIT)
        {
            send(&sum, Process::INIT, MPI_DOUBLE);
            return sum;
        }
        else
        {
            double integral = sum;
            for (int i=1; i< numprocs; i++)
            { 
                double recv_summ;
                MPI_Status status = receve(&recv_summ, i, MPI_DOUBLE);
                assert(status.MPI_ERROR);
                integral += recv_summ;  
            }
            printf("Integral is approximately  %.16f, Error   %.16f\n", integral, integral - fi(xh) + fi(xl));
            endwtime = MPI_Wtime();
            printf("Time of calculation = %f\n", endwtime-startwtime);
            return integral;
        }
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
