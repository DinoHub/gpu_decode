# jpg is 23 FPS

# This does not work
# ffmpeg -hwaccel cuvid -c:v h264_cuvid  -i rtsp://localhost:8554/stream -pix_fmt yuvj420p -updatefirst 1 -y /tmp/frame.jpg

# But this does!
# ffmpeg -hwaccel cuvid -c:v h264_cuvid  -i rtsp://localhost:8554/stream  -vf "hwdownload,format=yuv420p"  -pix_fmt yuvj420p -updatefirst 1 -y /tmp/frame.jpg
# ffmpeg -hwaccel cuvid -c:v h264_cuvid  -i rtsp://192.168.1.39:554/stream  -vf "scale_npp=format=yuv420p,hwdownload,format=yuv420p"  -pix_fmt yuvj420p -updatefirst 1 -y frame.jpg
ffmpeg -c:v h264  -i rtsp://192.168.1.39:554/stream    -pix_fmt rgb24 -updatefirst 1 -y frame.jpg

# png is 11 FPS
# ffmpeg -hwaccel cuvid -c:v h264_cuvid  -i rtsp://localhost:8554/stream  -vf "scale_npp=format=yuv420p,hwdownload,format=yuv420p"  -pix_fmt yuvj420p -updatefirst 1 -y /tmp/frame.png