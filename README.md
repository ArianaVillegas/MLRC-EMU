# MLRC Challenge: EMU

This repository contains experiments and extensions developed for the MLRC Challenge. The primary goal is to build upon existing methodologies to explore new approaches and improve performance on the MLRC tasks. Our work is inspired by and builds upon the EMU repository and paper.

## Project Overview

The MLRC Challenge aims to address [...].

## EMU Repository and Paper

This work is based on the EMU methodology as described in:

- **Paper**: Efficient Episodic Memory Utilization of Cooperative Multi-Agent Reinforcement Learning
  - Authors: Hyungho Na, Yunkyeong Seo, Il-chul Moon
  - Published in: [ICLR 2024](https://iclr.cc/Conferences/2024)
  - Link: https://arxiv.org/abs/2403.01112

- **EMU Repository**: [GitHub Repository Link](https://github.com/HyunghoNa/EMU/tree/main).

## Getting Started

### Prerequisites

1. Install dependencies:
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

source activate base
conda create -n emu python=3.8 -y
conda activate emu


git clone https://github.com/ArianaVillegas/MLRC-EMU.git
cd MLRC-EMU
git checkout FabryzzioMezaBranch

conda install -n emu pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch -y
conda install -n emu anaconda::scikit-learn -y
conda install -n emu anaconda::py-boost -y

# Install pip packages
pip install --upgrade psutil wheel pytest
pip install gfootball==2.10.2 gym==0.11
pip install scipy matplotlib seaborn pyyaml==5.3.1 pygame pytest probscale imageio snakeviz tensorboard-logger
    
# Install Python dependencies

pip install protobuf==3.19.6 
conda install -y -c conda-forge sacred 
conda install -y -c anaconda pymongo 
pip3 install numpy==1.23.1


cd ~/MLRC-EMU/src
pip install -e EMU_smac_env

cd ~/MLRC-EMU/src/EMU_release_pymarl
bash install_sc2.sh


export SC2PATH='~/MLRC-EMU/src/EMU_release_pymarl/3rdparty/StarCraftII'

pip install protobuf==3.19.6

conda install -y -c conda-forge sacred
```

### Running Experiments

Experiments are organized in the `experiments/` folder. To run a specific experiment, follow these steps:

1. [Step-by-step instructions for running an experiment, e.g.,]
```bash
cd ~/MLRC-EMU/src/EMU_release_pymarl/
python3 ~/MLRC-EMU/src/EMU_release_pymarl/src/main.py --config=EMU_sc2 --env-config=sc2 with env_args.map_name=5m_vs_6m save_model=True
```

2. Results will be saved in the `results/` folder.

## Contributions and Extensions

This repository includes:

- The integration of Deep Q-Networks (DQN) to address more complex discrete scenarios. Using the iTHOR library, evaluate the performance of DQN in these scenarios by comparing the effectiveness of different episodic memory representation techniques: Autoencoder, Random Projection, and Embeddings. This comparison will highlight how memory representation impacts learning efficiency, policy performance, and overall task success.
- 
- 

## Acknowledgments

We acknowledge the authors of the EMU paper and repository for their foundational work, which has been the base of our approach to the MLRC Challenge.

## License

This project is licensed under the MIT. See the `LICENSE` file for details.
