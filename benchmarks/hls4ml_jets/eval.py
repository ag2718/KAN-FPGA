import numpy as np
import argparse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def table_to_csv(header_lines, data_line):
    """
    Returns list of header, list of data
    """
    
    header_lines_split = [line.split("|") for line in header_lines]
    data_columns = []
    for col in range(len(header_lines_split[0])):
        column = [row[col].replace(" ", "") for row in header_lines_split]
        column = [x for x in column if len(x) > 0]
        data_columns.append(''.join(column))

    return data_columns, data_line.replace("+", "").replace("-", "").replace(" ", "").replace("(~0%)", "").split("|")


def main():

    parser = argparse.ArgumentParser(description="Evaluate performance and synthesis results of KAN network.")
    parser.add_argument('exp_name', help='Name of experiment (name of log file.)')
    parser.add_argument('--header', nargs='+', help='List of header columns', default=[])
    parser.add_argument('--data', nargs='+', help='List of data values', default=[])
    args = parser.parse_args()

    # Produce testbench data in valid form

    x_test = np.load(f"{BASE_DIR}/data/X_test.npy")

    with open(f"{BASE_DIR}/tb_inputs.dat", 'w') as f:
        for row in x_test:
            row_str = ' '.join(map(str, row))
            f.write(row_str + '\n')

    # Compile and run CPP code

    print(f"g++ -I {BASE_DIR}/firmware/KAN -I /home/aarushg/KAN-FPGA/HLS_arbitrary_Precision_Types/include -I /home/aarushg/KAN-FPGA/hls-lib-stream {BASE_DIR}/run_kan.cpp")

    os.system(f"g++ -I {BASE_DIR}/firmware -I /home/aarushg/KAN-FPGA/HLS_arbitrary_Precision_Types/include -I /home/aarushg/KAN-FPGA/hls-lib-stream {BASE_DIR}/run_kan.cpp")
    os.system(f"./a.out {BASE_DIR}/tb_inputs.dat {BASE_DIR}/tb_kan_outputs.dat")
    os.system(f"rm a.out")

    y_lbl = np.load(f"{BASE_DIR}/data/y_test.npy")
    y_pred = np.loadtxt(f"{BASE_DIR}/tb_kan_outputs.dat")

    # Count matching argmax indices
    correct = np.sum(np.argmax(y_lbl, axis=1) == np.argmax(y_pred, axis=1))

    os.system(f"rm {BASE_DIR}/tb_inputs.dat {BASE_DIR}/tb_kan_outputs.dat")

    header = args.header
    data = args.data
    
    header.extend(["correct", "total"])
    data.extend(map(str, [correct, y_lbl.shape[0]]))

    print(header, data)

    # # Write to the text file
    # with open(f"{BASE_DIR}/logs/{args.exp_name}.txt", 'w') as f:
    #     f.write(f"correct,total\n{correct},{y_lbl.shape[0]}\n")

    os.chdir(f"{BASE_DIR}/firmware")
    os.system(f"vitis_hls {BASE_DIR}/firmware/KAN.tcl")

    with open(f"{BASE_DIR}/firmware/KAN/solution1/syn/report/csynth.rpt", "r") as synth_rep_file:
        contents = synth_rep_file.read().split("\n")
        new_header, new_data = table_to_csv(contents[18:20], contents[21])
        print(new_header, new_data)
        header.extend(new_header)
        data.extend(new_data)

    header, data = zip(*[(h, d) for h, d in zip(header, data) if h and d])
    header, data = list(header), list(data)

    with open(f"{BASE_DIR}/logs/{args.exp_name}.txt", 'w') as f:
        f.write(f"{','.join(header)}\n{','.join(data)}")

if __name__ == '__main__':
    main()