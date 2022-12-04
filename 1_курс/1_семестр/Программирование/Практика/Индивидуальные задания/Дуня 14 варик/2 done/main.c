#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <math.h>
#include <time.h>

/** Дано целое число N и набор из N целых чисел, содержащий по крайней мере два
нуля. Вывести сумму чисел из данного набора, расположенных между первым и
последним нулем (если первый и последний нули идут подряд, то вывести 0). */

    int main()
{

    srand(time(NULL));

    SetConsoleCP(1251);

    SetConsoleOutputCP(1251);

        printf("Нахождение суммы между нулями в сгенерированном ряду: \n");

        int N, Nt, S, i;

          printf("Введите N: ");

          scanf("%d",&N);

    int OzAs(int,int,int); ///Объявление функции OzAs

	for (i=1; i <= N; i++){

            Nt = rand();

            if (Nt< 10000) {Nt=0;}
                                                      ///Генерация случайных чисел
            else {if (Nt< 25000) {Nt=2;} else{Nt=3;}

	}

    S= OzAs(N, Nt, i);
}

    printf("\nCумма чисел между первым и последним нолями: %d\n",S);

    system("pause");

    return(0);

}

	int flag =0,S=0,Smb=0; /// Объявление переменных

	int OzAs(N, Nt, i){    ///Функция OzAs

	if (i < N/2){          ///Обработка первой части ряда

            printf("%d ",Nt); ///вывод числа на экран

            if (Nt == 0){flag++;}

              if (flag == 1){S=S+Nt;}

                if (flag > 1){

                  if (Nt == 0){S=S+Smb;Smb=0;}

                      else{Smb=Smb+Nt;}

                        }
            }

	else {///Обработка второй части ряда

        if(flag < 2){Nt=0;}

            printf("%d ",Nt); ///вывод числа на экран

              if (Nt == 0){flag++;}

                if (flag == 1){S=S+Nt;}

                  if (flag > 1){

                    if (Nt == 0){S=S+Smb;Smb=0;}

                    else{Smb=Smb+Nt;

		    }

            }



     }

    return(S);  ///Вернуть S

}
