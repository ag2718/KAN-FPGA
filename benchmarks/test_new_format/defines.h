#ifndef DEFINES_H_
#define DEFINES_H_

#include <ap_int.h>
#include <ap_fixed.h>
#include <hls_stream.h>

#define N_INPUT 4
#define N_OUTPUT 1

#define LUT_SIZE 64

// Model related
typedef ap_fixed<8,6,AP_RND,AP_SAT> input_t;
typedef ap_fixed<8,6,AP_RND,AP_SAT> result_t;

// LUT related
typedef ap_fixed<8,6> lut_t;
typedef ap_fixed<8,6> lut_input_t;

#endif