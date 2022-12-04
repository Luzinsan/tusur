#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

/* Дан массив размера N и целое число K (1 ≤ K < N). Осуществить сдвиг элементов
массива вправо на K позиций (при этом A 1 перейдет в A K+1 , A 2 — в A K+2 , . . ., A N−K
— в A N , а исходное значение K последних элементов будет потеряно). Первые K
элементов полученного массива положить равными 0. Вспомогательные масси-
вы не использовать.*/

int *cr_arr(int h)
	{
		int *arr;

		arr =(int*)calloc(h,sizeof(int*));
		if( !arr ) return NULL;

		for(int i=0; i<h; i++)
		{
			arr[i] = rand() % 10;
		}

		return arr;
	}

void pr_arr(int e,int *arr)
	{
		for(int i=0; i<e; i++)
		{
			printf("%d ", arr[i]);
		}
	}

int *funk(int j, int k, int *arr)
	{
		for(int i= j; i >= 0; i--)
		{
			arr[i] = arr[i-k];
			if(i+1 <= k  ) arr[i]=0; // зануление первых k эл-ов массива
		}

		return arr;
	}


int main()
{
	srand(time(NULL));
	int n,k;
	int *array;

	printf("Привет я Георгий, смешаю массив(вы размерность я заполняю) на К позиция вправо, при этом первые К элементов зануляю.Вперёд!\n\n");

	printf("Введите размерность массива:\n");
	scanf("%d",&n);

	printf("Введите число K:\n");
	scanf("%d",&k);

	while(k <= 0)
		{
			printf("Введенно некорректное значение, попробуйте снова:\n");
			scanf("%d",&k);
		}

	array = cr_arr(n);

	printf("Исходный массив:\n");
	pr_arr(n,array);
	printf("\nНовый массив:\n");

	array = funk(n,k,array);
	pr_arr(n,array);

	printf("\n");
	free (array);


return 0;






}
