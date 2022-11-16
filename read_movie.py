import cv2
import os

video_file = 'eating1_color.mp4'
video_file = 'eating1_depth.mp4'

## 動画キャプチャ
videoCapture = cv2.VideoCapture(video_file)
## フレーム総数
totalFrames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
 
## n番目のフレーム画像を返す
def retrieveFrameImage(frameIndex):
    ## インデックスがフレームの範囲内なら…
    if(frameIndex >= 0 & frameIndex < totalFrames):
        videoCapture.set(cv2.CAP_PROP_POS_FRAMES, frameIndex)
        ret, image = videoCapture.read()
        return image
    else:
        return None
    
png = retrieveFrameImage(1)
print(png)
cv2.imwrite('depth.jpg', png)

# save_frame('eating1_color.mp4', 1, '/data')

# save_frame('eating1_depth.mp4', 1, 'C:/Users/mishima/Documents/GitHub/pbl_pointcloud/data')