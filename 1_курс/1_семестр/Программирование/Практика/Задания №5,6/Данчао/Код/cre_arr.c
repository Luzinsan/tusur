#include<stdio.h>
#include<stdlib.h>

int **cre_arr(int n)
{
	int **arr;

	arr = (int**)calloc(n,sizeof(int**)); //создаём массив указателей на указатели
	for(int i = 0; i<n; i++)
		arr[i] = (int*)calloc(n,sizeof(int*)); // заполняем 1 массив указателями
	if( !arr ) return NULL;

	return arr;
}
