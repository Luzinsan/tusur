#include <stdio.h>
#include <stdlib.h>

#define  M 3
#define  N 4

/*Дана матрица размера M  N.
В каждом ее столбце найти количество элементов,
больших среднего арифметического всех элементов
этого столбца.
*/

int main(void) {

    SetConsoleCP(1251);

    SetConsoleOutputCP(1251);

        int ar[M][N], i, j, sum;

        int count;

        float sr;

          for (i = 0; i < M; ++i) {

            for (j = 0; j < N; ++j) {

              printf("ar[%d][%d]\n", i, j);

              scanf("%d", &ar[i][j]);
        }
    }

    for (i = 0; i < M; ++i) {

        for (j = 0; j < N; ++j) {

            printf("%d ",ar[i][j]);
        }

        printf("\n");
    }


    for (j = 0; j < N; ++j) {

        sum = count = 0;

        for (i = 0; i < M; ++i) {

            sum += ar[i][j];
        }
        sr = (float) sum / M;

        for (i = 0; i < M; ++i) {

            if (ar[i][j] > sr) {

                ++count;
            }
        }

        printf("В столбце %d массива %d эл., больших средн.арифм.\n", j, count);
    }

    system("pause");

    return(0);
}


