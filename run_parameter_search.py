import subprocess
import itertools

# Parameter ranges to search
# resolutions = [32, 64, 128, 256, 512]
# total_precisions = [8, 12, 16]  
# float_precisions = [4, 6, 8]

grid_range = [-4, 4]

resolutions = [64, 128, 256]
#total_precisions = [4, 6, 8, 10, 12]
total_precisions = [7]
float_precisions = [3]
# float_precisions = [2, 3, 4, 5, 6]
prune_ratios = [0.0, 0.2, 0.4, 0.6, 0.8]

# Generate all combinations of parameters
configs = list(itertools.product(resolutions, total_precisions, float_precisions, prune_ratios))

# Run generate_and_eval.py for each configuration
for resolution, tot_precision, float_precision, prune_ratio in configs:
    # Skip invalid configurations where float_precision > tot_precision
    if float_precision >= tot_precision:
        continue
        
    cmd = [
        "python", "generate_and_eval.py",
        "--resolution", str(resolution),
        "--grid_range", str(grid_range[0]), str(grid_range[1]),
        "--tot_precision", str(tot_precision),
        "--float_precision", str(float_precision),
        "--benchmark", "hls4ml_jets",
        "--prune_ratio", str(prune_ratio)
    ]
    
    print(f"\nRunning configuration:")
    print(f"Resolution: {resolution}")
    print(f"Total precision: {tot_precision}")
    print(f"Float precision: {float_precision}")
    print(f"Prune ratio: {prune_ratio}")
    
    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error running configuration: {e}")
        continue

print("\nParameter search completed")