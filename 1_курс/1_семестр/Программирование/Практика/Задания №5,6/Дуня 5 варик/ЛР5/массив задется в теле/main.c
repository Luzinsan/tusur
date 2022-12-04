#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <locale.h>
void function(int arr[10][10])
{
    int i, j, sum, M=10;

    printf("Массив M x M:\n");

        for (i=0; i<M; i++)

        {
            for(j=0; j<M; j++)

                {
                    printf("%3d ",arr[i][j]);
                }

            printf("\n");
        }

    sum=0;

    for(j=1; j<M; j++)

    {
        for(i=0; i<M; i++)

            {

            sum+=arr[i][j];

            }

        j++;
    }

    printf("\n\nСумма чисел: %d \n\n", sum);

    if (sum > 0)

    {

    printf("\n Преобразованный массив M x M:");

    for(i=0; i<M; i++)

    {

        for(j=0; j<M; j++)

        arr[i][j]*=arr[i][j];

    i++;

    }

    }

    if (sum < 0)

    {
        printf("\n Преобразованный массив M x M:");

        for(j=0; j<M; j++)

            {

            i = M - j - 1;

            arr[i][j] +=2;

            }
    }

    printf("\n");

    for (i=0; i<M; i++)

    {
        for(j=0; j<M; j++)

        {

        printf("%3d ",arr[i][j]);

        }

    printf("\n");

    }

}
int main()

{
    int arr[10][10]=

    {
        {1, 2, 3, 10, -20, 6, 8, 0, 9, -11},
        {1, 2, 3, 10, -20, 6, 8, 0, 9, -11},
        {1, 2, 3, 10, -20, 6, 8, 0, 9, -11},
        {1, 2, 3, 10, -20, 6, 8, 0, 9, -11},
        {1, 2, 3, 10, -20, 6, 8, 0, 9, -11},
        {1, 2, 3, 10, -20, 6, 8, 0, 9, -11},
        {1, 2, 3, 10, -20, 6, 8, 0, 9, -11},
        {1, 2, 3, 10, -20, 6, 8, 0, 9, -11},
        {1, 2, 3, 10, -20, 6, 8, 0, 9, -11},
        {1, 2, 3, 10, -20, 6, 8, 0, 9, -11}
    };

    setlocale (LC_CTYPE, "RUS");

    printf("\n");

    function(arr);

    return 0;

}
