# Decoding RSTP Streams using GPU

## Sources
- http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
- https://medium.com/@fanzongshaoxing/use-ffmpeg-to-decode-h-264-stream-with-nvidia-gpu-acceleration-16b660fd925d
- https://github.com/opencv/opencv/issues/11220

You have to use at least OpenCV 3.4.2, then :

Create a videoreader using the FFMPEG backend : cap->open(video_src, CAP_FFMPEG); <br>
set the envvar OPENCV_FFMPEG_CAPTURE_OPTIONS="video_codec;h264_cuvid" <br>
This way, the videoreader will use the h264_cuvid codec. <br>
If your source is an rtsp one, add the entry rtsp_transport;tcp ; so the envvar becomes :
OPENCV_FFMPEG_CAPTURE_OPTIONS="video_codec;h264_cuvid|rtsp_transport;tcp"


## Requirements (https://developer.nvidia.com/ffmpeg)
- You would need to have a nvidia gpu
- Download and install compatible gpu driver from [here](https://www.nvidia.com/download/index.aspx?lang=en-us) 
- Download and install the CUDA Toolkit from [here](https://developer.nvidia.com/cuda-toolkit)
- Download and install ffnvcodec:
```bash
git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git
cd nv-codec-headers && sudo make install && cd –
```
- Compile and install ffmpeg from source
```bash
git clone https://git.ffmpeg.org/ffmpeg.git
cd ffmpeg
git checkout n3.4.7
./configure --enable-cuda --enable-cuvid --enable-nvenc --enable-nonfree --enable-libnpp --extra-cflags=-I/usr/local/cuda/include --extra-ldflags=-L/usr/local/cuda/lib64
make -j 10 # run 10 threads
sudo make install
```
After this is done, restart your comp


### Testing installation
try running
```bash
ffmpeg -hwaccel cuvid -c:v h264_cuvid  -i rtsp://localhost:8554/stream  -vf "scale_npp=format=yuv420p,hwdownload,format=yuv420p"  -pix_fmt yuvj420p -updatefirst 1 -y /tmp/frame.jpg
```
You can do this using vlc to simlute a rtsp stream <br>
You can `watch nvidia-smi` to see the gpu usage

