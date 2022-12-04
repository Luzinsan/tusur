#include<stdio.h>
#include<stdlib.h>

void pr_array(int n,int *array[n])
{ 
	printf("\n");
	for(int i =0; i<n;i++)
		for(int j=0; j<n; j++)
			{
	            		printf("%d ", array[i][j]);
	            		if(j==n-1) printf("\n");
			}
}			
