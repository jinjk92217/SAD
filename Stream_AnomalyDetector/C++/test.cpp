#include <iostream>
#include <stdio.h>
#include <queue>
#include<string.h>
using namespace std;
queue<float> q;
int main()
{	
	int i;
	cout<<"hello world!\n";
	for(i=0;i<12;i++)q.push(i*1.0);
	for(i=0;i<12;i++){cout<<q.front()<<" "<<q.size();q.pop();}	
	int a[10]={1};
	int b[10]={2};
	for(i=0;i<10;i++){a[i]=1;b[i]=2;}
	for(i=0;i<10;i++)printf("%d\n",a[i]);
	memcpy(a,b,sizeof(a));
	for(i=0;i<10;i++)printf("%d\n",a[i]);
	return 0;
}
