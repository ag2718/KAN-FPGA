#include "lut_0_0_0.h"
#include "value_to_index.h"

const lut_t lut_0_0_0[LUT_SIZE] = {
  (lut_t)0.00000e+00,  (lut_t)0.00000e+00,  (lut_t)0.00000e+00,  (lut_t)0.00000e+00,
 (lut_t)0.00000e+00,  (lut_t)0.00000e+00, (lut_t)0.00000e+00, (lut_t)0.00000e+00,
(lut_t)0.00000e+00, (lut_t)0.00000e+00, (lut_t)0.00000e+00, (lut_t)-1.56250e-02,
(lut_t)-1.56250e-02, (lut_t)-1.56250e-02, (lut_t)-1.56250e-02, (lut_t)-1.56250e-02,
(lut_t)-1.56250e-02, (lut_t)-1.56250e-02, (lut_t)-1.56250e-02, (lut_t)-3.12500e-02,
(lut_t)-3.12500e-02, (lut_t)-4.68750e-02, (lut_t)-6.25000e-02, (lut_t)-7.81250e-02,
(lut_t)-7.81250e-02, (lut_t)-9.37500e-02, (lut_t)-9.37500e-02, (lut_t)-9.37500e-02,
(lut_t)-7.81250e-02, (lut_t)-6.25000e-02, (lut_t)-4.68750e-02, (lut_t)-3.12500e-02,
(lut_t)0.00000e+00,  (lut_t)1.56250e-02,  (lut_t)4.68750e-02,  (lut_t)7.81250e-02,
 (lut_t)1.09375e-01,  (lut_t)1.40625e-01,  (lut_t)1.71875e-01,  (lut_t)2.18750e-01,
 (lut_t)2.50000e-01,  (lut_t)2.81250e-01,  (lut_t)3.28125e-01,  (lut_t)3.59375e-01,
 (lut_t)4.06250e-01,  (lut_t)4.53125e-01,  (lut_t)4.84375e-01,  (lut_t)5.31250e-01,
 (lut_t)5.78125e-01,  (lut_t)6.09375e-01,  (lut_t)6.56250e-01,  (lut_t)6.87500e-01,
 (lut_t)7.18750e-01,  (lut_t)7.50000e-01,  (lut_t)7.96875e-01,  (lut_t)8.28125e-01,
 (lut_t)8.75000e-01,  (lut_t)9.06250e-01,  (lut_t)9.53125e-01,  (lut_t)9.84375e-01,
 (lut_t)1.01562e+00,  (lut_t)1.04688e+00,  (lut_t)1.06250e+00,  (lut_t)1.09375e+00 
};

lut_t lut_lookup_0_0_0(lut_input_t input) {
    #pragma HLS BIND_STORAGE variable=lut_0_0_0 type=RAM_1P impl=LUTRAM
    return lut_0_0_0[value_to_index(input)];
} 