import cv2
import os
# from yaspin import yaspin
from time import time, sleep

# print(os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'])

# vp = '/home/dh/Videos/kitty_puppy.mp4'
# vp = '/home/dh/Videos/CatDog.avi'
vp = 'rtsp://localhost:8554/stream'
# vp = 'rtsp://192.168.1.39:554/stream'
additional_params = ' ! decodebin ! videoconvert ! appsink max-buffers=1 drop=true'
# additional_params = ''
# vp = 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'
# cap = cv2.VideoCapture(vp + additional_params, cv2.CAP_FFMPEG)
cap = cv2.VideoCapture(vp + additional_params)

frame_count = 0
total_time = 0

while cap.isOpened():
# try:
    # with yaspin().white.bold.shark.on_blue as sp:
# while True:
    tic = time()
    ret, frame = cap.read()
    if not ret:
        break
    toc = time()
    cv2.imshow('', frame)
    frame_count += 1
    total_time += (toc - tic)
    # print(frame_count)
    if cv2.waitKey(1) == ord('q'):
        break
# except KeyboardInterrupt:
    # print('Keyboard Interrupted')


print('\n\nAvg fps:{}'.format(frame_count/total_time))


