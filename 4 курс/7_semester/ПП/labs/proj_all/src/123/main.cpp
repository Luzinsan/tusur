#include "Integral.h"
#include "Matrix.h"


void lab1(int argc, char *argv[])
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
}


void lab2(int argc, char *argv[])
{
    Matrix<float> proc(argc, argv, 14, 4, 
    "/home/luzinsan/TUSUR_learn/4 курс/7_semester/ПП/labs/lr2/output.txt");
    proc.scatterVec();
}


void lab3(int argc, char *argv[])
{
    Matrix<float> proc(argc, argv, 9, 9, 
    "/home/luzinsan/TUSUR_learn/4 курс/7_semester/ПП/labs/lr3/output.txt");
    proc.selectTriangle();
}



int main(int argc, char *argv[])
{
    // lab1(argc, argv);
    // lab2(argc, argv);
    lab3(argc, argv);
    return 0;
}