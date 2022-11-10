import pyrealsense2 as rs
import numpy as np
import cv2
import glob
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--visualize', action='store_true')
args = parser.parse_args() 

bagfiles = glob.glob('tmp.bag')
num_bags = len(bagfiles)
print(num_bags)
for progress, bagfile in enumerate(bagfiles):
    color_mp4file = os.path.basename(bagfile).split('.')[0]+'_color'+'.mp4'
    depth_mp4file = os.path.basename(bagfile).split('.')[0]+'_depth'+'.mp4'
    if os.path.isfile(color_mp4file):
        os.remove(color_mp4file)
        os.remove(depth_mp4file)

    config = rs.config()
    config.enable_device_from_file(bagfile)

    pipeline = rs.pipeline()
    profile = pipeline.start(config)

    device = profile.get_device()
    playback = device.as_playback()

    for stream in profile.get_streams():
        vprof = stream.as_video_stream_profile()
        if  vprof.format() == rs.format.rgb8:
            frame_rate = vprof.fps()
            size = (vprof.width(), vprof.height())

    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # ファイル形式(ここではmp4)
    writer_color = cv2.VideoWriter(color_mp4file, fmt, frame_rate, size) # ライター作成(カラー用)
    writer_depth = cv2.VideoWriter(depth_mp4file, fmt, frame_rate, size) # ライター作成(depth用)

    print('{}/{}: '.format(progress+1, num_bags),bagfile, size, frame_rate)

    try:
        cur = -1
        while True:
            frames = pipeline.wait_for_frames()

            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            color_image = np.asanyarray(color_frame.get_data())    
            depth_image = np.asanyarray(depth_frame.get_data())    
            color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
            # 描画
            writer_color.write(color_image)
            writer_depth.write(depth_image)
            

            if args.visualize:
                cv2.namedWindow(bagfile, cv2.WINDOW_AUTOSIZE)
                cv2.imshow(bagfile, color_image)
                cv2.waitKey(1)

            next = playback.get_position()
            if next < cur:
                break
            cur = next

    finally:
        print(color_image.shape)
        print(depth_image.shape)
        pipeline.stop()
        writer_color.release()
        writer_depth.release()
        cv2.destroyAllWindows()