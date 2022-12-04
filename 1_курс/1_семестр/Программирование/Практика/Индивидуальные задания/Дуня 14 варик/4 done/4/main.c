#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <math.h>
#include <time.h>

/**Дан массив размера N.
Найти номер его последнего локального максимума*/


    int main()

{

    SetConsoleCP(1251);

    SetConsoleOutputCP(1251);

        printf("Дан массив размера N.\n");

        printf("Найти номер его последнего локального максимума\n");

    int N, NM=0, i;

    printf("Введите N: ");

    scanf("%d",&N);

	int arr[N]; ///Ввод массива


	for (i=0; i <= N-1; i++)

	{

            printf("Введите arr[%d]: ",i);

            scanf("%d",&arr[i]);

	}

	for (i=1; i <= N-2; i++){

						        ///Поиск локального максимума
    	    if((arr[i]>arr[i-1])&&(arr[i]>arr[i+1])){

            NM=i;
    }
}
    printf("Номер локального максимума: %d",NM);

    system("pause");

    return(0);

}

