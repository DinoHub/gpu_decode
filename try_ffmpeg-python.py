import cv2
import time
import ffmpeg
import numpy as np
import tensorflow as tf

# vp = '/home/dh/Videos/CatDog.avi'
# vp = '/videos/CatDog.avi'
# vp = 'rtsp://192.168.1.39:554/stream'
# vp = 'rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov'
# vp ='rtsp://170.93.143.139/rtplive/470011e600ef003a004ee33696235daa'
vp = 'rtsp://localhost:8554/stream'

# width = 1920
# height = 1080

probe = ffmpeg.probe(vp)
video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
width = int(video_stream['width'])
height = int(video_stream['height'])
print('probe w x h: {}x{}'.format(width, height))

process = (
    ffmpeg
    # .input(vp)
    # .input(vp, hwaccel='cuvid', vcodec='h264_cuvid')
    .input(vp, hwaccel='cuvid', vcodec='h264_cuvid', r='1',rtsp_transport='udp', thread_queue_size='8888')
    .output('pipe:', format='rawvideo', vf="scale_npp=format=yuv420p,hwdownload,format=yuv420p", pix_fmt='yuvj420p')
    # .output('pipe:', format='rawvideo', vf="scale_npp=format=yuv420p,hwdownload,format=yuv420p", pix_fmt='yuvj420p', muxdelay=0, r=1)
    # .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    # .output('pipe:', format='rawvideo', pix_fmt='rgb24', vframes=1)
    # .global_args('-nostats', "-loglevel","debug", "-fflags", "discardcorrupt")
    .run_async(pipe_stdout=True)
)


'''
Synchronous running, run ffmpeg,  then run conversion to numpy
'''
# def sync_run():
#     out, _ = (
#         ffmpeg
#         .input(vp)
#         # .input(vp, hwaccel='cuvid', vcodec='h264_cuvid')
#         .output('pipe:', format='rawvideo', pix_fmt='rgb24')
#         # .output('pipe:', format='rawvideo', pix_fmt='yuv420p')
#         .run(capture_stdout=True)
#     )
#     video = (
#         np
#         .frombuffer(out, np.uint8)
#         .reshape([-1, height, width, 3])
#     )

def YUV2RGB( yuv ):
    m = np.array([[ 1.0, 1.0, 1.0],
                 [-0.000007154783816076815, -0.3441331386566162, 1.7720025777816772],
                 [ 1.4019975662231445, -0.7141380310058594 , 0.00001542569043522235] ])
    
    rgb = np.dot(yuv,m)
    rgb[:,:,0]-=179.45477266423404
    rgb[:,:,1]+=135.45870971679688
    rgb[:,:,2]-=226.8183044444304
    rgb = rgb / 255.
    return rgb

# from scipy import ndimage
 
# def ConvertYUVtoRGB(yuv_planes):
#     plane_y  = yuv_planes[:,:,0]
#     plane_u  = yuv_planes[:,:,1]
#     plane_v  = yuv_planes[:,:,2]
     
#     # height = plane_y.shape[0]
#     # width  = plane_y.shape[1]
     
#     # upsample if YV12
#     # plane_u = ndimage.zoom(plane_u, 2, order=0)
#     # plane_v = ndimage.zoom(plane_v, 2, order=0)
#     # alternativelly can perform upsampling with numpy.repeat()
#     #plane_u = plane_u.repeat(2, axis=0).repeat(2, axis=1)
#     #plane_v = plane_v.repeat(2, axis=0).repeat(2, axis=1)
     
#     # reshape
#     plane_y  = plane_y.reshape((plane_y.shape[0], plane_y.shape[1], 1))
#     plane_u  = plane_u.reshape((plane_u.shape[0], plane_u.shape[1], 1))
#     plane_v  = plane_v.reshape((plane_v.shape[0], plane_v.shape[1], 1))
     
#     # make YUV of shape [height, width, color_plane]
#     yuv = np.concatenate((plane_y, plane_u, plane_v), axis=2)
     
