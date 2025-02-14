#!/bin/bash

# Define el algoritmo y los mapas
declare -A experiments
experiments=(
    [EMU_sc2]="1c3s5z 3s_vs_5z 5m_vs_6m"
    [EMU_sc2_cds]="1c3s5z 3s_vs_5z 5m_vs_6m"
    [EMU_sc2_hard_3s5z_vs_3s6z]="3s5z_vs_3s6z"
    [EMU_sc2_hard_cds_3s5z_vs_3s6z]="3s5z_vs_3s6z"
    [EMU_sc2_hard_6h_vs_8z]="6h_vs_8z"
    [EMU_sc2_hard_cds_6h_vs_8z]="6h_vs_8z"
    [EMU_sc2_hard_cds_MMM2]="MM2"
    [EMU_sc2_hard_MMM2]="MM2"
)

# Define los mapas con índices
declare -A map_indexes
map_indexes=(
    [1]="1c3s5z"
    [2]="3s_vs_5z"
    [3]="5m_vs_6m"
    [4]="3s5z_vs_3s6z"
    [5]="6h_vs_8z"
    [6]="MM2"
)

# Obtiene los mapas a ejecutar desde los argumentos de la línea de comandos
selected_maps=()
for index in "$@"; do
    if [[ -n "${map_indexes[$index]}" ]]; then
        selected_maps+=("${map_indexes[$index]}")
    fi
done

if [ ${#selected_maps[@]} -eq 0 ]; then
    echo "No se seleccionó ningún mapa válido. Saliendo."
    exit 1
fi

# Ruta a la carpeta de PyMARL
PATH_PYMARL="$HOME/MLRC-EMU/src/EMU_release_pymarl"

for algorithm in "${!experiments[@]}"; do
    for map in ${experiments[$algorithm]}; do
        if [[ " ${selected_maps[@]} " =~ " ${map} " ]]; then
            mkdir -p "$map"
            JOB_NAME="${map}_${algorithm}"
            LOG_OUT="$map/${JOB_NAME}.out"
            LOG_ERR="$map/${JOB_NAME}.err"

            # Comando a ejecutar localmente (sin SLURM)
            CMD="source ~/.bashrc; source activate emu; export SC2PATH='$PATH_PYMARL/3rdparty/StarCraftII'; python3 $PATH_PYMARL/src/main.py --config=$algorithm --env-config=sc2 with env_args.map_name=$map save_model=True"

            echo "Ejecutando: $CMD"
            # Ejecuta el comando en segundo plano, redirigiendo salida y error
            bash -c "$CMD" > "$LOG_OUT" 2> "$LOG_ERR" &
            sleep 20  # Para evitar lanzar demasiados procesos a la vez
        fi
    done
done

wait
