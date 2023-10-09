#pragma once
#include <math.h>
#include <fstream>
#include <sstream>
#include "Process.h"

/*!
	@brief Класс, подсчитывающий интегральную сумму методом прямоугольника.
    Точность задаётся количеством разбиений интервала определённого интеграла - n
*/
class Integral : public Process
{
private:
    int intervals = 0;
    double xl = -0.2, // low  bordert
        xh = 1.0;     // high border
    double c = 0.9;
    double step;
    double sum = 0.0;
    double startwtime, endwtime;
    std::ofstream fout;

public:
    Integral(int argc, char *argv[], MPI_Comm comm = MPI_COMM_WORLD,
             std::string filename = "output.txt")
        : Process(argc, argv, comm)
    {
        fflush(NULL);
        fout.open(filename, std::ios::out);
        fflush(NULL);
    }
    ~Integral() { fout.close(); }

    void printInfo(std::string accompanying_message = "", std::ostream &out = std::cout)
    {
        out << "\nNumber of intervals: " << intervals
            << "\nLow border: " << xl
            << "\nHight border: " << xh
            << "\nParameter: " << c
            << "\n"
            << accompanying_message;
        fflush(NULL);
    }

    void unpuckParams(void *buf, int length)
    {
        
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
            std::cout << "\nEnter the number of intervals (0 quit): ";
            fflush(NULL);
            int n;
            std::cin >> n;
            fflush(stdin);
            intervals = n;
            if (n != 0)
            {
                double temp;
                std::cout << "Enter the low border: ";
                fflush(NULL);
                std::cin >> temp;
                fflush(stdin);
                xl = temp;
                std::cout << "Enter the hight border: ";
                fflush(NULL);
                std::cin >> temp;
                fflush(stdin);
                xh = temp;
                std::cout << "Enter the parameter of function: ";
                fflush(NULL);
                std::cin >> temp;
                fflush(stdin);
                c = temp;
            }
            else
                xl, xh, c = 0, 0, 0;
            buf = multiplePack(len_buf,
                               "iddd", intervals, xl, xh, c);
            startwtime = MPI_Wtime();
        }
        else
            buf = new char[len_buf];
        broadcast(buf, MPI_PACKED, len_buf);
        if (PID != Process::INIT)
        {
            unpuckParams(buf, len_buf);
            if (intervals == 0)
                return 0;
        }
        delete[] buf;
        return intervals;
    }


    /**
     * @brief Подсчёт интегральной суммы на изолированном отрезке
     * 
     * @return double интегральная сумма
     */
    double evalIntegral()
    {
        step = (xh - xl) / static_cast<double>(intervals);
        for (int i = PID + 1; i <= intervals; i += numprocs)
        {
            double x = xl + step * ((double)i - 0.5);
            sum += f(x, c);
        }
        sum *= step;
        std::stringstream str;
        str << std::scientific << "SUMM: " << sum;
        Process::printInfo(str.str());
        fflush(NULL);
        str.clear();
        str.str("");
        return sum;
    }

    /**
     * @brief Суммирование результатов со всех процессов
     * 
     * @return double итоговая интегральная сумма
     */
    double summarazing()
    {
        double integral = 0;
        reduce(&sum, &integral, MPI_DOUBLE);

        endwtime = MPI_Wtime();

        if (PID == Process::INIT)
        {
            Communicator::printInfo("", fout);
            printInfo("", fout);
            std::stringstream str;
            str << std::scientific << "Integral is approximately: " << integral;
            Process::printInfo(str.str(), fout);
            fflush(NULL);
            str.clear();
            str.str("");
            str << std::scientific << "Error: " << integral - fi(xh, c) + fi(xl, c);
            Process::printInfo(str.str(), fout);
            fflush(NULL);
            str.clear();
            str.str("");
            str << std::scientific << "Time of calculation: " << endwtime - startwtime;
            Process::printInfo(str.str(), fout);
            fflush(NULL);
            str.clear();
            str.str("");
            return integral;
        }
        else
            return sum;
    }

    /**
     * @brief Вычисление значения подынтегральной функции: 
     * @f$f(x) = \frac{1}{1+(c*a)^2}@f$
     * 
     * @param a абсцисса для вычисления значения в точке x
     * @param c параметр подынтегрального выражения
     * @return double вычисленная ордината
     */
    static double f(double a, double c)
    {
        return 1 / (1 + pow(c * a, 2));
    }

    /**
     * @brief Вычисление значения первообразной функции: 
     * @f$F(x) = \frac{1}{c} * \arctan(c*a)@f$
     * 
     * @param a абсцисса для вычисления значения в точке x
     * @param c параметр первообразной функции
     * @return double вычисленная ордината
     */
    static double fi(double a, double c)
    {
        return (1 / c) * atan(c * a);
    }
};



