#include "lut_0_0_0.h"
#include "lut_0_0_1.h"
#include "lut_0_0_2.h"
#include "lut_0_0_3.h"

void KAN(input_t input[N_INPUT], result_t output[N_OUTPUT])
{
#pragma HLS ARRAY_PARTITION variable = input complete
#pragma HLS ARRAY_PARTITION variable = output complete

#pragma HLS interface mode = ap_none port = input, output
#pragma HLS PIPELINE II = 1

	//// LAYER 0 ////

	// Compute activations from LUTs
	lut_t act_0_0_0 = lut_lookup_0_0_0(input[0]);
	lut_t act_0_0_1 = lut_lookup_0_0_1(input[0]);
	lut_t act_0_0_2 = lut_lookup_0_0_2(input[0]);
	lut_t act_0_0_3 = lut_lookup_0_0_3(input[0]);

	output[0] = act_0_0_0 + act_0_0_1 + act_0_0_2 + act_0_0_3;

}