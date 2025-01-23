#!/bin/bash

# Move the 3rdparty directory
mv /workspace/3rdparty /workspace/EMU/src/EMU_release_pymarl/

# Set the SC2PATH environment variable
export SC2PATH='/workspace/EMU/src/EMU_release_pymarl/3rdparty/StarCraftII'

# Install sacred using conda
conda install -y -c conda-forge sacred

# Install specific version of protobuf using pip
pip install protobuf==3.19.6

# Build gfootball_engine
pushd /opt/conda/envs/emu/lib/python3.8/site-packages/gfootball_engine && cmake . && make -j `nproc` && popd

# Create a symbolic link for libgame.so
pushd /opt/conda/envs/emu/lib/python3.8/site-packages/gfootball_engine && ln -sf libgame.so _gameplayfootball.so && popd

# Copy libstdc++.so.6 to the conda environment
cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /opt/conda/envs/emu/lib
