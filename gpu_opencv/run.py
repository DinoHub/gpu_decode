import cv2

vid = '/media/dh/HDD/sample_data/videos/SeoulHongikUnivStreetViewWalk_5mintrim_1080p.mp4'
cap = cv2.VideoCapture(vid)

assert cap.isOpened()
print(cap.getBackendName())
import pdb; pdb.set_trace()

frame_id = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_id += 1
    cv2.waitKey(1)
    print(frame_id)