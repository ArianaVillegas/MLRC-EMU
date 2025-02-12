#!/bin/bash
#SBATCH --job-name=mi_trabajo1    # Nombre del trabajo
#SBATCH --output=mi_trabajo1.out  # Archivo de salida
#SBATCH --error=mi_trabajo1.err   # Archivo de error
#SBATCH --ntasks=2               # Número de tareas (procesos)
#SBATCH --cpus-per-task=1        # CPUs por tarea
#SBATCH --mem=7G                 # Memoria por nodo
#SBATCH --time=3-00:00:00        # Tiempo máximo de ejecución (day-hour:min:sec)
#SBATCH --partition=gpu      # Partición a usar
#SBATCH --mail-type=END,FAIL     # Cuando se enviará un mail
#SBATCH --mail-user=renzo.felix@utec.edu.pe


# Carga el entorno necesario
source ~/.bashrc                         # Asegúrate de que .bashrc tenga conda configurado
conda activate mi_entorno                # Activa el entorno conda


# Run your Python script inside the Singularity container
python3 ~/MLRC-EMU/src/EMU_release_pymarl/src/main.py --config=EMU_sc2 --env-config=sc2 with env_args.map_name=5m_vs_6m save_model=True

