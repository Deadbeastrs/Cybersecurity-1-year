#ifndef __SPEED_T__
#define __SPEED_T__
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// call this function to start a nanosecond-resolution timer
struct timespec timer_start1(){
    struct timespec start_time;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start_time);
    return start_time;
}

// call this function to end a timer, returning nanoseconds elapsed as a long
long timer_end1(struct timespec start_time){
    struct timespec end_time;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end_time);
    long diffInNanos = (end_time.tv_sec - start_time.tv_sec) * (long)1e9 + (end_time.tv_nsec - start_time.tv_nsec);
    return diffInNanos;
}


#endif
