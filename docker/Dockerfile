# Use an official Ubuntu as a base image
FROM nvidia/cuda:12.6.3-base-ubuntu24.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    libgl1-mesa-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-ttf-dev \
    libsdl2-gfx-dev \
    libdirectfb-dev \
    libst-dev \
    mesa-utils \
    xvfb \
    x11vnc \
    wget \
    bzip2 \
    && rm -rf /var/lib/apt/lists/*

# Update package lists and install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    zip unzip \
    cmake \
    build-essential \
    libstdc++6 \
    software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -b -p /opt/conda \
    && rm /tmp/miniconda.sh

# Set up conda environment
ENV PATH="/opt/conda/bin:$PATH"
RUN conda create -n emu python=3.8 -y

# Activate the conda environment and install Python packages
ENV PATH /opt/conda/envs/emu/bin:$PATH

# Install PyTorch and other conda packages
RUN conda install -n emu pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch -y
RUN conda install -n emu anaconda::scikit-learn -y
RUN conda install -n emu anaconda::py-boost -y

# Install pip packages
RUN pip install --upgrade psutil wheel pytest
RUN pip install gfootball==2.10.2 gym==0.11
RUN pip install scipy matplotlib seaborn \
    pyyaml==5.3.1 pygame pytest probscale imageio snakeviz tensorboard-logger
    
# Install Python dependencies
RUN pip install protobuf==3.19.6 && \
    conda install -y -c conda-forge sacred && \
    conda install -y -c anaconda pymongo && \
    pip3 install numpy==1.23.1

# Set the working directory
WORKDIR /workspace
RUN git clone https://github.com/ArianaVillegas/MLRC-EMU.git /workspace/EMU/ 

# Install EMU_smac_env (maps)
RUN cd /workspace/EMU/src && pip install -e EMU_smac_env

# Add repository and update libstdc++6
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test && \
    apt-get update && \
    apt-get install -y --only-upgrade libstdc++6

# Copy the updated libstdc++ to the conda environment
RUN cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /opt/conda/lib/

# Copy the SC2 installation script and run it
RUN bash /workspace/EMU/src/EMU_release_pymarl/install_sc2.sh

# Set environment variables
ENV SC2PATH=/workspace/EMU/EMU_release_pymarl/3rdparty/StarCraftII

# Clean up Conda cache
RUN conda clean -a -y

# Default command (if any)
CMD ["bash"]
