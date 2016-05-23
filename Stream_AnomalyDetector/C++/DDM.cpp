#include<stdio.h>
#include<math.h>
#define INF 99999999.9
#define MAXSIZE 100
extern "C" {
	int i;
	double p_i, s_i, ps_min, p_min, s_min;
	double threshold, alpha, beta;
	bool newDrift = false;
	void Initialize(){
                i = 1;
                p_i = 1;
                s_i = 0;
                ps_min = INF;
                p_min = INF;
                s_min = INF;
        }
	void init(double _threshold, double _alpha, double _beta){
		threshold = _threshold;
		newDrift = false;
		alpha = _alpha;
		beta = _beta;
		//alpha = 2.0;
		//beta = 3.0;
		Initialize();
	}
	bool prediction(double xi){
		if(xi > threshold)
			return false;
		return true;
	}
	double compute_si(double p, int i){
		return sqrt(p * (1 - p) / i);
	}
	int Process(double xi){
		if(prediction(xi)==false)
			p_i = p_i + (1.0 - p_i) / i;
		else
			p_i = p_i - p_i / i;
		s_i = compute_si(p_i,i);
		if(i<10000)
			i = i + 1;
		if(i>30){
			//printf("aaa %f %f %f %f\n",p_i,p_min,s_i,s_min);
			if( p_i + s_i <= ps_min ){
				p_min = p_i;
				s_min = s_i;
				ps_min = p_i + s_i;
			}
			else if(p_i + s_i >= p_min + beta * s_min){
				Initialize();
				return 1;
			}
			else if(p_i + s_i >= p_min + alpha * s_min){
				return 2;
			}
		}
		return 0;
	} 	
}


