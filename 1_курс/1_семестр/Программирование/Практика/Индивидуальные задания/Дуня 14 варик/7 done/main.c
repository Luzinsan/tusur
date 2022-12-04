#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

/*Дана матрица размера M × N. Удалить столбец, содержащий максимальный элемент матрицы.*/

int main(void)
{
    int a[10][10];

    int m,n;

    printf("M: ");

    scanf("%i",&m);

    printf("N: ");

    scanf("%i",&n);



    int i,j;

    for (i=0; i<m; ++i){

        printf("%i : \n", i+1);

        for (j=0; j<n; ++j){

            printf("%i : ", j+1);

            scanf("%i", &a[i][j]);
        }
    }

    int maxeI=0,maxeJ=0;

    for (i=0; i<m; ++i){

        for (j=0; j<n; ++j){

            if (a[i][j]>a[maxeI][maxeJ]) {

                maxeI=i;

                maxeJ=j;
            }
        }
    }


    --m;

    for (i=maxeI; i<m; ++i)

        for (j=0; j<n; ++j)

            a[i][j]=a[i+1][j];


    for (i=0; i<m; ++i){
        for (j=0; j<n; ++j) printf(" : %i", a[i][j]);
        printf(" : \n");
    }
    system("pause");

    return 0;
}
