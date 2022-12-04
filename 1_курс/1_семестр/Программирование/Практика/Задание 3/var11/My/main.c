#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

 void function (int n)
    {
    int k=0,
        q=2;
    printf("\nОтвет: ");

    while (n >= (q*q))
    {
        if ((n%(q*q)) == 0)
        {
            if ((n%(q*q*q)) != 0)
            {
                printf("%d",q);
                printf(" ");
                k=k+1;
            }
        }
        q=q+1;
    }
    if (k == 0) printf("0");

    printf("\n");

    return;
    }

int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);

    printf("Получение всех таких q, при которых:\n"
           "- n делится на q^2; \n"
           "- n не делится на q^3.\n");

    int n;
    printf("\nВведите значение n.\n");
    scanf("%d", &n);

    function (n);

    return 0;
}