#     # according to ITU-R BT.709
#     yuv[:,:, 0] = yuv[:,:, 0].clip(16, 235).astype(yuv.dtype) - 16
#     yuv[:,:,1:] = yuv[:,:,1:].clip(16, 240).astype(yuv.dtype) - 128

#     A = np.array([[1.164,  0.000,  1.793],
#                   [1.164, -0.213, -0.533],
#                   [1.164,  2.112,  0.000]])
     
#     # our result
#     rgb = np.dot(yuv, A.T).clip(0, 255).astype('uint8')
#     #rgb = np.tendordot(yuv, A.T, axes=(1,1)).swapaxes(1,2).clip(0, 255).astype('uint8')
     
#     return rgb

def bytes2yuv(x, w, h):
    k = w*h
    y =  np.frombuffer(x[0:k], dtype=np.uint8).reshape((h, w))
    u =  np.frombuffer(x[k:k+k//4], dtype=np.uint8).reshape((h//2, w//2))
    v =  np.frombuffer(x[k+k//4:], dtype=np.uint8).reshape((h//2, w//2))
    u = np.reshape(cv2.resize(np.expand_dims(u, -1), (w, h)), (h, w))
    v = np.reshape(cv2.resize(np.expand_dims(v, -1), (w, h)), (h, w))
    image = np.stack([y, u, v], axis=-1)
    return image

class YUV2BGR_GPU():
    def __init__(self, w=1920, h=1080): 
        config = tf.ConfigProto(gpu_options=tf.GPUOptions(per_process_gpu_memory_fraction=0.03))
        self.y = tf.placeholder(shape=(1, h, w), dtype=tf.float32)
        self.u = tf.placeholder(shape=(1, h, w), dtype=tf.float32) 
        self.v = tf.placeholder(shape=(1, h, w), dtype=tf.float32)
        r = self.y+1.371*(self.v-128)
        g = self.y+0.338* (self.u-128)-0.698*(self.v-128)
        b = self.y+1.732*(self.u-128)
        result = tf.stack([b, g, r], axis=-1)
        self.result = tf.squeeze(tf.clip_by_value(result, 0, 255))
        self.sess = tf.Session(config=config)

    def convert(self, yuv_planes):
        y = yuv_planes[:,:,0]
        u = yuv_planes[:,:,1]
        v = yuv_planes[:,:,2]
        y = y.reshape((1, y.shape[0], y.shape[1]))
        u = u.reshape((1, u.shape[0], u.shape[1]))
        v = v.reshape((1, v.shape[0], v.shape[1]))
        results = self.sess.run(self.result, feed_dict={self.y:y, self.u: u, self.v: v})

        return results.astype(np.uint8)

C = YUV2BGR_GPU(w=width, h=height)

n = width*height
yuv_times = []
rgb_conversion_times = []
trgb_conversion_times = []    

while True:
    # time.sleep(0.5)
    # in_bytes = process.stdout.read(width * height * 3)
    in_bytes = process.stdout.read(int(width*height*6//4))
    if not in_bytes:
        break
    # in_frame = (
    #     np
    #     .frombuffer(in_bytes, np.uint8)
    #     .reshape([height, width, 3])
    # )

    
    tic = time.time()
    yuv_in_frame = bytes2yuv(in_bytes, width, height)   
    toc = time.time()
    yuv_time = toc - tic
    # print('Time taken for yuv decoding using GPU', yuv_time)
    yuv_times.append(yuv_time)
    
    bgr_in_frame = C.convert(yuv_in_frame)
    toc2 = time.time()
    rgb_conversion_time = toc2 - toc
    rgb_conversion_times.append(rgb_conversion_time)
    # print('Time taken for rgb conversion', rgb_conversion_time)
    
    # rgb_in_frame = in_frame

    # rgb_in_frame = ConvertYUVtoRGB(yuv_in_frame)
    # trgb_conversion_time = time.time() - toc2
    # trgb_conversion_times.append(trgb_conversion_time)

    #print(rgb_in_frame.shape)
    cv2.imshow('', bgr_in_frame)
    # print(in_frame.shape)
    cv2.waitKey(1)
    


# import pdb; pdb.set_trace()