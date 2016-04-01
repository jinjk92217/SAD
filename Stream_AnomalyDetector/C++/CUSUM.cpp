#include<stdio.h>
#define NUL 99999999.9
extern "C" {
	double pre_x = NUL, gp = 0.0, gn = 0.0, drift, threshold, s;
	int first = 0;
	void init(double para[]){
		drift = para[0];
		threshold = para[1];
	}
	void prints(){float a = NUL; if(pre_x == NUL)printf("%f %f %f %d\n",drift,threshold,a,first);first = 1;}
	int Process(double x){
		if(first == 0){
			pre_x = x;
			first = 1;
			return 0;
		}
		s = x - pre_x;
		pre_x = x;
		gp = gp + s - drift;
		gn = gn - s - drift;
		//printf("CUSUM %f %f\n",gp,gn);
		if(gp < 0.0)
			gp = 0.0;
		if(gn < 0.0)
			gn = 0.0;
		if(gp > threshold || gn > threshold){
			gp = 0.0;
			gn = 0.0;
			return 1;
		}
		return 0;

	}
}


