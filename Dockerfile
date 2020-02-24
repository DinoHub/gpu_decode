# FROM tensorflow/tensorflow:1.13.1-gpu-py3
FROM nvcr.io/nvidia/cuda:10.0-cudnn7-runtime-ubuntu18.04

RUN apt-get update -qq && apt-get -y install \
    autoconf \
    automake \
    build-essential \
    cmake \
    git-core \
    libass-dev \
    libfreetype6-dev \
    libsdl2-dev \
    libtool \
    libva-dev \
    libvdpau-dev \
    libvorbis-dev \
    libxcb1-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    pkg-config \
    texinfo \
    wget \
    zlib1g-dev 

# RUN apt clean \
#     apt update \
#     apt -y purge cuda \
#     apt -y purge nvidia-* \
#     apt -y autoremove

# RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
# RUN mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
# RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
# RUN add-apt-repository "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"
# RUN apt-get update

RUN git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git

RUN cd nv-codec-headers && make install

RUN cd ..

RUN git clone https://git.ffmpeg.org/ffmpeg.git

RUN cd ffmpeg && git checkout n3.4.7

RUN apt-get -y install yasm 

RUN apt-get -y install cuda

RUN cd ffmpeg && ./configure --enable-cuda --enable-cuvid --enable-nvenc --enable-nonfree --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --extra-ldflags=-L/usr/local/cuda/lib64

RUN make -j 10 
# run 10 threads

RUN make install

RUN apt-get -y install python3-dev python3-numpy

RUN apt-get -y install python3-tk
RUN apt-get -y install python3-opencv\
    && rm -rf /var/lib/apt/lists/*
RUN apt-get -y -y autoremove


RUN pip3 install --no-cache-dir --upgrade pip 
RUN pip3 install --no-cache-dir numpy \
                                scipy==1.0.0 \
                                matplotlib \ 
                                ffmpeg-python
