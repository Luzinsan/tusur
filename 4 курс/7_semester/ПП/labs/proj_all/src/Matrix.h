#pragma once
#include "Process.h"
#include <fstream>
#include <iomanip>
#include <iostream>

#include <random>
#include <algorithm>
#include <iterator>
#include <vector>

template<typename T>
class Matrix: public Process
{
private:
    int rows, columns;
    T* data = NULL;
    double startwtime, endwtime;
    std::ofstream fout;
public:
    Matrix(int argc, char *argv[], 
        int _rows=5, int _columns=5, 
        MPI_Comm comm = MPI_COMM_WORLD,
        std::string filename = "/home/luzinsan/TUSUR_learn/4 курс/7_semester/ПП/labs/lr2/output.txt")
        : Process(argc, argv, comm)
    {
        fout.open(filename, std::ios::out);
        rows = _rows;
        columns = _columns;
        if (PID==Process::INIT)
        {
            Communicator::printInfo("", fout);
            data = new T[rows * columns];
            fillRandom();
            Process::printInfo("INITIAL RANDOM MATRIX", fout);
            fout << *this;
            Process::printInfo("\t--------------------------------", fout);
        }
        startwtime=MPI_Wtime();
    }
    ~Matrix() { fout.close(); delete data;} 

    void fillRandom(T min=-100.0, T max=100.0)
    {
        std::random_device rnd_device;
        std::mt19937 mersenne_engine {rnd_device()}; 
        std::uniform_real_distribution<T> dist {min, max};
        
        auto gen = [&dist, &mersenne_engine]()
                    {return dist(mersenne_engine);};

        std::generate(data, data + rows * columns, gen);
    }

    void printInfo(std::string accompanying_message = "", 
                    std::ostream &out = std::cout, T* buf=NULL, int length=0)
    {
        Process::printInfo("\n", out);
        if (buf)
            for(int i = 0; i < length/columns; i++)
            {
                for(int j = 0; j < columns; j++)
                    out << std::setw(10) << buf[i*columns + j] << " ";
                out << "\n"; fflush(NULL);
            }
        fflush(NULL);
    }
private:
    static T* reflect(T* array, int len, int cols)
    {
        for(int i = 0; i < len / cols; ++i)
            for(int j = 0; j < cols/2; ++j)
                std::swap(array[i*cols + j], 
                          array[i*cols + (cols -1-j)]);
        return array;
    }
public:

    void scatterVec()
    {
        int count = rows / numprocs;  
        int rest = rows % numprocs;
        int *displs = new int[numprocs], 
            *rcounts = new int[numprocs];
        if (PID==Process::INIT)
            for(int i = 0; i < numprocs; i++)
            {
                rcounts[i] = i < rest ? columns * (count+1) : columns*count;
                displs[i] = displs[i-1] + rcounts[i-1];
            }
        int length = PID < rest ? columns * (count+1) : columns*count;
        int startIndex = PID * length + (PID >= rest ? rest : 0);
        T *partOfArray = new T[length];

        MPI_Scatterv(data, rcounts, displs, MPI_FLOAT, 
                    partOfArray, length, MPI_FLOAT, Process::INIT, comm);
        
        reflect(partOfArray, length, columns);
        printInfo("", std::cout, partOfArray, length);
                
        MPI_Gatherv(partOfArray, length, MPI_FLOAT,
                    data, rcounts, displs, MPI_FLOAT, Process::INIT, comm);
        delete rcounts, displs, partOfArray;
    
        if (PID == Process::INIT)
        {
            fout << *this;
            std::stringstream str;
            str << std::scientific << "Time of calculation: " << endwtime - startwtime;
            Process::printInfo(str.str(), fout);
            Process::printInfo("\t--------------------------------", fout);
            fflush(NULL);
            str.clear();
            str.str("");
        }
    }

    friend std::ostream& operator<<(std::ostream& out, const Matrix<T>& matrix)
    {
        out << "\nNumber of rows: " << matrix.rows
            << "\nNumber of columns: " << matrix.columns
            << "\n";
        for (int i = 0; i < matrix.rows; ++i) 
        {
            for (int j = 0; j < matrix.columns; ++j)
                out << std::setw(10)<<matrix.data[i * matrix.columns + j] << " ";
            out << "\n";
        }
        fflush(NULL);
        return out;
    }
    
 
};