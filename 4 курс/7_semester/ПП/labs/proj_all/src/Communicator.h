#pragma once
#include "mpi.h"

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
    ~Communicator() { MPI_Finalize(); }
public:
    virtual void printInfo(std::string accompanying_message = "", std::ostream &out = std::cout)
    {
        out << "\nProcessor name: " << processor_name
            << "\nNumber of processes: " << numprocs
            << "\n" << accompanying_message;
        fflush(NULL);
    }
};