#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

/** Описать функцию IsPowerN(K, N), возвращающую ненулевое значение, если целый параметр K > 0
является степенью числа N > 1, и ноль в противном случае. Дано число N > 1. */

    int main()
{

    SetConsoleCP(1251);

    SetConsoleOutputCP(1251);

        printf("Является ли число K степенью N?\n");

        int k=64,n=0;

        printf("Число K: %d\n",k);

    while (n<=1)

        {

        printf("Введите N > 1\n");

        scanf("%d",&n);

        if (n<=1) {printf("ОШИБКА!\n\n");

        }

}

    int IsPowerN(int,int);

      printf("\nРезультат: %d\n(1-да, 0-нет)",IsPowerN(k,n));

      system("pause");

      return (0);

    }

    int IsPowerN(K,N)

    {

    int flag=0,P=N;

    while (P <= K)

        {

        if (K == P) {flag = 1; P = P * N;}

        else {P = P * N;}

        }

    return (flag);

    }
