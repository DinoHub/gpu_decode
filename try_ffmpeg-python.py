import cv2
import ffmpeg
import numpy as np

vp = '/home/dh/Videos/CatDog.avi'

width = 1920
height = 1080

process = (
    ffmpeg
    # .input(vp)
    .input(vp, hwaccel='cuvid', vcodec='h264_cuvid')
    # .output('pipe:', format='rawvideo', vf="scale_npp=format=yuv420p,hwdownload,format=yuv420p", pix_fmt='yuvj420p')
    .output('pipe:', format='rawvideo', vf="scale_npp=format=yuv420p,hwdownload,format=yuv420p", pix_fmt='yuvj420p', s='1920x1080')
    # .output('pipe:', format='rawvideo', pix_fmt='rgb24')
    # .output('pipe:', format='rawvideo', pix_fmt='rgb24', vframes=1)
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

from scipy import ndimage
 
def ConvertYUVtoRGB(yuv_planes):
    plane_y  = yuv_planes[:,:,0]
    plane_u  = yuv_planes[:,:,1]
    plane_v  = yuv_planes[:,:,2]
     
    # height = plane_y.shape[0]
    # width  = plane_y.shape[1]
     
    # upsample if YV12
    # plane_u = ndimage.zoom(plane_u, 2, order=0)
    # plane_v = ndimage.zoom(plane_v, 2, order=0)
    # alternativelly can perform upsampling with numpy.repeat()
    #plane_u = plane_u.repeat(2, axis=0).repeat(2, axis=1)
    #plane_v = plane_v.repeat(2, axis=0).repeat(2, axis=1)
     
    # reshape
    plane_y  = plane_y.reshape((plane_y.shape[0], plane_y.shape[1], 1))
    plane_u  = plane_u.reshape((plane_u.shape[0], plane_u.shape[1], 1))
    plane_v  = plane_v.reshape((plane_v.shape[0], plane_v.shape[1], 1))
     
    # make YUV of shape [height, width, color_plane]
    yuv = np.concatenate((plane_y, plane_u, plane_v), axis=2)
     
    # according to ITU-R BT.709
    yuv[:,:, 0] = yuv[:,:, 0].clip(16, 235).astype(yuv.dtype) - 16
    yuv[:,:,1:] = yuv[:,:,1:].clip(16, 240).astype(yuv.dtype) - 128

    A = np.array([[1.164,  0.000,  1.793],
                  [1.164, -0.213, -0.533],
                  [1.164,  2.112,  0.000]])
     
    # our result
    rgb = np.dot(yuv, A.T).clip(0, 255).astype('uint8')
    #rgb = np.tendordot(yuv, A.T, axes=(1,1)).swapaxes(1,2).clip(0, 255).astype('uint8')
     
    return rgb


def bytes2yuv(x, w, h):
    k = w*h
    y =  np.frombuffer(x[0:k], dtype=np.uint8).reshape((h, w))
    u =  np.frombuffer(x[k:k+k//4], dtype=np.uint8).reshape((h//2, w//2))
    v =  np.frombuffer(x[k+k//4:], dtype=np.uint8).reshape((h//2, w//2))
    u = np.reshape(cv2.resize(np.expand_dims(u, -1), (w, h)), (h, w))
    v = np.reshape(cv2.resize(np.expand_dims(v, -1), (w, h)), (h, w))
    image = np.stack([y, u, v], axis=-1)
    return image

n = width*height

while True:
    # in_bytes = process.stdout.read(width * height * 3)
    in_bytes = process.stdout.read(int(width*height*6//4))
    if not in_bytes:
        break
    # in_frame = (
    #     np
    #     .frombuffer(in_bytes, np.uint8)
    #     .reshape([height, width, 3])
    # )

    yuv_in_frame = bytes2yuv(in_bytes, width, height)   
    rgb_in_frame = YUV2RGB(yuv_in_frame)
    # rgb_in_frame = in_frame
    # rgb_in_frame = ConvertYUVtoRGB(in_frame)
    #print(rgb_in_frame.shape)
    cv2.imshow('', rgb_in_frame)
    # print(in_frame.shape)
    cv2.waitKey(1)
    


import pdb; pdb.set_trace()