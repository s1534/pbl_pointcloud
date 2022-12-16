import pyrealsense2 as rs
import numpy as np
import cv2
import open3d
from datetime import datetime
import os
from pytz import timezone
import matplotlib.pyplot as plt
import pandas as pd

# bagファイルを1フレームごとにplyとして出力する
# ラベルごとにフォルダの振り分けを行う

def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

df = pd.read_csv('eating3.csv',index_col = 0)

# ラベルの定義
label_dict = {'料理-主食を掴む':'main-dish_grab',
            '料理-主食を食べる':'main-dish_eat',
            '料理-副菜を掴む':'side-dish_grab',
            '料理-副菜を食べる':'side-dish_eat',
            '料理-主菜を掴む':'staple-dish_grab',
            '料理-主菜を食べる':'staple-dish_eat',
            '食器類を持つ':'tableware_hold',
            '食器類を置く':'tableware_put'}
df['action_label'] = df['action_label'].map(label_dict)

print(df)

list_dataset = df.to_numpy().tolist()
action = df['action_label'].unique().tolist()
action_num = [i for i in range(len(action))]
label_enc = dict(zip(action,action_num))

# 最初のラベルで初期化
label = list_dataset[0]
first_frame = label[0]
last_frame = label[1]



config = rs.config()
bag_filename = 'D:/pointcloud/20221110/eating3.bag'

# ↓ ここでファイル名設定
config.enable_device_from_file(bag_filename)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)

intr = profile.get_stream(rs.stream.color).as_video_stream_profile().get_intrinsics()
pinhole_camera_intrinsic = open3d.camera.PinholeCameraIntrinsic(intr.width, intr.height, intr.fx, intr.fy, intr.ppx, intr.ppy)

align_to = rs.stream.color
align = rs.align(align_to)

try:
    num = 0
    list_dataset_num = 0
    count =1
    while True:
        # フレーム待ち(Color & Depth)
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        # Show images
        # plt.subplot(221)
        # plt.title('rgbd.color image')
        # plt.imshow(rgbd.color)
        # plt.subplot(222)
        # plt.title('rgbd.depth image')
        # plt.imshow(rgbd.depth)
        # plt.subplot(223)
        # plt.title('depth_image')
        # plt.imshow(depth)
        # plt.subplot(224)
        # plt.title('color_image')
        # plt.imshow(color_image)
        # plt.show()

        print(num)
        # ディレクトリが無いときは作成する
        # my_makedirs("data/"+label[2])
        if first_frame <= num and num <= last_frame:
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            # color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
            color = open3d.geometry.Image(color_image)

            depth_image = np.asanyarray(depth_frame.get_data())
            depth = open3d.geometry.Image(depth_image)
            
            # 人だけ抜き取る神のパラメータ
            rgbd = open3d.geometry.RGBDImage.create_from_color_and_depth(color, depth, depth_scale=100.0, depth_trunc=70,convert_rgb_to_intensity = False)
            pcd =  open3d.geometry.PointCloud.create_from_rgbd_image(rgbd, pinhole_camera_intrinsic)

            if num == first_frame:
                my_makedirs("data/"+"eating3/"+label[2]+"/"+str(first_frame))

            open3d.io.write_point_cloud("data/"+"eating3/"+label[2]+"/"+str(first_frame)+'/'+str(count)+".ply", pcd)
            count+=1
            print('ply作成')
            if num == last_frame:
                list_dataset_num+=1
                label = list_dataset[list_dataset_num]
                first_frame = label[0]
                last_frame = label[1]
        num+=1

finally:
    # Stop streaming
    pipeline.stop()