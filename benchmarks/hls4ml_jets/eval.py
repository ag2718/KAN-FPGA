import numpy as np
import argparse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():

    parser = argparse.ArgumentParser(description="Evaluate performance and synthesis results of KAN network.")
    parser.add_argument('exp_name', help='Name of experiment (name of log file.)')
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

    # Write to the text file
    with open(f"{BASE_DIR}/logs/{args.exp_name}.txt", 'w') as f:
        f.write(f"Correct / Total: {correct} / {y_lbl.shape[0]} (Accuracy: {100 * correct / y_lbl.shape[0] :.2f}%)")

if __name__ == '__main__':
    main()