import cv2
import os
from yaspin import yaspin
from time import time, sleep

print(os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'])

vp = '/home/levan/Videos/kitty_puppy.mp4'
cap = cv2.VideoCapture(vp, cv2.CAP_FFMPEG)

frame_count = 0
total_time = 0

try:
    with yaspin().white.bold.shark.on_blue as sp:
        while True:
            tic = time()
            ret, frame = cap.read()
            if not ret:
                break
            toc = time()
            frame_count += 1
            total_time += (toc - tic)
            # print(frame_count)
except KeyboardInterrupt:
    print('Keyboard Interrupted')


print('\n\nAvg fps:{}'.format(frame_count/total_time))


