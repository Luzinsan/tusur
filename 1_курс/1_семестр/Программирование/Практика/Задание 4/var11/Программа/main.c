#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include <math.h>


double series (double x, double e)
{
    double a = (2 * x), s = 0;
    int n = 0;

    while (sqrt(a*a) >= e)
    {
        s = s + a;
        n = n + 1;
        a = (a * 4 * x * x) / (4 * n * n + 2 * n);
    }

    return s;
}


int main ()
{
    setlocale (LC_CTYPE, "RUSSIAN");

    printf ("\tВычисление и печатать таблицы значений функции F(x), заданной рядом Тейлора.\n\n");

    printf ("\n\t\t   бесконечность \n");
    printf ("\t\t\t__      2n+1 \n");
    printf ("\t\t        \\   (2x) \n");
    printf ("\tФункция:  F(x) = > -------. \n");
    printf ("\t\t\t/  (2n+1)! \n");
    printf ("\t\t\tTT \n");
    printf ("\t\t\tn=0 \n\n");
    printf ("\tДробные числа вводить через \".\". \n");
    printf ("      ____________________________________________________________________________________\n\n\n");

    double A, B;

    printf ("\tВведите границы интервала. \n\n");
    printf ("\t\tЛевая: ");
    scanf ("%lf", &A);
    printf ("\t\tПравая: ");
    scanf ("%lf", &B);
    printf ("\n\n");

    while (A == B)
    {
        printf ("\tОшибка! \n\tВведены одинаковые значения границ интервала. \n\tВведите другие значчения. \n");
        printf ("\t\tЛевая: ");
        scanf ("%lf", &A);
        printf ("\t\tПравая: ");
        scanf ("%lf", &B);
        printf ("\n\n");
    }

    double r;

    printf ("\tВведите шаг табулирования: ");
    scanf ("%lf", &r);
    printf ("\n\n");

    while (r == 0)
    {
        printf ("\tОшибка! \n\tШаг табулирования равен 0. \n\tВведите другое значение: ");
        scanf ("%lf", &r);
        printf ("\n\n");
    }

    while (sqrt(r * r) > sqrt((A - B) * (A - B)))
    {
        printf ("\tОшибка! \n\tДлина интервала меньше значения шаг табулирования. \n\tВведите другие значения. \n\n");

        printf ("\tВведите границы интервала. \n\n");
        printf ("\t\tЛевая: ");
        scanf ("%lf", &A);
        printf ("\t\tПравая: ");
        scanf ("%lf", &B);
        printf ("\n\n");

        while (A == B)
        {
            printf ("\tОшибка! \n\tВведены одинаковые значения границ интервала. \n\tВведите другие значчения. \n");
            printf ("\t\tЛевая: ");
            scanf ("%lf", &A);
            printf ("\t\tПравая: ");
            scanf ("%lf", &B);
            printf ("\n\n");
        }

        printf ("\tВведите шаг табулирования: ");
        scanf ("%lf", &r);
        printf ("\n\n");

        while (r == 0)
        {
            printf ("\tОшибка! \n\tШаг табулирования равен 0. \n\tВведите другое значение: ");
            scanf ("%lf", &r);
            printf ("\n\n");
        }
    }

    while (((r > 0) & (A > B)) | ((r < 0) & (A < B)))
    {
        if ((r < 0) & (A < B))
        {
            while ((r < 0) & (A < B))
            {
                printf ("\tОшибка! \n\tЗначения интервала увеличиваются, а шаг табулирования меньше 0. \n\tВведите другие значения. \n\n");

                printf ("\tВведите границы интервала. \n\n");
                printf ("\t\tЛевая: ");
                scanf ("%lf", &A);
                printf ("\t\tПравая: ");
                scanf ("%lf", &B);
                printf ("\n\n");

                while (A == B)
                {
                    printf ("\tОшибка! \n\tВведены одинаковые значения границ интервала. \n\tВведите другие значчения. \n");
                    printf ("\t\tЛевая: ");
                    scanf ("%lf", &A);
                    printf ("\t\tПравая: ");
                    scanf ("%lf", &B);
                    printf ("\n\n");
                }

                printf ("\tВведите шаг табулирования: ");
                scanf ("%lf", &r);
                printf ("\n\n");

                while (r == 0)
                {
                    printf ("\tОшибка! \n\tШаг табулирования равен 0. \n\tВведите другое значение: ");
                    scanf ("%lf", &r);
                    printf ("\n\n");
                }

                while (sqrt(r * r) > sqrt((A - B) * (A - B)))
                {
                    printf ("\tОшибка! \n\tДлина интервала меньше значения шаг табулирования. \n\tВведите другие значения. \n\n");

                    printf ("\tВведите границы интервала. \n\n");
                    printf ("\t\tЛевая: ");
                    scanf ("%lf", &A);
                    printf ("\t\tПравая: ");
                    scanf ("%lf", &B);
                    printf ("\n\n");

                    while (A == B)
                    {
                        printf ("\tОшибка! \n\tВведены одинаковые значения границ интервала. \n\tВведите другие значчения. \n");
                        printf ("\t\tЛевая: ");
                        scanf ("%lf", &A);
                        printf ("\t\tПравая: ");
                        scanf ("%lf", &B);
                        printf ("\n\n");
                    }

                    printf ("\tВведите шаг табулирования: ");
                    scanf ("%lf", &r);
                    printf ("\n\n");

                    while (r == 0)
                    {
                        printf ("\tОшибка! \n\tШаг табулирования равен 0. \n\tВведите другое значение: ");
                        scanf ("%lf", &r);
                        printf ("\n\n");
                    }
                }
            }
        }

        if ((r > 0) & (A > B))
        {
            while ((r > 0) & (A > B))
            {
                printf ("\tОшибка! \n\tЗначения интервала уменьшается, а шаг табулирования больше 0. \n\tВведите другие значения. \n\n");

                printf ("\tВведите границы интервала. \n\n");
                printf ("\t\tЛевая: ");
                scanf ("%lf", &A);
                printf ("\t\tПравая: ");
                scanf ("%lf", &B);
                printf ("\n\n");

                while (A == B)
                {
                    printf ("\tОшибка! \n\tВведены одинаковые значения границ интервала. \n\tВведите другие значчения. \n");
                    printf ("\t\tЛевая: ");
                    scanf ("%lf", &A);
                    printf ("\t\tПравая: ");
                    scanf ("%lf", &B);
                    printf ("\n\n");
                }

                printf ("\tВведите шаг табулирования: ");
                scanf ("%lf", &r);
                printf ("\n\n");

                while (r == 0)
                {
                    printf ("\tОшибка! \n\tШаг табулирования равен 0. \n\tВведите другое значение: ");
                    scanf ("%lf", &r);
                    printf ("\n\n");
                }

                while (sqrt(r * r) > sqrt((A - B) * (A - B)))
                {
                    printf ("\tОшибка! \n\tДлина интервала меньше значения шаг табулирования. \n\tВведите другие значения. \n\n");

                    printf ("\tВведите границы интервала. \n\n");
                    printf ("\t\tЛевая: ");
                    scanf ("%lf", &A);
                    printf ("\t\tПравая: ");
                    scanf ("%lf", &B);
                    printf ("\n\n");

                    while (A == B)
                    {
                        printf ("\tОшибка! \n\tВведены одинаковые значения границ интервала. \n\tВведите другие значчения. \n");
                        printf ("\t\tЛевая: ");
                        scanf ("%lf", &A);
                        printf ("\t\tПравая: ");
                        scanf ("%lf", &B);
                        printf ("\n\n");
                    }

                    printf ("\tВведите шаг табулирования: ");
                    scanf ("%lf", &r);
                    printf ("\n\n");

                    while (r == 0)
                    {
                        printf ("\tОшибка! \n\tШаг табулирования равен 0. \n\tВведите другое значение: ");
                        scanf ("%lf", &r);
                        printf ("\n\n");
                    }
                }
            }
        }
    }

    float e;

    printf ("\tВведите допустимую погрешность вычисления. \n\tЗначение допустимой погрешности вычисления должно входить в интервал 0 < e < 1. \n\n\t\t\t\t\t");
    scanf ("%f", &e);

    while ((e <= 0) | (e >= 1))
    {
        printf ("\tОшибка! \n\tЗначение допустимой погрешности вычисления не входит в интервал 0 < e < 1. \n\tВведите другое значение: ");
        scanf ("%f", &e);
    }

    printf ("      ____________________________________________________________________________________\n\n");
    printf ("\t\t\t   Таблица\n\n");
    printf ("\t\t+-----------+----------------+\n");
    printf ("\t\t|     x     |      F(x)      |\n");
    printf ("\t\t+-----------+----------------+\n");

    double x = A, Fx;

    if (A < B)
    {
        while (x <= B)
        {
            Fx = series (x, e);
            printf("\t\t| %9.4lf | %14.9lf |\n", x, Fx);
            x = x + r;
        }
    }
    if (A > B)
    {
        while (x >= B)
        {
            Fx = series (x, e);
            printf("\t\t| %9.4lf | %14.9lf |\n", x, Fx);
            x = x + r;
        }
    }

    printf ("\t\t+-----------+----------------+\n");

    return 0;
}
