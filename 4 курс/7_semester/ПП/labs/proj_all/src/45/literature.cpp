#include <iostream>
#include <omp.h>
#include <semaphore.h>
#include <unistd.h>
#include <chrono>
#include <thread>
#include <fstream>

int Nrdr = 0;
sem_t W, R;
int data = 0;
int t = 1000;
std::ofstream file;

void READER(int n) 
{
    sem_wait(&R);
    Nrdr++;
    #pragma omp critical
    {
        std::cout << "READER " << omp_get_thread_num() << ": Nrdr=" << Nrdr << '\n';
        file << "READER " << omp_get_thread_num() << ": Nrdr=" << Nrdr << '\n';
    }
    if (Nrdr == 1) sem_wait(&W);
    sem_post(&R);
    #pragma omp critical
    {
        std::cout << "READER " << omp_get_thread_num() << ": Nrdr=" << Nrdr << ": data=" << data
                  << " inter="<<n<<std::endl;
        file << "READER " << omp_get_thread_num() << ": Nrdr=" << Nrdr << ": data=" << data
                  << " inter="<<n<<std::endl;
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(rand() % t + 1));
    {
        sem_wait(&R);
        Nrdr--;
        std::this_thread::sleep_for(std::chrono::milliseconds(rand() % t + 1));
        #pragma omp critical
        {
            std::cout << "READER "  << omp_get_thread_num() << ": Nrdr=" << Nrdr << std::endl;
            file << "READER "  << omp_get_thread_num() << ": Nrdr=" << Nrdr << std::endl;
        }
        if (Nrdr == 0) sem_post(&W);
        sem_post(&R);
    }

    std::this_thread::sleep_for(std::chrono::seconds(rand() % 1 + 1));
}

void WRITER(int n) 
{
    std::this_thread::sleep_for(std::chrono::milliseconds(rand() % t + 1));
    sem_wait(&W);
    data++;
    #pragma omp critical
    {
        std::cout<< "\nWRITER "  << omp_get_thread_num() << ": data=" << data << " inter="<<n<<std::endl;
        file << "\nWRITER "  << omp_get_thread_num() << ": data=" << data << " inter="<<n<<std::endl;
    }
        sem_post(&W);
    
    // std::this_thread::sleep_for(std::chrono::seconds(rand() % 1 + 1));
}

int main(int argc, char *argv[]) 
{
    sem_init(&W, 0, 1);
    sem_init(&R, 0, 1);
    file.open("out_sync.txt");

    int n = std::atoi(argv[1]);

    #pragma omp parallel
    {
        #pragma omp sections nowait
        {
            #pragma omp section
            {
                for (int i = 0; i < n; i++)
                    WRITER(i);
            }
            #pragma omp section
            {
                for (int i = 0; i < n; i++)
                    READER(i);
            }
            #pragma omp section
            {
                for (int i = 0; i < n; i++)
                    READER(i);
            }
            #pragma omp section
            {
                for (int i = 0; i < n; i++)
                    READER(i);
            }
        }
    }

    file.close();
    sem_destroy(&W);
    sem_destroy(&R);
    
    return 0;
}
