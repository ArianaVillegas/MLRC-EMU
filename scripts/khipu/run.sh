#!/bin/bash

# Define the algorithm and maps
declare -A experiments

experiments=(
    [EMU_grf]="academy_3_vs_1_with_keeper academy_counterattack_easy academy_counterattack_hard"
    [EMU_grf_cds]="academy_3_vs_1_with_keeper academy_counterattack_easy academy_counterattack_hard"
)

# Define maps with indexes
declare -A map_indexes
map_indexes=(
    [1]="academy_3_vs_1_with_keeper"
    [2]="academy_counterattack_easy"
    [3]="academy_counterattack_hard"
)

# Get maps to execute from command-line arguments
selected_maps=()
for index in "$@"; do
    if [[ -n "${map_indexes[$index]}" ]]; then
        selected_maps+=("${map_indexes[$index]}")
    fi
done

if [ ${#selected_maps[@]} -eq 0 ]; then
    echo "No valid maps selected. Exiting."
    exit 1
fi

# SLURM job parameters
SBATCH_CPUS_PER_TASK=1  # Number of CPUs per task
SBATCH_MEM="7G"  # Memory allocation
SBATCH_PARTITION="gpu"  # Partition to submit the job
SBATCH_TIME="2-00:00:00"  # Max time limit
SBATCH_MAIL="undef@gmail.com"

# Paths (Use environment variables or set defaults)
RESULTS_DIR="${RESULTS_DIR:-/home/user/gf_khipu_results/results_bind}"
CONTAINER_PATH="${CONTAINER_PATH:-/home/user/khipu_gf/my_container}"
SCRIPT_PATH="${SCRIPT_PATH:-/workspace/EMU/src/EMU_release_pymarl/src/main.py}"

# Validate that the required paths exist
if [[ ! -d "$RESULTS_DIR" ]]; then
    echo "Error: RESULTS_DIR does not exist ($RESULTS_DIR)"
    exit 1
fi

if [[ ! -f "$CONTAINER_PATH" ]]; then
    echo "Error: CONTAINER_PATH does not exist ($CONTAINER_PATH)"
    exit 1
fi

for algorithm in "${!experiments[@]}"; do
    for map in ${experiments[$algorithm]}; do
        if [[ " ${selected_maps[@]} " =~ " ${map} " ]]; then
            mkdir -p "$map"
            JOB_NAME="${map}_${algorithm}"
            SCRIPT_NAME="$map/slurm_${JOB_NAME}.sh"

            cat <<EOT > "$SCRIPT_NAME"
#!/bin/bash
#SBATCH --job-name=$JOB_NAME
#SBATCH --output=$map/${JOB_NAME}.out
#SBATCH --error=$map/${JOB_NAME}.err
#SBATCH --partition=$SBATCH_PARTITION
#SBATCH --time=$SBATCH_TIME
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=$SBATCH_CPUS_PER_TASK
#SBATCH --mem=$SBATCH_MEM
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=$SBATCH_MAIL
#SBATCH --nodelist=g001

source ~/.bashrc
source activate emu

apptainer exec --nv --bind "$RESULTS_DIR:/workspace/EMU/src/EMU_release_pymarl/results" "$CONTAINER_PATH" python3 "$SCRIPT_PATH" --config=$algorithm --env-config=$map
EOT

            chmod +x "$SCRIPT_NAME"
            sbatch "$SCRIPT_NAME"
            sleep 5  # To avoid submitting jobs too fast
        fi
    done
done
