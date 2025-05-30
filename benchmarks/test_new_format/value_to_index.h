#ifndef VALUE_TO_INDEX_H
#define VALUE_TO_INDEX_H

inline int value_to_index(lut_input_t value) {
    int data_round = (value * LUT_SIZE) >> 3;
    int index = data_round + ((4 * LUT_SIZE) >> 3);
    return index;
}

#endif 