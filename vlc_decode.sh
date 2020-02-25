# cvlc --snapshot-format=png --snapshot-ratio=1 --snapshot-prefix=frame --snapshot-path="/media/dh/HDD1/vlc_out" /home/dh/Videos/CatDog.avi vlc://quit


cvlc /home/dh/Videos/CatDog.avi --rate=1 --video-filter=scene --vout=dummy --start-time=0 --scene-format=png --scene-ratio=24 --scene-prefix=frame
# cvlc /home/dh/Videos/CatDog.avi --rate=1 --video-filter=scene --vout=dummy --scene-format=png --scene-ratio=24 --scene-prefix=snap --scene-path="/media/dh/HDD1/vlc_out" vlc://quit
