#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

//** Дан целочисленный массив размера N (> 2). Удалить из массива все элементы с четными номерами (2, 4, . . .). */

 int main(void)
{
    int a[10];

    int n,k=0;

    printf("N: ");

    scanf("%i",&n);

    int i;

    for (i=0; i<n; ++i)

    {

        printf("a[%i] : ",i+1);

        scanf("%i",&a[i]);
    }

    for (i=0; i<n; i+=2)

    {

            a[k]=a[i];

            ++k;
    }

    printf("A - %i\n",k);

    for (i=0; i<k; ++i) printf("  %i: %i\n",i+1,a[i]);

    system("pause");

    return 0;
}
