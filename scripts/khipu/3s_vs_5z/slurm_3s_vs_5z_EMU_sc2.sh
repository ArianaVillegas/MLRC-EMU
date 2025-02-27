#!/bin/bash
#SBATCH --job-name=3s_vs_5z_EMU_sc2
#SBATCH --output=3s_vs_5z/3s_vs_5z_EMU_sc2.out
#SBATCH --error=3s_vs_5z/3s_vs_5z_EMU_sc2.err
#SBATCH --partition=standard
#SBATCH --time=3-00:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=7G
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=renzo.felix@utec.edu.pe

source ~/.bashrc
source activate mi_entorno

export SC2PATH='/home/renzo.felix/pruebas/MLRC-EMU/src/EMU_release_pymarl/3rdparty/StarCraftII'


python3 /home/renzo.felix/pruebas/MLRC-EMU/src/EMU_release_pymarl/src/main.py --config=EMU_sc2 --env-config=sc2 with env_args.map_name=3s_vs_5z save_model=True
