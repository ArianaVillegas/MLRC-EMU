#!/bin/bash
#SBATCH --job-name=C-Last-hard
#SBATCH --output=%x/%j_%t.out
#SBATCH --error=%x/%j_%t.err
#SBATCH --partition=gpu
#SBATCH --time=2-00:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=7G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=undef@gmail.com


source ~/.bashrc
source activate emu

# Set user-specific variables
RESULTS_DIR="${RESULTS_DIR:-/path/to/results}"
CONTAINER_PATH="${CONTAINER_PATH:-/path/to/container.sif}"
SCRIPT_PATH="${SCRIPT_PATH:-/workspace/EMU/src/EMU_release_pymarl/src/main.py}"
CONFIG="EMU_grf_cds"
ENV_CONFIG="academy_counterattack_hard"

# Run the command with Apptainer
CUDA_VISIBLE_DEVICES=0 apptainer exec --nv \
    --bind "$RESULTS_DIR:/workspace/EMU/src/EMU_release_pymarl/results" \
    "$CONTAINER_PATH" \
    python3 "$SCRIPT_PATH" --config="$CONFIG" --env-config="$ENV_CONFIG"