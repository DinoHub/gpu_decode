# jpg is 23 FPS

# This does not work
# ffmpeg -hwaccel cuvid -c:v h264_cuvid  -i rtsp://localhost:8554/stream -pix_fmt yuvj420p -updatefirst 1 -y /tmp/frame.jpg

# But this does!
ffmpeg -hwaccel cuvid -c:v h264_cuvid  -i rtsp://localhost:8554/stream  -vf "scale_npp=format=yuv420p,hwdownload,format=yuv420p"  -pix_fmt yuvj420p -updatefirst 1 -y /tmp/frame.jpg

# png is 11 FPS
# ffmpeg -hwaccel cuvid -c:v h264_cuvid  -i rtsp://localhost:8554/stream  -vf "scale_npp=format=yuv420p,hwdownload,format=yuv420p"  -pix_fmt yuvj420p -updatefirst 1 -y /tmp/frame.png