#!/bin/bash
export WORKSPACE=$HOME/Workspace
export DATA=/media/dh/HDD/

xhost +local:docker
docker run -it  --gpus all -w $WORKSPACE -v $WORKSPACE:$WORKSPACE -v $DATA:$DATA --net=host --ipc host -e DISPLAY=unix$DISPLAY  opencv_gpu:rtx2070