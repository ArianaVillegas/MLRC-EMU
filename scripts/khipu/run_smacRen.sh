#!/bin/bash

# Define the algorithm and maps
declare -A experiments

experiments=(
    [EMU_sc2]="1c3s5z 3s_vs_5z 5m_vs_6m"
    #[EMU_sc2_cds]="1c3s5z 3s_vs_5z 5m_vs_6m"
    #[EMU_sc2_hard_3s5z_vs_3s6z]="3s5z_vs_3s6z"
    #[EMU_sc2_hard_cds_3s5z_vs_3s6z]="3s5z_vs_3s6z"
    #[EMU_sc2_hard_6h_vs_8z]="6h_vs_8z"
    #[EMU_sc2_hard_cds_6h_vs_8z]="6h_vs_8z"
    #[EMU_sc2_hard_cds_MMM2]="MM2"
    #[EMU_sc2_hard_MMM2]="MM2"
)

# Define maps with indexes
declare -A map_indexes
map_indexes=(
    [1]="1c3s5z"
    [2]="3s_vs_5z"
    [3]="5m_vs_6m"
    [4]="3s5z_vs_3s6z"
    [5]="6h_vs_8z"
    [6]="MM2"
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
SBATCH_PARTITION="standard"  # Partition to submit the job
SBATCH_TIME="3-00:00:00"  # Max time limit
SBATCH_MAIL="renzo.felix@utec.edu.pe"


PATH_PYMARL="$HOME/pruebas/MLRC-EMU/src/EMU_release_pymarl"

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
#SBATCH --nodelist=n005

source ~/.bashrc
source activate mi_entorno

export SC2PATH='$PATH_PYMARL/3rdparty/StarCraftII'


python3 $PATH_PYMARL/src/main.py --config=$algorithm --env-config=sc2 with env_args.map_name=$map save_model=True
EOT

            chmod +x "$SCRIPT_NAME"
            sbatch "$SCRIPT_NAME"
            sleep 20  # To avoid submitting jobs too fast
        fi
    done
done
