#include <omp.h>
#include <iostream>
#include <math.h>

static double f(double a, double c);
static double fi(double a, double c);

void lab4(int argc, char *argv[])
{
    int intervals = 12;
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
    std::cout << "\nMaximum number of threads: " << max_threads;
    
    omp_set_num_threads(std::stoi(argv[1]));
    #pragma omp parallel
    #pragma omp master
        std::cout << "\nNumber of threads: " << omp_get_num_threads();
    
    double integral = 0;
    double step = (xh - xl) / static_cast<double>(intervals);
    std::cout << "\nStep: " << step << '\n';
    double startwtime = omp_get_wtime();
    #pragma omp parallel for shared(step, xl, c) reduction (+: integral)\
                schedule(dynamic) 
        for (int i = 1; i <= intervals; i++)
        {
            double x = xl + step * ((double)i - 0.5);
            integral += f(x, c) * step;
            #pragma omp critical
                std::cout << omp_get_thread_num()
                          << ": " << "x=" << x << ";\t f(x)=" << f(x, c) 
                          << "; \tpart of integral=" << integral << '\n';
        }
    std::cout << std::scientific << "\nIntegral is approximately: " << integral;
    std::cout << std::scientific << "\nError: " << integral - fi(xh, c) + fi(xl, c);
    std::cout << std::scientific << "\nTime of calculation: " << omp_get_wtime() - startwtime;
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

