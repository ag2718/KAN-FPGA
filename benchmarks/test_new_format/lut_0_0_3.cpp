#include "lut_0_0_3.h"
#include "value_to_index.h"

const lut_t lut_0_0_3[LUT_SIZE] = {
  (lut_t)0.00000e+00,  (lut_t)0.00000e+00, (lut_t)0.00000e+00, (lut_t)0.00000e+00,
(lut_t)0.00000e+00, (lut_t)0.00000e+00, (lut_t)0.00000e+00, (lut_t)0.00000e+00,
(lut_t)0.00000e+00, (lut_t)0.00000e+00,  (lut_t)0.00000e+00,  (lut_t)1.56250e-02,
 (lut_t)1.56250e-02,  (lut_t)1.56250e-02,  (lut_t)1.56250e-02,  (lut_t)1.56250e-02,
 (lut_t)1.56250e-02,  (lut_t)1.56250e-02,  (lut_t)1.56250e-02,  (lut_t)1.56250e-02,
(lut_t)0.00000e+00, (lut_t)-1.56250e-02, (lut_t)-1.56250e-02, (lut_t)-3.12500e-02,
(lut_t)-3.12500e-02, (lut_t)-3.12500e-02, (lut_t)-3.12500e-02, (lut_t)-3.12500e-02,
(lut_t)-1.56250e-02, (lut_t)0.00000e+00,  (lut_t)0.00000e+00,  (lut_t)1.56250e-02,
 (lut_t)1.56250e-02,  (lut_t)1.56250e-02,  (lut_t)1.56250e-02,  (lut_t)1.56250e-02,
 (lut_t)3.12500e-02,  (lut_t)3.12500e-02,  (lut_t)3.12500e-02,  (lut_t)3.12500e-02,
 (lut_t)4.68750e-02,  (lut_t)4.68750e-02,  (lut_t)4.68750e-02,  (lut_t)4.68750e-02,
 (lut_t)4.68750e-02,  (lut_t)4.68750e-02,  (lut_t)6.25000e-02,  (lut_t)6.25000e-02,
 (lut_t)6.25000e-02,  (lut_t)6.25000e-02,  (lut_t)6.25000e-02,  (lut_t)6.25000e-02,
 (lut_t)7.81250e-02,  (lut_t)7.81250e-02,  (lut_t)9.37500e-02,  (lut_t)1.09375e-01,
 (lut_t)1.25000e-01,  (lut_t)1.40625e-01,  (lut_t)1.40625e-01,  (lut_t)1.56250e-01,
 (lut_t)1.56250e-01,  (lut_t)1.71875e-01,  (lut_t)1.71875e-01,  (lut_t)1.71875e-01 
};

lut_t lut_lookup_0_0_3(lut_input_t input) {
    #pragma HLS BIND_STORAGE variable=lut_0_0_3 type=RAM_1P impl=LUTRAM
    return lut_0_0_3[value_to_index(input)];
} 