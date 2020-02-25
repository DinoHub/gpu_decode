import vlc
import cv2
import time

# vp = 'rtsp://localhost:8554/stream'
vp = 'rtsp://192.168.1.39:554/stream'
args = '--vout=dummy'
# player=vlc.MediaPlayer(vp)
inst = vlc.Instance(args)
player = inst.media_player_new()
player.set_mrl(vp)
# player=vlc.MediaPlayer('{} {}'.format(vp,args))
# player.video_set_callbacks(lock= True, unlock= None, display=False, opaque=None)
player.play()

while 1:
    # time.sleep(0.1)
    res = player.video_take_snapshot(0, 'vlc_test.png', 0, 0)
    if res == 0:
        img = cv2.imread('vlc_test.png')
        # cv2.imshow('', img)
        cv2.waitKey(1)
    # # print(res)
