#include<stdio.h>
#include<queue>
#include<math.h>
#include<string.h>
#include<iostream>
using namespace std;
queue<float> myqueue;
#define INF 99999999.9
#define MAXSIZE 1000
extern "C" {
	int i;
	double p_i, s_i, ps_min, p_min, s_min;
	double alpha, beta,W1[MAXSIZE],W2[MAXSIZE];
	bool newDrift = false;
	double SUM1,SUM2;
	int number1, number2,current1,current2;
	void Initialize(){
                i = 1;
                p_i = 1;
                s_i = 0;
                ps_min = INF;
                p_min = INF;
                s_min = INF;
        }
	void init(double para[]){
		newDrift = false;
		alpha = para[0];
		beta = para[1];
		SUM1 = 0.0;
                SUM2 = 0.0;
                number1 = 0;
                number2 = 0;
		current1 = -1;
		current2 = -1;
		Initialize();
	}
	bool prediction(double xi){
		if(xi > 1.0 * SUM1 / number1)
			return false;
		return true;
	}
	double compute_si(double p, int i){
		return sqrt(p * (1 - p) / i);
	}
	void addW1(double xi){
		SUM1 += xi;
                if(number1 >= MAXSIZE)
                	SUM1 -= W1[current1];
                if(number1 < MAXSIZE)
                	number1 += 1;
               	current1 = (current1 + 1)%MAXSIZE;
                     	W1[current1] = xi;
	}
	void addW2(double xi){
		SUM2 += xi;
                if(number2 >= MAXSIZE)
                       	SUM2 -= W2[current2];
              	if(number2 < MAXSIZE)
                  	number2 += 1;
           	current2 = (current2 + 1)%MAXSIZE;
           	W2[current2] = xi;
	}
	int Process(double xi){
		if(prediction(xi)==false)
			p_i = p_i + (1.0 - p_i) / i;
		else
			p_i = p_i - p_i / i;
		s_i = compute_si(p_i,i);
		if(i<1000)
			i = i + 1;
		else
			i = 1000;		
		if(i>30){
			//printf("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb %d %f %d %f %d %f %f\n",i,SUM1,number1,SUM2,number2,SUM1/number1,SUM2/number2);
			if( p_i + s_i <= ps_min ){
				p_min = p_i;
				s_min = s_i;
				ps_min = p_i + s_i;
			}
			else if(p_i + s_i >= p_min + beta * s_min){
				//printf("aaa %d %d %f %f\n",i,number1,SUM1,SUM1/number1);
				Initialize();
				SUM1 = SUM2;
				number1 = number2;
				current1 = current2;
				memcpy(W1,W2,sizeof(W1));
				SUM2 = 0.0;
				number2 = 0;
				current2 = -1;
				addW1(xi);
				//printf("aaa %d %d %f %f %f %f %f\n",i,number1,SUM1,p_i,p_min,s_i,s_min);
				return 2;
			}
			else if(p_i + s_i >= p_min + alpha * s_min){
				if(newDrift == true){
					SUM2 = 0.0;
					number2 = 0;
					current2 = -1;
					newDrift = false;
				}
				addW2(xi);
				addW1(xi);
				return 1;
			}
			else
				newDrift = true;
		}
		addW1(xi);
		if(i>1000000000){
			SUM1 = 0.0;
			number1 = 0;
			current1 = -1;
			SUM2 = 0.0;
			number2 = 0;
			current2 = -1;
			Initialize();
		}
		return 0;
	} 	
}


