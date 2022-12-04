#include<stdio.h>
#include<stdlib.h>
#include<time.h>

void funk();
int** cre_arr();
void pr_array();

void chose3()
{	
	int n;
	int **array;
	srand(time(NULL));
	
	printf("Угу, тогда скорее начнём! Введите размерность квадратной матрицы:\n");
	scanf("%d",&n);
	
	array = cre_arr(n);
	
	for(int i =0; i<n;i++)
		for(int j=0; j<n; j++)
			{
				printf("a сейчас введите элемент A[%d%s%d%s\n",i+1,"][",j+1,"]");
				scanf("%d",&array[i][j]);
			}
	
	
	printf("исходная матрица:\n");
	pr_array(n, array );
	funk(n,array);

	printf("\nЭто всё, если что я буду на вашем электронном носителе :~).\n");

	
}
