# MLRC Challenge: EMU

This repository contains experiments and extensions developed for the MLRC Challenge. The primary goal is to build upon existing methodologies to explore new approaches and improve performance on the MLRC tasks. Our work is inspired by and builds upon the EMU repository and paper.

## Project Overview

The MLRC Challenge aims to address the issue of reproducibility in machine learning research by providing a platform for researchers to validate and extend existing methodologies. The challenge involves replicating the results of a selected paper and then proposing extensions or improvements to the original work. Our project focuses on the EMU methodology, which leverages episodic memory to enhance cooperative multi-agent reinforcement learning (MARL) performance.

## EMU Repository and Paper

This work is based on the EMU methodology as described in:

- **Paper**: Efficient Episodic Memory Utilization of Cooperative Multi-Agent Reinforcement Learning
  - Authors: Hyungho Na, Yunkyeong Seo, Il-chul Moon
  - Published in: [ICLR 2024](https://iclr.cc/Conferences/2024)
  - Link: https://arxiv.org/abs/2403.01112

- **EMU Repository**: [GitHub Repository Link](https://github.com/HyunghoNa/EMU/tree/main).

## Contributions and Extensions

This repository includes:

- A systematic replication of the EMU framework Na et al. (2024), focusing on reproducible experiments while documenting implementation challenges and resource requirements. This validation effort strengthens the theoretical foundations of episodic control in MARL.
- Adaptation of the EMU framework for distributed computing environments, enabling scalable training across high-performance computing clusters while maintaining coordination efficiency. This extension demonstrates EMU’s potential for large-scale, computation-intensive MARL applications.
- A rigorous parametric analysis of the state embedding threshold (δ) unveils its pivotal role in dictating convergence and stability across diverse memory embedding techniques (Random Projection, EmbNet, and dCAE).


## Getting Started

### High Performance Computing (HPC) Setup with Apptainer 
1. Build the container in sandbox mode (for writable access):
    ```shell
    apptainer build --sandbox my_container docker://diegoran/emu:v2
    ```
2. Start an interactive shell session with writable access:
    ```shell
    apptainer shell --writable my_container
    ```
3. Activate the Conda Environment
    ```shell
    source activate base
    conda activate emu
    ```

4. Execute the Setup Script
    ```shell
    cd /workspace/EMU
    git pull origin main
    bash /workspace/EMU/docker/setup.sh
    ```

    ```shell
    export SC2PATH='/workspace/EMU/src/EMU_release_pymarl/3rdparty/StarCraftII'
    ```
5. Run an experiment.
   Before running the script, export the environment variables:
   ```shell
   # Set RESULTS_DIR to a writable directory outside the container, here will be saved the results of the experiments
   export RESULTS_DIR="/home/user/gf_khipu_results/results_bind"
   # Set CONTAINER_PATH to the path of the container
   export CONTAINER_PATH="/home/user/khipu_gf/my_container"            
   ```
    1. Individual Experiment
       ```shell
       cd scripts/khipu
       sbatch run_one.sh 
       ```
    2. Multiple Experiments. The following command will run EMU (QPLEX) and EMU (CDS) with the indexes of the maps you want to run. The available maps are: academy_3_vs_1_with_keeper (1), academy_counterattack_easy (2), academy_counterattack_hard (3). Ej: bash run.sh 1 2 3
       ```bash
       cd scripts/khipu
       bash run.sh {indexes of maps}
       ```
       

### Local Setup wih Docker
1. Pull the Docker Image
    ```shell
    docker pull diegoran/emu:v2
    ```
2. Run the Docker Container
   * With GPU Support (if available):

     ```shell
     docker run -it --gpus all diegoran/emu:v2
     ```
   * Without GPU Support:
     ```shell
     docker run -it diegoran/emu:v2
     ```

3. Start the Container and Access the Terminal
    ```shell
    docker start <container_id>
    
    docker exec -it <container_id> bash
    ```

4. Activate the Conda Environment
    ```shell
    source activate base
    conda activate emu
    ```

5. Execute the Setup Script
    ```shell
    cd /workspace/EMU
    git pull origin main
    bash /workspace/EMU/docker/setup.sh
    ```

    ```shell
    export SC2PATH='/workspace/EMU/src/EMU_release_pymarl/3rdparty/StarCraftII'
    ```
6. Run an experiment. 
    ```shell
    cd /workspace/EMU/src/EMU_release_pymarl/
    ```
    1. To train EMU(QPLEX) on SC2 setting tasks, run the following command. For EMU(CDS), please change config file to EMU_sc2_cds.
       ```shell
       # SC2 
       python3 src/main.py --config=EMU_sc2 --env-config=sc2 with env_args.map_name=5m_vs_6m
       ```
    2. To train EMU(QPLEX) on Google Research Football setting tasks, run the following command. For EMU(CDS), please change config file to EMU_grf_cds.
       ```shell
       # GFootball
       python3 src/main.py --config=EMU_grf --env-config=academy_3_vs_1_with_keeper
       ```


### Local Setup and High Performance Computing (HPC) Setup (without Google Research Football)
> **Note**: The following instructions are for setting up the repository on a local machine or an HPC cluster without Google Research Football. For Google Research Football, please refer to the Docker setup instructions.
1. Clone the repository:
   ```bash
   git clone https://github.com/ArianaVillegas/MLRC-EMU.git
   cd MLRC-EMU
   git checkout FabryzzioMezaBranch
   ```
2. Install Python packages:
   ```bash
   conda create -n emu python=3.8 -y
   conda activate emu
   
   bash scripts/setup/install_dependencies.sh
    ```
3. Set up StarCraft II  and SMAC:
   ```bash
    cd src
    pip install -e EMU_smac_env
  
    cd EMU_release_pymarl
    bash install_sc2.sh
   ```
4. Set the environment variables:
   > **Note: Replace** PATH_TO_MLRC-EMU with the actual location where you cloned the repository.
   ```bash
   export SC2PATH='PATH_TO_MLRC-EMU/src/EMU_release_pymarl/3rdparty/StarCraftII'
   ```
5. Install additional dependencies:
   ```bash
   # Navigate to the root directory of the repository
   bash scripts/setup/additional_dependencies.sh
   ```
6. Run the experiments:
    1. In a local environment:
         ```bash
          # Navigate to the root directory of the repository
          cd src/EMU_release_pymarl/
          python3 src/main.py --config=EMU_sc2 --env-config=sc2 with env_args.map_name=5m_vs_6m save_model=True
         ```
    2. In a distributed environment (High Performance Computing (HPC) cluster with Slurm):
          > **Note: Replace** PATH_TO_MLRC-EMU in the line 50 in 'scripts/khipu/run_smac.sh' with the actual location where you cloned the repository.
       1. Run the following commands:
          ```bash
           # From the root directory of the repository
           cd scripts/khipu
          ```
       2. The following command will run EMU (QPLEX) and EMU (CDS) with the indexes of the maps you want to run. The available maps are: 1c3s5z (1), 3s_vs_5z (2), 5m_vs_6m (3), 3s5z_vs_3s6z (4), 6h_vs_8z (5), MMM2 (6). Ej: bash run_smac.sh 1 2 3
          ```bash
          bash run_smac.sh {indexes of maps}
          ```
##  Results
The results of the experiments are saved in the `src/EMU_release_pymarl/results` directory. Some of the obtained results are included in the `results` directory of this repository.

## Acknowledgments

We acknowledge the authors of the EMU paper and repository for their foundational work, which has been the base of our approach to the MLRC Challenge.

## License

This project is licensed under the MIT. See the `LICENSE` file for details.
