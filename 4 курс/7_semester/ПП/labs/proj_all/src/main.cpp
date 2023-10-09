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
    Matrix<float> proc(argc, argv, 14, 4);
    proc.scatterVec();

}


int main(int argc, char *argv[])
{
    //lab1(argc, argv);
    lab2(argc, argv);
    return 0;
}