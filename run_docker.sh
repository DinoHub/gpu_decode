xhost local:root
docker run -it --gpus all  -v $HOME/Workspace:/workspace -v $HOME/Videos:/videos  --net=host --ipc=host --env="DISPLAY"  ptzaurus