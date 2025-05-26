import subprocess
import itertools

# Parameter ranges to search
# resolutions = [32, 64, 128, 256, 512]
# total_precisions = [8, 12, 16]  
# float_precisions = [4, 6, 8]

resolutions = [64, 128, 256]
total_precisions = [6]
float_precisions = [3]
grid_range = [-8, 8]

# Generate all combinations of parameters
configs = list(itertools.product(resolutions, total_precisions, float_precisions))

# Run generate_and_eval.py for each configuration
for resolution, tot_precision, float_precision in configs:
    # Skip invalid configurations where float_precision > tot_precision
    if float_precision >= tot_precision:
        continue
        
    cmd = [
        "python", "generate_and_eval.py",
        "--resolution", str(resolution),
        "--grid_range", str(grid_range[0]), str(grid_range[1]),
        "--tot_precision", str(tot_precision),
        "--float_precision", str(float_precision),
        "--benchmark", "hls4ml_jets"
    ]
    
    print(f"\nRunning configuration:")
    print(f"Resolution: {resolution}")
    print(f"Total precision: {tot_precision}")
    print(f"Float precision: {float_precision}")
    
    try:
        subprocess.run(cmd)
    except subprocess.CalledProcessError as e:
        print(f"Error running configuration: {e}")
        continue

print("\nParameter search completed")