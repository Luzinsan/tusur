#include<stdio.h>
#include<stdlib.h>

#define h 3
void pr_array();

void funk(int n, int *Array[n])
{
	int S= 0,Jmax = 0,Smax;				// находим сумму 1 столбца и присваеваем Smax
							//  что бы было с чем сравнивать в дальнейшем
	for(int j = 0; j< 1;j++)
		for(int i = 0; i < n; i++)
                	S = S + Array[i][j];
	Smax = S;

	for(int j =0; j<n;j++)				// Находим максимальную столбец с макс суммой
		{
			S = 0;
			for(int i=0; i<n; i++)
				S = S + Array[i][j];

			if (S >= Smax)
				{
					Jmax = j;
					Smax = S;
				}

		}

	printf("\nОтвет:%d\n",Jmax + 1);		// Выводим номер  столбца с макс суммой(при этом нумерацию считаем с 1)


	if (Jmax == 2) 					//Если сумма 3 столбца наибольшая то меняем гл и побоч диогонали
		{
			printf("Новая матрица А:\n");
			int znach;
			for(int i = 0 , j =n -1 ; i<n;i++, j--)
				{
						znach = Array[i][i];
						Array[i][i] = Array[i][n-i-1];
						Array[i][n-i-1] = znach;
				}

			pr_array(n,Array);		//Вывод новой матрицы
		}
			free(Array);			// Освобождаем память
}

