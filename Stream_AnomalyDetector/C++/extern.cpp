#include<stdio.h>
extern "C" {
	void display(int a){
		printf("this is in the c %d\n",a);
	}
}
