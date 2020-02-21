http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
https://medium.com/@fanzongshaoxing/use-ffmpeg-to-decode-h-264-stream-with-nvidia-gpu-acceleration-16b660fd925d
https://github.com/opencv/opencv/issues/11220

You have to use at least OpenCV 3.4.2, then :

Create a videoreader using the FFMPEG backend : cap->open(video_src, CAP_FFMPEG);
set the envvar OPENCV_FFMPEG_CAPTURE_OPTIONS="video_codec;h264_cuvid"
This way, the videoreader will use the h264_cuvid codec.
If your source is an rtsp one, add the entry rtsp_transport;tcp ; so the envvar becomes :
OPENCV_FFMPEG_CAPTURE_OPTIONS="video_codec;h264_cuvid|rtsp_transport;tcp"

