import subprocess
import itertools
import os
import re

BENCHMARK = "hls4ml_jets"
MODELS_DIR = "/home/aarushg/KAN-FPGA/benchmarks/hls4ml_jets/models"

model_files = os.listdir(MODELS_DIR)

# Extract parameters from filenames using regex
pattern = re.compile(r'model(.*)_(\d+)t(\d+)f_pr([\d.]+)\.pth')
extracted_params = []
for filename in model_files:
    match = pattern.match(filename)
    if match:
        exp_name, tot_precision, float_precision, prune_ratio = match.groups()
        tot_precision, float_precision = int(tot_precision), int(float_precision)
        prune_ratio = float(prune_ratio)
        extracted_params.append((exp_name, tot_precision, float_precision, prune_ratio))

# Run generate_and_eval.py for each configuration
for (exp_name, tot_precision, float_precision, prune_ratio) in extracted_params:

    resolution = 2**tot_precision
    int_precision = tot_precision - float_precision
    grid_range = [-2**(int_precision - 1), 2**(int_precision - 1)]

    cmd = [
        "python", "generate_and_eval.py",
        "--resolution", str(resolution),
        "--grid_range", str(grid_range[0]), str(grid_range[1]),
        "--tot_precision", str(tot_precision),
        "--float_precision", str(float_precision),
        "--benchmark", BENCHMARK,
        "--model_path", f"{MODELS_DIR}/model{exp_name}_{tot_precision}t{float_precision}f_pr{prune_ratio}.pth",
        "--exp_name", exp_name,
        "--prune_ratio", str(1 - prune_ratio)
    ]
    
    print(f"\nRunning configuration:")
    print(f"Experiment name: {exp_name}")
    print(f"Resolution: {resolution}")
    print(f"Total precision: {tot_precision}")
    print(f"Float precision: {float_precision}")
    print(f"Prune ratio: {1 - prune_ratio}")
    
    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error running configuration: {e}")
        continue

print("\nParameter search completed")