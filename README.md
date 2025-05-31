# KAN-FPGA

This repository provides tools for generating, synthesizing, and evaluating KAN networks on FPGAs, as well as performing parameter sweeps for design exploration.

## Main Scripts and Workflows

### 1. Synthesize and Evaluate a KAN Network

Use `generate_and_eval.py` to:
- Generate C++/HLS code for a KAN model
- Synthesize and evaluate the model on a specified benchmark

#### **Usage:**
```sh
python generate_and_eval.py --benchmark <benchmark_name> [--model_path <path/to/model.pt>] [--resolution <int>] [--grid_range <low> <high>] [--tot_precision <int>] [--float_precision <int>] [--prune_ratio <float>]
```

#### **Arguments:**
- `--benchmark` (required): Name of the benchmark (e.g., `hls4ml_jets`, `anomaly_detection`).
- `--model_path`: Path to the PyTorch model file. Defaults to `kan.pt` in the benchmark folder.
- `--resolution`: Resolution for activation values (default: 256).
- `--grid_range`: Range for the activation grid (default: -8 8). **Must match training.**
- `--tot_precision`: Total bit precision for quantization (default: 16).
- `--float_precision`: Number of floating point bits (default: 6).
- `--prune_ratio`: Fraction of weights to prune (default: 0.0).

#### **What it does:**
- Generates C++ code for the KAN model in the benchmark's `firmware/` directory.
- Runs synthesis and evaluation using the benchmark's `eval.py` script.
- Prints results and saves logs in the benchmark's `logs/` directory.

#### **Example:**
```sh
python generate_and_eval.py --benchmark anomaly_detection --resolution 128 --grid_range -8 8 --tot_precision 12 --float_precision 6 --prune_ratio 0.2
```

---

### 2. Parameter Search

Use `run_parameter_search.py` to:
- Sweep over multiple combinations of resolution, precision, and pruning parameters
- Automatically run synthesis and evaluation for each configuration

#### **Usage:**
Edit the parameter lists at the top of `run_parameter_search.py` to set the desired sweep ranges, then run:
```sh
python run_parameter_search.py
```

#### **What it does:**
- Iterates over all valid parameter combinations
- Calls `generate_and_eval.py` for each configuration
- Prints results for each run

---

## Output
- Generated C++/HLS code is placed in `benchmarks/<benchmark>/firmware/`
- Evaluation logs are saved in `benchmarks/<benchmark>/logs/`

---

## Notes
- Make sure your model and grid range match between training and synthesis.
- For custom models, specify the path with `--model_path`.