#!/bin/bash

# Install Conda packages
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
