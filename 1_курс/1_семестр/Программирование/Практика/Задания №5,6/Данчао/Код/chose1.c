#include<stdio.h>
#include<stdlib.h>

#define h 3
void funk_stat();
void pr_array_stat();

void chose1()
{	
	int k = 1;
	int array[h][h];

	for(int i =0; i<h;i++)
		for(int j=0; j<h; j++)
			array[i][j] = k++ ;

	printf("Исходная матрица:\n");
	pr_array_stat(h, array);
	funk_stat(h, array);

	printf("\nТааакс, на этом всё, если понадоблюсь запустите снова, хорошо =)?\n");


	
}

