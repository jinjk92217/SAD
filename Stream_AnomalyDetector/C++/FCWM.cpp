#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#define inf 99999999


extern "C" {
    double *reference_window, *recent_window, maxn_score, delta_score;
    int nBin, reference_window_size,recent_window_size;
    bool if_update = true;
    int *reference_bins, *recent_bins;
    int reference_number = 0, recent_number = 0;
    int tmp_bin;
    double tmp_score;
    int reference_front = 0, reference_end = 0, recent_front = 0, recent_end = 0;
    double KLDAB = 0.0, KLDBA = 0.0 , threshold;
    int count_alarm = 0;
    void init(int number_bin,int ref_size, int rec_size,double maxn, bool update_able, double Lambda){
           reference_front = 0;
           reference_end = 0;
           recent_front = 0;
           recent_end = 0;
           KLDAB = 0.0;
           KLDBA = 0.0;
           count_alarm = 0;
           reference_number = 0;
           recent_number = 0;
           nBin = number_bin;
           reference_window_size = ref_size;
           recent_window_size = rec_size;
           maxn_score = maxn;
           delta_score = 1.0 * maxn_score / nBin;
           if_update = update_able;
//           delete reference_window;
//           delete recent_window;
//           delete reference_bins;
//           delete recent_bins;
           reference_window = new double[reference_window_size];
           recent_window = new double[recent_window_size];
           reference_bins = new int[nBin];
           recent_bins = new int[nBin];
           for(int i = 0; i< nBin; i++){
                reference_bins[i] = 1;
                recent_bins[i] = 1;
           }
           threshold = Lambda;
    }
    void compute_KLD(){
        KLDAB = 0.0;
        KLDBA = 0.0;
        for(int bin = 0; bin < nBin ; bin++)
        {
//              SUM_KLD += fabs(1.0 * reference_bins[bin]/ (reference_window_size+nBin) * log(1.0 * reference_bins[bin]/recent_bins[bin]) - 1.0 * recent_bins[bin]/ (recent_window_size+nBin) * log(1.0 * recent_bins[bin]/reference_bins[bin]));
                KLDAB = KLDAB + 1.0 * reference_bins[bin]/ (reference_window_size+nBin) * log(1.0 * reference_bins[bin]/recent_bins[bin]);
                KLDBA = KLDBA + 1.0 * recent_bins[bin]/ (recent_window_size+nBin)* log(1.0 * recent_bins[bin]/reference_bins[bin]);

        }
    }
    void increase_bins(int bin){
            KLDAB = KLDAB + 1.0 * reference_bins[bin]/ (reference_window_size + nBin)* log(1.0 * reference_bins[bin]/recent_bins[bin]);
            KLDBA = KLDBA + 1.0 * recent_bins[bin]/ (recent_window_size + nBin) * log(1.0 * recent_bins[bin]/reference_bins[bin]);
    }
    void decrease_bins(int bin){
            KLDBA = KLDBA - 1.0 * recent_bins[bin]/ (recent_window_size + nBin) * log(1.0 * recent_bins[bin]/reference_bins[bin]);
            KLDAB = KLDAB - 1.0 * reference_bins[bin]/ (reference_window_size + nBin) * log(1.0 * reference_bins[bin]/recent_bins[bin]);
    }
    void put_reference(double score){
        reference_window[reference_end] = score;
        reference_end = (reference_end + 1) %reference_window_size;
        tmp_bin = score / delta_score;
        if(tmp_bin>=nBin)
            tmp_bin = nBin-1;
        decrease_bins(tmp_bin);
        reference_bins[tmp_bin] = reference_bins[tmp_bin] + 1;
        increase_bins(tmp_bin);
    }
    void get_reference(){
        tmp_score = reference_window[reference_front];
        reference_front = (reference_front + 1) %reference_window_size;
        tmp_bin = tmp_score / delta_score;
        if(tmp_bin>=nBin)
            tmp_bin = nBin-1;
        decrease_bins(tmp_bin);
        reference_bins[tmp_bin] = reference_bins[tmp_bin] - 1;
        increase_bins(tmp_bin);
    }
    void put_recent(double score){
        recent_window[recent_end] = score;
        recent_end = (recent_end + 1) %recent_window_size;
        tmp_bin = score / delta_score;
        if(tmp_bin>=nBin)
            tmp_bin = nBin-1;
        decrease_bins(tmp_bin);
        recent_bins[tmp_bin] = recent_bins[tmp_bin] + 1;
        increase_bins(tmp_bin);
    }
    void get_recent(){
        tmp_score = recent_window[recent_front];
        recent_front = (recent_front + 1) %recent_window_size;
        tmp_bin = tmp_score / delta_score;
        if(tmp_bin>=nBin)
            tmp_bin = nBin-1;
        decrease_bins(tmp_bin);
        recent_bins[tmp_bin] = recent_bins[tmp_bin] - 1;
        increase_bins(tmp_bin);
    }
    int Process(double xi){
        if(reference_number<reference_window_size){
            put_reference(xi);
            reference_number += 1;
        }
        else if(if_update == true){
                get_reference();
                put_reference(xi);
        }
        if(recent_number < recent_window_size){
            recent_number += 1;
            put_recent(xi);
        }
        else{
            get_recent();
            put_recent(xi);
        }
        if(count_alarm < 1.5 * recent_window_size)
            count_alarm += 1;
        if(reference_number<reference_window_size || recent_number< recent_window_size || count_alarm < 1.5 * recent_window_size)
            return 0;
//        compute_KLD();
        if(fabs(fabs(KLDAB) - fabs(KLDBA))> threshold)
        {
            count_alarm = 0;
//        if(SUM_KLD>threshold)
            return 1;
        }
        return 0;
    }
}