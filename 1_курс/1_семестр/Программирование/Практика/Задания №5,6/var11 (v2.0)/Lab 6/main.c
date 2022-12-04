#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include <limits.h>

int Avtom (int **A, int *m, int *n)
{
    *m = 3;
    *n = 5;

    A = (int**) malloc (*m * sizeof(int*));

    A[0] = (int*) malloc (*n * sizeof(int));
    A[0][0] = -1;
    A[0][1] = 4;
    A[0][2] = 7;
    A[0][3] = 3;
    A[0][4] = 6;

    A[1] = (int*) malloc (*n * sizeof(int));
    A[1][0] = 2;
    A[1][1] = -5;
    A[1][2] = 0;
    A[1][3] = 15;
    A[1][4] = 10;

    A[2] = (int*) malloc (*n * sizeof(int));
    A[2][0] = 8;
    A[2][1] = 9;
    A[2][2] = 11;
    A[2][3] = 12;
    A[2][4] = 20;

    return A;
}

void M_N (int *m, int *n)
{
    printf ("\n   Введите размер матрицы.\n   Количество строк: ");
    scanf ("%d", &*m);
    printf ("   Количество столбцов: ");
    scanf ("%d", &*n);

    while ((*n < 1) || (*m < 1) || ((*n < 1) && (*m < 1)))
    {
        printf ("\n   Размер матрицы задан неправильно!!!");

        printf ("\n   Введите размер заново.\n   Количество строк: ");
        scanf ("%d", &*m);
        printf ("   Количество столбцов: ");
        scanf ("%d", &*n);
    }

    return;
}

int Sam (int *m, int *n, int **A)
{
    A = (int**) malloc (*m * sizeof(int*));

    for (int s = 0; s < *m; s++)
    {
        A[s] = (int*) malloc (*n * sizeof(int));

        printf ("\n");

        for (int l = 0; l < *n; l++)
        {
            printf ("   Элемент[%d][%d]: ", s + 1, l + 1);
            scanf ("%d", &A[s][l]);
        }
    }

    printf ("\n");
    return A;
}

int Rando (int *m, int *n, int **A)
{
    A = (int**) malloc (*m * sizeof(int*));

    for (int s = 0; s < *m; s++)
    {
        A[s] = (int*) malloc (*n * sizeof(int));

        for (int l = 0; l < *n; l++)
        {
            A[s][l] = rand() % 100;
        }
    }

    printf ("\n");
    return A;
}

int Massiv (int *m, int *n, int **A)
{
    char b;
    printf ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n   Каким способом задается матрица (автоматически (A), самостоятельный ввод (S), ввод случайным образом (R))\n\t\t\t\t\t\t\t\t\t\t (при ошибке введите заново): ");
    scanf ("%c", &b);

    printf ("\n");

    while (!(b == 'A' || b == 'a' || b == 's' || b == 'S' || b == 'R' || b == 'r'))
    {
        printf ("   ");
        printf ("Ошибка!!!");
        printf ("   ");
        scanf ("%c", &b);
    }

    if (b == 'a' || b == 'A')
        A = Avtom (A, m, n);

    if (b == 's' || b == 'S')
    {
        M_N (m, n);

        A = Sam (m, n, A);
    }

    if (b == 'R' || b == 'r')
    {
        M_N (m, n);

        A = Rando (m, n, A);
    }
    return A;
}

void MX (int **A, int *m, int *n, int *i, int *j)
{
    int max = INT_MIN;

    for (int s = 0; s < *m; s++)
        for (int l = 0; l < *n; l++)
            {
                if (A[s][l] > max)
                {
                    max = A[s][l];

                    *i = s;
                    *j = l;
                }
            }

    return;
}

int Izmen (int **A, int *m, int *n, int *i, int *j)
{
    int q, p = n;

    for (int l = 0; l < *n; l++)
    {
        q = A[0][l];
        A[0][l] = A[*i][l];
        A[*i][l] = q;
    }

    for (int s = 0; s < *m; s++)
    {
        q = A[s][0];
        A[s][0] = A[s][*j];
        A[s][*j] = q;
    }

    return A;
}

int main()
{
    setlocale (LC_CTYPE, "RUSSIAN");
    printf ("\tЗадание: найти индексы строки и столбца максимального элемента прямоугольной матрицы A"
            "\n\t\t размера m*n. Поменять местами эту строку и этот столбец с первыми так, чтобы"
            "\n\t\t элемент A11 был максимальным элементом матрицы.\n\n");

    int **A;
    int m, n;
    A = Massiv (&m, &n, A);

    printf ("\n");
    printf ("   Исходная матрица:\n");
    for (int s = 0; s < m; s++)
    {
        printf ("   ");

        for (int l = 0; l < n; l++)
            printf ("%5d", A[s][l]);

        printf ("\n");
    }

    int i, j;
    MX (A, &m, &n, &i, &j);

    A = Izmen (A, &m, &n, &i, &j);

    printf ("\n    На пересечении строки %d и столбца %d находится максимальный элемент матрицы.", i + 1, j + 1);

    printf ("\n\n   Измененная матрица:\n");
    for (int s = 0; s < m; s++)
    {
        printf ("   ");

        for (int l = 0; l < n; l++)
            {
                printf ("%5d", A[s][l]);
            }

        printf ("\n");
    }

    for (int s = 0; s < m; s++)
        free(A[s]);
    free(A);

    getchar();
    return 0;
}
