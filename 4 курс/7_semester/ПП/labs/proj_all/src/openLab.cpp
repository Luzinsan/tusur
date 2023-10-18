#include <omp.h>
#include <iostream>
#include <math.h>
#include <fstream>
#define CHUNK 1

static double f(double a, double c);
static double fi(double a, double c);

void lab4(int argc, char *argv[])
{
    std::ofstream fout("/home/luzinsan/TUSUR_learn/4 курс/7_semester/ПП/labs/proj_all/bin/4/output.txt",
                        std::ios::app);
    fout << "\n\n-------------------------------------------------------------";
    int intervals = 100000000;
    fout << "\nNumber of intervals: " << intervals;
    // std::cout << "\nEnter the number of intervals (0 quit): ";
    // std::cin >> intervals;
    if (!intervals) return;

    double xl=-0.2, xh=1.0, c=0.9;
    // std::cout << "\nEnter the low border: ";
    // std::cin >> xl;
    // std::cout << "\nEnter the hight border: ";
    // std::cin >> xh;
    // std::cout << "\nEnter the parameter of function: ";
    // std::cin >> c;

    int max_threads = omp_get_max_threads();
    fout << "\nMaximum number of threads: " << max_threads;
    if (argv[1])
        omp_set_num_threads(std::stoi(argv[1]));
    #pragma omp parallel
    #pragma omp master
        fout << "\nEvaluation on " << omp_get_num_threads() << " threads";
    
    double integral = 0;
    double step = (xh - xl) / static_cast<double>(intervals);
    fout << "\nStep: " << step << '\n';
    double startwtime = omp_get_wtime();
    fout << "\nSTATIC chunk:" << CHUNK;
    // fout << "\nSTATIC auto";
    // fout << "\nDYNAMIC chunk:" << CHUNK;
    // fout << "\nDYNAMIC auto";

    #pragma omp parallel for shared(step, xl, c) reduction (+: integral)\
                schedule(static, CHUNK) 
        for (int i = 1; i <= intervals; i++)
        {
            double x = xl + step * ((double)i - 0.5);
            integral += f(x, c) * step;
            // #pragma omp critical
            //     std::cout << omp_get_thread_num()
            //               << ": " << "x=" << x << ";\t f(x)=" << f(x, c) 
            //               << "; \tpart of integral=" << integral << '\n';
        }
    fout << std::scientific << "\nIntegral is approximately: " << integral;
    fout << std::scientific << "\nError: " << integral - fi(xh, c) + fi(xl, c);
    fout << std::scientific << "\nTime of calculation: " << omp_get_wtime() - startwtime;
}

int main(int argc, char *argv[])
{
    lab4(argc, argv);
    return 0;
}


static double f(double a, double c)
{
    return 1 / (1 + pow(c * a, 2));
}

   
static double fi(double a, double c)
{
    return (1 / c) * atan(c * a);
}

