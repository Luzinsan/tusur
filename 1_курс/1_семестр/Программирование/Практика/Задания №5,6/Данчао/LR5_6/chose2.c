#include<stdio.h>
#include<stdlib.h>
#include<time.h>

void funk();
int** cre_arr();
void pr_array();

void chose2()
{
	int n;
	int **array;
	srand(time(NULL));

	printf("Очень хорошо, в таком случае введите размерность квадратной матрицы:\n");
	scanf("%d",&n);

	array = cre_arr(n);

	for(int i =0; i<n;i++)
		for(int j=0; j<n; j++)
			array[i][j] = rand() % 10;

	printf("исходная матрица:\n");
	pr_array(n, array );
	funk(n,array);

	printf("\nФуууух вроде всё, ну вы это запускайте если что :)!!\n");



}
