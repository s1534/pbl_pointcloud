import pyrealsense2 as rs
import numpy as np
import cv2
import time
# Configure depth and color streams
config = rs.config()
config.enable_stream(rs.stream.depth, 1024, 768, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# config.enable_stream(rs.stream.infrared, 640, 480, rs.format.y8, 30)

config.enable_record_to_file('d435data.bag')
# Start streaming
pipeline = rs.pipeline()
profile = pipeline.start(config)
start = time.time()
frame_no = 1

depth_sensor = profile.get_device().first_depth_sensor()
laser_pwr = depth_sensor.get_option(rs.option.laser_power)
set_laser = 10
depth_sensor.set_option(rs.option.laser_power, set_laser)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        # ir_frame = frames.get_infrared_frame()
        fps  = frame_no / (time.time() - start)  
        print(fps)
        frame_no = frame_no+1  
        if not color_frame  :   
            # ir_image = np.asanyarray(ir_frame .get_data())    
            color_image = np.asanyarray(color_frame.get_data()) 

finally:    
    pipeline.stop()     