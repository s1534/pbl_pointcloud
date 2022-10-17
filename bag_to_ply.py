import pyrealsense2 as rs
import numpy as np
import cv2
import glob
import os
import argparse
import open3d

parser = argparse.ArgumentParser()
parser.add_argument('--visualize', action='store_true')
args = parser.parse_args() 

bagfiles = glob.glob('bag_data/20221017_234132.bag')
num_bags = len(bagfiles)

for progress, bagfile in enumerate(bagfiles):
    mp4file = os.path.basename(bagfile).split('.')[0]+'.mp4'
    if os.path.isfile(mp4file):
        continue

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
    writer = cv2.VideoWriter(mp4file, fmt, frame_rate, size) # ライター作成

    print('{}/{}: '.format(progress+1, num_bags),bagfile, "size:",size, "frame_rate:",frame_rate)


    # Create an align object
    # rs.align allows us to perform alignment of depth frames to others frames
    # The "align_to" is the stream type to which we plan to align depth frames.
    align_to = rs.stream.color
    align = rs.align(align_to)

    try:
        cur = -1
        while True:
            frames = pipeline.wait_for_frames()

            aligned_frames = align.process(frames)

            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()

            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())

            print(color_image.shape,depth_image.shape)

            color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2BGR)
            writer.write(color_image)


            color = open3d.geometry.Image(color_image)
            depth = open3d.geometry.Image(depth_image)

            # Remove background - Set pixels further than clipping_distance to grey
            # grey_color = 153
            # depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
            # bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)

            # Generate the pointcloud and texture mappings
            rgbd = open3d.geometry.RGBDImage.create_from_color_and_depth(color, depth, convert_rgb_to_intensity = False)
            pcd = open3d.geometry.PointCloud.create_from_rgbd_image(rgbd, open3d.camera.PinholeCameraIntrinsic)

            # Render images
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            # images = np.hstack((bg_removed, depth_colormap))

            open3d.io.write_point_cloud("output.ply",pcd)

            if args.visualize:
                cv2.namedWindow(bagfile, cv2.WINDOW_AUTOSIZE)
                cv2.imshow(bagfile, color_image)
                cv2.waitKey(1)

            next = playback.get_position()
            if next < cur:
                break
            cur = next

    finally:
        pipeline.stop()
        writer.release()
        cv2.destroyAllWindows()