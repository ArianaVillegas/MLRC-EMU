FROM nvidia/cuda:12.3.2-cudnn9-devel-ubuntu20.04
MAINTAINER Tabish Rashid

# Set non-interactive mode for apt-get to avoid tzdata configuration prompts
ENV DEBIAN_FRONTEND=noninteractive

# CUDA includes
ENV CUDA_PATH /usr/local/cuda
ENV CUDA_INCLUDE_PATH /usr/local/cuda/include
ENV CUDA_LIBRARY_PATH /usr/local/cuda/lib64

# Ubuntu Packages
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        software-properties-common \
        apt-utils \
        nano \
        vim \
        man \
        build-essential \
        wget \
        sudo \
        curl \
        libssl-dev \
        openssl \
        libopenblas-dev \
        libhdf5-dev \
        hdf5-helpers \
        hdf5-tools \
        libhdf5-serial-dev \
        libprotobuf-dev \
        protobuf-compiler \
        git && \
    add-apt-repository -y multiverse && \
    apt-get update -y && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Install Python 3 and pip3
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install \
        numpy \
        scipy \
        pyyaml \
        matplotlib \
        imageio \
        tensorboard-logger \
        pygame \
        jsonpickle==0.9.6 \
        setuptools \
        torch \
        torchvision \
        snakeviz \
        pytest \
        probscale

# Clone and install Sacred from OxWhirl fork
RUN git clone https://github.com/oxwhirl/sacred.git /install/sacred && \
    cd /install/sacred && \
    python3 setup.py install && \
    rm -rf /install/sacred

# Install SMAC
RUN pip3 install git+https://github.com/oxwhirl/smac.git

# Set SC2PATH environment variable
ENV SC2PATH /pymarl/3rdparty/StarCraftII

# Create and set working directory
RUN mkdir -p /pymarl
WORKDIR /pymarl

# Reset DEBIAN_FRONTEND
ENV DEBIAN_FRONTEND=dialog
