# FROM nvcr.io/nvidia/tensorflow:18.06-py3
# FROM nvcr.io/nvidia/tensorflow:18.10-py3
FROM nvcr.io/nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04

RUN apt-get -y update
# RUN apt-get -y upgrade

RUN apt-get -y install python3.5-tk \
    python3-pip

RUN apt-get -y install sudo \
    apt-transport-https 

RUN apt-get -y install libcanberra-gtk-module \
    libcanberra-gtk3-module \
    dbus-x11

RUN apt-get install -y libopencv-calib3d2.4v5 \
    libopencv-contrib2.4v5 \
    libopencv-core2.4v5 \
    libopencv-features2d2.4v5 \
    libopencv-flann2.4v5 \
    libopencv-gpu2.4v5 \
    libopencv-highgui2.4v5 \
    libopencv-imgproc2.4v5 \
    libopencv-legacy2.4v5 \
    libopencv-ml2.4v5 \
    libopencv-objdetect2.4v5 \
    libopencv-ocl2.4v5 \
    libopencv-photo2.4v5 \
    libopencv-stitching2.4v5 \
    libopencv-superres2.4v5 \
    libopencv-ts2.4v5 \
    libopencv-video2.4v5 \
    libopencv-videostab2.4v5

RUN pip3 install --no-cache-dir --upgrade pip 
RUN pip3 install --no-cache-dir numpy==1.15.3 \
    scipy==1.0.0 \
    matplotlib \
    Pillow==5.3.0 \
    opencv-python
RUN pip3 install --no-cache-dir tensorflow==1.9.0 \
    tensorflow-gpu==1.9.0 \
    Keras==2.2.4 \
    torch==1.1.0 \
    torchvision==0.2.1
RUN pip3 install --no-cache-dir hikvisionapi==0.2.1 \
    simple-pid==0.2.2 \
    GPUtil==1.4.0 \
    tqdm==4.28.1
RUN pip3 install --no-cache-dir requests

RUN apt-get install -y git yasm

RUN git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git &&\
    cd nv-codec-headers &&\
    make install &&\
    cd .. && rm -r nv-codec-headers

RUN git clone https://git.ffmpeg.org/ffmpeg.git &&\
    cd ffmpeg &&\
    git checkout n3.4.7 &&\
    ./configure --enable-cuda --enable-cuvid --enable-nvenc --enable-nonfree --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --extra-ldflags=-L/usr/local/cuda/lib64 &&\
    make -j8 &&\
    make install &&\
    cd .. && rm -r ffmpeg

RUN pip3 install --no-cache-dir ffmpeg-python 

RUN rm -rf /var/lib/apt/lists/* && apt-get -y autoremove

RUN useradd -m user && echo "user:pwd" | chpasswd && adduser user sudo
USER user

WORKDIR /home

