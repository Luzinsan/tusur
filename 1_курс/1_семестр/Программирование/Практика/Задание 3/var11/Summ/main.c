#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

int main()
{
    SetConsoleCP (1251);
    SetConsoleOutputCP (1251);

    printf("Печатают сумму N квадратов значений, вычисляемых по правилу\n"
           "\n\ta = i/3 если i кратно 3, в противном случае a = i/(i-3),\n"
           "\tгде i = 1, 2,..., N.\n"
           "\nВведите значение количества слагаемых: ");
    int N;
    scanf ("%d", &N);

/**     Вычислить значение суммы S */

    double a,
           S= 0.0,
           k = 0,
           b = 0;
    int i = 1;

    while (i <= N)
    {
        if (i%3 == 0)
        {
            a = (double)i / 3;
            k = k + 1;
        }

        else
        {
            a = (double)i / (i - 3);
            b = b + 1;
        }


        S = S + a * a;
        i = i + 1;
    }

    printf ("\n\n\tПри N = %d имеем S = %8.4f\n", N, S);
    printf ("\n\tОперация a = i/3 выполнено k = %5.2f раз; оперврия a = i/(i-3) - b = %5.1f раз.\n", k, b);

    return 0;
}
