#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <vector>

#include <KAN.cpp>
#include <defines.h>

// hls-fpga-machine-learning insert braear

namespace nnet
{
    bool trace_enabled = true;
    std::map<std::string, void *> *trace_outputs = NULL;
    size_t trace_type_size = sizeof(double);
} // namespace nnet

int main(int argc, char **argv)
{
    // hls-fpga-machine-learning insert namespace

    // load input data from text file
    std::ifstream fin(argv[1]);
    std::ofstream fout(argv[2]);

    std::string iline;
    std::string lline;
    int e = 0;

    int correct = 0, total = 0;

    if (fin.is_open())
    {
        while (std::getline(fin, iline))
        {
            char *cstr = const_cast<char *>(iline.c_str());
            char *current;

            // std::vector<input_t> in;
            input_t in[N_INPUT];
            current = strtok(cstr, " ");
            for (int i = 0; i < N_INPUT; i++)
            {
                in[i] = atof(current);

            // std::cout << "Input: ";
            // std::cout << in[i] << " ";
            // std::cout << std::endl;

                current = strtok(NULL, " ");
            }

            // hls-fpga-machine-learning insert data
            result_t pr[N_OUTPUT];
            KAN(in, pr);

            for (int i = 0; i < N_OUTPUT; i++)
            {
                fout << pr[i] << " ";
            }
            fout << "\n";

            e++;

            // hls-fpga-machine-learning insert tb-output
        }
        fin.close();
    }
    else
    {
        std::cout << "INFO: Unable to open input/predictions file." << std::endl;
        fout.close();
        return 1;

        // hls-fpga-machine-learning insert zero

        // hls-fpga-machine-learning insert top-level-function

        // hls-fpga-machine-learning insert output

        // hls-fpga-machine-learning insert tb-output
    }

    fout.close();

    return 0;
}