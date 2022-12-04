#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>

/* Дано число R и массив A размера N. Найти элемент массива, который наиболее
близок к числу R (то есть такой элемент A K , для которого величина |A K − R| явля-
ется минимальной)*/

int *cr_arr(int h)
	{
		int *arr;

		arr =(int*)calloc(h,sizeof(int*));
		if( !arr ) return NULL;

		for(int i=0; i<h; i++)
			arr[i] = rand() % 10;


		return arr;
	}

int fun(int r,int n,int *arr)
{
	int a;

	a = arr[0];

	for(int i=0; i<n; i++)
			{
	            		printf("%d ", arr[i]); // печать массива
				if( fabs(a - r) > fabs(arr[i] - r) )a = arr[i];
			}
	return a;

}


int main()
{
	srand(time(NULL));
	int N,R,A;
	int *array;

	printf("Привет я Настя, вывожу элемент массива(вы размер а я заполню его разными числами) который наиболее близок ктому числу которое выввели(ВНИМАНИЕ если в последовательности 2 числа для которых |Ак-R| вывожу то которое раньше) .Начинаем!\n");

	printf("Введите размерность массива:\n");
	scanf("%d",&N);

	while(N<=0)
		{
			printf("некорректное значение N, пожалуйста повторите ввод\n");
			scanf("%d",&N);
		}

	printf("Введите число R:\n");
	scanf("%d",&R);


	array = cr_arr(N);

	A = fun(R,N,array);

	printf("\nОтвет:%d\n",A);

	free (array);


return 0;






}
