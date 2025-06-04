import os
import argparse
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(BASE_DIR)

parser = argparse.ArgumentParser(description="Synthesize and evaluate KAN network.")
parser.add_argument('--benchmark', help='Benchmark on which synthesis and evaluation is being performed.')
parser.add_argument('--model_path', type=str, default=None, help='Path to the model file (default: kan.pt in benchmark folder)')

parser.add_argument('--resolution', type=int, default=256, help='Resolution for activation values')
parser.add_argument('--grid_range', type=int, nargs=2, default=[-8, 8], help='Grid range as two integers (MUST BE THE SAME AS TRAIN TIME)')
parser.add_argument('--tot_precision', type=int, default=16, help='Total bit precision')
parser.add_argument('--float_precision', type=int, default=6, help='Floating bit precision')
parser.add_argument('--prune_ratio', type=float, default=0.0, help='Pruning ratio')
parser.add_argument('--exp_name', type=str, default=None, help='Experiment name')

args = parser.parse_args()

if args.model_path is not None:
    MODEL_PATH = args.model_path
else:
    MODEL_PATH = f"{BASE_DIR}/benchmarks/{args.benchmark}/kan.pt"

OUTPUT_DIR = f"{BASE_DIR}/benchmarks/{args.benchmark}/firmware"


#### GENERATE KAN CPP FILES ####
os.system(f"python {BASE_DIR}/generate_kan_cpp/main.py --model_path {MODEL_PATH} --resolution {args.resolution} --grid_range {args.grid_range[0]} {args.grid_range[1]} --tot_precision {args.tot_precision} --float_precision {args.float_precision} --output_dir {OUTPUT_DIR} --prune_fraction {args.prune_ratio}")
print(f"KAN CPP code generated at {OUTPUT_DIR}!")

#################################


### PERFORM EVAL USING BENCHMARK-SPECIFIC SCRIPT ###

EXP_NAME = (args.exp_name if args.exp_name is not None else "") + f"res{args.resolution}_gr{args.grid_range[0]},{args.grid_range[1]}_tp{args.tot_precision}_fp{args.float_precision}_pr{args.prune_ratio}"

os.system(f"python {BASE_DIR}/benchmarks/{args.benchmark}/eval.py {EXP_NAME} --header res tp fp pr --data {args.resolution} {args.tot_precision} {args.float_precision} {args.prune_ratio}")
print(f"Results (benchmark {args.benchmark}, config {EXP_NAME})")
print(f"------------------------------------------")
with open(f"{BASE_DIR}/benchmarks/{args.benchmark}/logs/{EXP_NAME}.txt", 'r') as f:
    print(f.read())