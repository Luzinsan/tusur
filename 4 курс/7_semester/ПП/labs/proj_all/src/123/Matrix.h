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
    MPI_Datatype MPI_TRIANGLE;
    int len_type = 0;
  
public:
    Matrix(int argc, char *argv[], 
        int _rows=5, int _columns=5, 
        std::string filename = "/home/luzinsan/TUSUR_learn/4 курс/7_semester/ПП/labs/lr3/output.txt",
        MPI_Comm comm = MPI_COMM_WORLD)
        : Process(argc, argv, comm)
    {
        fout.open(filename, std::ios::app);
        rows = _rows;
        columns = _columns;
        data = new T[rows * columns]{0};
        if (PID==Process::INIT)
        {
            Communicator::printInfo("", fout);
            fillRandom();
            Process::printInfo("INITIAL RANDOM MATRIX", fout);
            fout << *this; fflush(NULL);
            Process::printInfo("\t--------------------------------", fout);
        }
        createDatatype();
        startwtime=MPI_Wtime();
    }
    void setShape(int _rows, int _columns)
    {
        rows = _rows;
        columns = _columns;
        MPI_Type_free(&MPI_TRIANGLE);
        createDatatype();
    }

    ~Matrix() { 
        fout.close(); 
        delete data;
        MPI_Type_free(&MPI_TRIANGLE);
    } 

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

    friend std::ostream& operator<<(std::ostream& out, const Matrix<T>& matrix)
    {
        out << "\nNumber of rows: " << matrix.rows
            << "\nNumber of columns: " << matrix.columns
            << "\n";
        for (int i = 0; i < matrix.rows; ++i) 
        {
            for (int j = 0; j < matrix.columns; ++j){
                out << std::setw(10)<<matrix.data[i * matrix.columns + j] << " "; fflush(NULL);}
            out << "\n";
        }
        fflush(NULL);
        return out;
    }
#pragma region lab2
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
#pragma endregion
    
#pragma region lab3
private:
    void createDatatype()
    {
        int length = (rows>>1) + 1;
        int blocklens[length], indices[length];
        /*

        1 1 1 1 1 1 1
        0 1 1 1 1 1 0
        0 0 1 1 1 0 0
        0 0 0 1 0 0 0
        0 0 0 0 0 0 0
        0 0 0 0 0 0 0
        0 0 0 0 0 0 0

        */
        for (int i=0; i<length; i++) 
        {
            blocklens[i] = columns - (i<<1);
            len_type += blocklens[i];
            indices[i]   = i*(columns + 1);
        }
        MPI_Type_indexed(length, blocklens, indices, 
                         MPI_FLOAT, &MPI_TRIANGLE);
        MPI_Type_commit(&MPI_TRIANGLE);
    }
public:
    void selectTriangle()
    {
        switch(PID){
            case Process::INIT:
                send(data, 1, MPI_TRIANGLE, 1, 1);
                send(data, 1, MPI_TRIANGLE, 1, 2);
                delete[] data;
                data = new T[rows * columns]{0};
                receive(data, 1, MPI_TRIANGLE);
                Process::printInfo("", fout);
                fout << *this; fflush(NULL);
                break;
            case 1:
                receive(data, Process::INIT, MPI_TRIANGLE, 1, 1);
                Process::printInfo("", fout);
                fout << *this; fflush(NULL);

                delete[] data;
                data = new T[rows * columns]{0};
                //??принять посланные данные в массив по размеру выбранных данных базового типа.
                receive(data, Process::INIT, MPI_FLOAT, len_type, 2); 
                
                Process::printInfo("", fout);
                fout << *this; fflush(NULL);

                send(data, Process::INIT, MPI_FLOAT, len_type);
                break;
        }
    }

#pragma endregion
    
 
};