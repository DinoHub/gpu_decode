import cv2
import numpy as np
import subprocess as sp

# ffmpeg_cmd = ["ffmpeg",  "-y",  
#               "-hwaccel",  "nvdec",
#               "-c:v",  "h264_cuvid",
#               "-vsync", "0", 
#               "-max_delay", "500000", 
#               "-reorder_queue_size", "10000", 
#               "-i",  "rtsp://localhost:8554/stream", 
#               "-f", "rawvideo",
#               "-pix_fmt", "yuv420p",
#               "-preset", "slow",
#               "-an", "-sn", 
#               "-vf", "fps=15", 
#               "-"]

# ffmpeg_cmd = ['ffmpeg', '-y', '-vsync', '0',
#                 '-hwaccel', 'cuvid', '-vcodec', 'h264_cuvid',
#                 '-i', 'rtsp://localhost:8554/stream',
#                 '-f', 'rawvideo',
#                 '-pix_fmt', 'yuv420p',
#                 '-']

# ffmpeg_cmd = ['ffmpeg', '-y', '-vsync', '0',
#                 '-hwaccel', 'cuvid', '-vcodec', 'h264_cuvid',
#                 '-i', 'rtsp://localhost:8554/stream',
#                 '-vcodec', 'h264_nvenc',
#                 '-an',
#                 '-']

# ffmpeg_cmd = 'ffmpeg -vsync 0 -hwaccel cuvid -i /home/levan/Videos/KittensMeetPuppiesForTheFirstTime_original.mkv -ss 00:05 -t 01:40 -f rawvideo -preset slow -sn -an -pix_fmt yuv420p -'
# ffmpeg_cmd = 'ffmpeg -vsync 0 -hwaccel cuvid -vcodec h264_cuvid -i rtsp://localhost:8554/stream -f rawvideo -preset slow -an -sn -pix_fmt yuv420p -'

# ffmpeg_cmd = 'ffmpeg -hwaccel cuvid -c:v h264_cuvid  -i rtsp://localhost:8554/stream  -vf "scale_npp=format=yuv420p,hwdownload,format=yuv420p"  -pix_fmt yuvj420p -updatefirst 1 -'

ffmpeg_cmd = 'ffmpeg -hwaccel cuvid -c:v h264_cuvid -i rtsp://localhost:8554/stream -vf "scale_npp=format=yuv420p,hwdownload,format=yuv420p" -pix_fmt yuvj420p -updatefirst 1 -y /tmp/frame.jpg'


ffmpeg_cmd = ffmpeg_cmd.split(' ')

# ffmpeg_cmd = [ 'ffmpeg',
#             '-i', '/home/dh/Videos/CatDog.avi',
#             '-f', 'image2pipe',
#             '-pix_fmt', 'rgb24',
#             '-vcodec', 'rawvideo', '-']
print(ffmpeg_cmd)
# exit()
# pipe = sp.Popen(ffmpeg_cmd, stdout = sp.PIPE, bufsize=10**8)
pipe = sp.Popen(ffmpeg_cmd, stdout=sp.PIPE, bufsize=10**8)

exit()

w = 1920
h = 1080

while True:
    raw_image = pipe.stdout.read(w*h*3)
    # transform the byte read into a numpy array
    # image =  np.fromstring(raw_image, dtype='uint8')
    # image = image.reshape((h,w,3))
    # throw away the data in the pipe's buffer.
    print(type(raw_image))
    print(raw_image)
    pipe.stdout.flush()
    # cv2.imshow('', image)
    # cv2.waitKey(0)
# # ffmpeg = sp.Popen(ffmpeg_cmd, stdout=sp.PIPE, bufsize=10)
# # exit()
# n = w*h
# while True: 
#     buff = ffmpeg.stdout.read(int(w*h*6//4))
#     # buff = ffmpeg.stdout.read()
#     print(buff)
#     # y =  np.frombuffer(buff[0:n], dtype=np.uint8).reshape((h, w))
#     # u =  np.frombuffer(buff[n:n+n//4], dtype=np.uint8).reshape((h//2, w//2))
#     # v =  np.frombuffer(buff[n+n//4:], dtype=np.uint8).reshape((h//2, w//2))
#     # u = np.reshape(cv2.resize(np.expand_dims(u, -1), (w, h)), (h, w))
#     # v = np.reshape(cv2.resize(np.expand_dims(v, -1), (w, h)), (h, w))
#     # image = np.stack([y, u, v], axis=-1)
