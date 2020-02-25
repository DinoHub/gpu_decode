import cv2
import time
import imghdr

frame_count = 0
fixed_fp = 'vlc_test.png'
wait = 0.01

while 1:
    time.sleep(wait)
    if imghdr.what(fixed_fp) is not None:
        frame = cv2.imread(fixed_fp)
    if frame is not None:
        frame_count += 1
        if frame_count%100 == 0:
            print(frame_count)
        # print('showing',frame.shape)
        # cv2.imshow('', frame)
        # cv2.waitKey(1)