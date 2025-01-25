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

1. Clone the repository:
   ```bash
   git clone https://github.com/ArianaVillegas/MLRC-EMU.git
   cd mlrc-emu
   ```

2. [Additional setup steps.]

### Running Experiments

Experiments are organized in the `experiments/` folder. To run a specific experiment, follow these steps:

1. [Step-by-step instructions for running an experiment, e.g.,]
   ```bash
   python src/train.py --config config/experiment_1.yaml
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
