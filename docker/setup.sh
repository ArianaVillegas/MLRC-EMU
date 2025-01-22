#!/bin/bash

# Update package lists
apt update

# Install zip and unzip
apt install -y zip unzip

# Run the SC2 installation script
bash /workspace/EMU/EMU_release_pymarl/install_sc2.sh

# Install Python dependencies
pip install protobuf==3.19.6
conda install -y -c conda-forge sacred
conda install -y -c anaconda pymongo

# Build and link gfootball_engine
pushd /opt/conda/envs/emu/lib/python3.8/site-packages/gfootball_engine
cmake .
make -j $(nproc)
popd

pushd /opt/conda/envs/emu/lib/python3.8/site-packages/gfootball_engine
ln -sf libgame.so _gameplayfootball.so
popd

# Add repository and update libstdc++6
add-apt-repository -y ppa:ubuntu-toolchain-r/test
apt-get update
apt-get install -y --only-upgrade libstdc++6

# Copy the updated libstdc++ to the conda environment
cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /opt/conda/envs/emu/lib/

# Export SC2PATH
export SC2PATH=/workspace/EMU/EMU_release_pymarl/3rdparty/StarCraftII

# Install numpy with pip3
pip3 install numpy==1.23.1
