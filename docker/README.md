# EMU Project Setup and Execution
This guide provides step-by-step instructions to run the EMU project locally and on the Khipu platform.

## Local Setup
1. Pull the Docker Image
Pull the pre-built Docker image from Docker Hub:

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

6. Run an experiment
```shell
cd /workspace/EMU/src/EMU_release_pymarl/
```

```shell
python3 src/main.py --config=EMU_sc2 --env-config=sc2 with env_args.map_name=5m_vs_6m
```



# Instructions to run in Khipu
