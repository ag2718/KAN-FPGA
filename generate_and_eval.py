import os
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="Synthesize and evaluate KAN network.")
parser.add_argument('--benchmark', help='Benchmark on which synthesis and evaluation is being performed.')

parser.add_argument('--resolution', type=int, default=256, help='Resolution for activation values')
parser.add_argument('--grid_range', type=int, nargs=2, default=[-8, 8], help='Grid range as two integers (MUST BE THE SAME AS TRAIN TIME)')
parser.add_argument('--tot_precision', type=int, default=16, help='Total bit precision')
parser.add_argument('--float_precision', type=int, default=6, help='Floating bit precision')

args = parser.parse_args()

MODEL_PATH = f"{BASE_DIR}/benchmarks/{args.benchmark}/kan.pt"
OUTPUT_DIR = f"{BASE_DIR}/benchmarks/{args.benchmark}/firmware"


#### GENERATE KAN CPP FILES ####
os.system(f"python {BASE_DIR}/generate_kan_cpp/main.py --model_path {MODEL_PATH} --resolution {args.resolution} --grid_range {args.grid_range[0]} {args.grid_range[1]} --tot_precision {args.tot_precision} --float_precision {args.float_precision} --output_dir {OUTPUT_DIR}")
print(f"KAN CPP code generated at {OUTPUT_DIR}!")

#################################


### PERFORM EVAL USING BENCHMARK-SPECIFIC SCRIPT ###

EXP_NAME = f"res{args.resolution}_gr{args.grid_range[0]},{args.grid_range[1]}_tp{args.tot_precision}_fp{args.float_precision}"
os.system(f"python {BASE_DIR}/benchmarks/{args.benchmark}/eval.py {EXP_NAME}")
print(f"Results (benchmark {args.benchmark}, config {EXP_NAME})")
print(f"------------------------------------------")
with open(f"{BASE_DIR}/benchmarks/{args.benchmark}/logs/{EXP_NAME}.txt", 'r') as f:
    print(f.read())