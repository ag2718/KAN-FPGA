import numpy as np
import argparse
import os
import sys
from sklearn import metrics
import common as com

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

# Helper to parse synthesis report (copied from hls4ml_jets/eval.py)
def table_to_csv(header_lines, data_line):
    header_lines_split = [line.split("|") for line in header_lines]
    data_columns = []
    for col in range(len(header_lines_split[0])):
        column = [row[col].replace(" ", "") for row in header_lines_split]
        column = [x for x in column if len(x) > 0]
        data_columns.append(''.join(column))
    return data_columns, data_line.replace("+", "").replace("-", "").replace(" ", "").replace("(~0%)", "").split("|")

def main():
    parser = argparse.ArgumentParser(description="Evaluate KAN anomaly detection on hardware.")
    parser.add_argument('exp_name', help='Name of experiment (name of log file.)')
    parser.add_argument('--header', nargs='+', help='List of header columns', default=[])
    parser.add_argument('--data', nargs='+', help='List of data values', default=[])

    args = parser.parse_args()

    param = com.yaml_load()
    mode = True  # Always development mode for metrics
    dirs = com.select_dirs(param=param, mode=mode)

    header = args.header
    data = args.data

    aucs = []
    paucs = []

    # Prepare log directory and file
    logs_dir = os.path.join(BASE_DIR, 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, f"{args.exp_name}.txt")

    # Compile and run firmware
    firmware_dir = os.path.abspath(os.path.join(BASE_DIR, 'firmware'))
    cpp_path = os.path.join(firmware_dir, 'KAN.cpp')
    includes = f"-I {firmware_dir} -I /home/aarushg/KAN-FPGA/HLS_arbitrary_Precision_Types/include -I /home/aarushg/KAN-FPGA/hls-lib-stream"
    os.system(f"g++ {includes} {cpp_path}")
    tb_outputs_path = os.path.join(BASE_DIR, "tb_kan_outputs.dat")

    for idx, target_dir in enumerate(dirs):

        machine_type = os.path.split(target_dir)[1]
        machine_id_list = com.get_machine_id_list_for_test(target_dir)

        for id_str in machine_id_list:
            test_files, y_true = com.test_file_list_generator(target_dir, id_str, mode)
            if len(test_files) == 0:
                continue
            # Extract features for all test files and write to tb_inputs.dat
            all_vectors = []
            for file_path in test_files:
                data = com.file_to_vector_array(
                    file_path,
                    n_mels=param["feature"]["n_mels"],
                    frames=param["feature"]["frames"],
                    n_fft=param["feature"]["n_fft"],
                    hop_length=param["feature"]["hop_length"],
                    power=param["feature"]["power"]
                )
                all_vectors.append(data)
            # Concatenate all feature vectors
            all_vectors = np.concatenate(all_vectors, axis=0)
            tb_inputs_path = os.path.join(BASE_DIR, "tb_inputs.dat")
            with open(tb_inputs_path, 'w') as f:
                for row in all_vectors:
                    row_str = ' '.join(map(str, row))
                    f.write(row_str + '\n')
            os.system(f"./a.out {tb_inputs_path} {tb_outputs_path}")
            # Read predictions
            y_pred = np.loadtxt(tb_outputs_path)
            os.remove(tb_inputs_path)
            os.remove(tb_outputs_path)

            # Compute anomaly scores (mean squared error per file)
            # Need to map predictions back to files
            # Assume each file's feature vectors are contiguous in all_vectors and y_pred
            file_lengths = [com.file_to_vector_array(
                file_path,
                n_mels=param["feature"]["n_mels"],
                frames=param["feature"]["frames"],
                n_fft=param["feature"]["n_fft"],
                hop_length=param["feature"]["hop_length"],
                power=param["feature"]["power"]
            ).shape[0] for file_path in test_files]
            anomaly_scores = []
            idx_start = 0
            for flen in file_lengths:
                idx_end = idx_start + flen
                # Compute mean squared error for this file
                x = all_vectors[idx_start:idx_end]
                y = y_pred[idx_start:idx_end]
                errors = np.mean((x - y) ** 2, axis=1)
                anomaly_scores.append(np.mean(errors))
                idx_start = idx_end
            # Compute metrics
            auc = metrics.roc_auc_score(y_true, anomaly_scores)
            p_auc = metrics.roc_auc_score(y_true, anomaly_scores, max_fpr=param["max_fpr"])
            aucs.append(auc)
            paucs.append(p_auc)
            print(f"Machine {machine_type} ID {id_str}: AUC={auc}, pAUC={p_auc}")

    os.system("rm a.out")
    
    # Prepare header and data for log file
    header = ["AUC", "pAUC"]
    data = [str(np.mean(aucs)), str(np.mean(paucs))]
    
    os.chdir(f"{BASE_DIR}/firmware")
    os.system(f"vitis_hls KAN.tcl")

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

