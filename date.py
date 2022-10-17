## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##                  Export to PLY                  ##
#####################################################

# First import the library
import pyrealsense2 as rs
from datetime import datetime
from pytz import timezone
import os

def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)


utc_now = datetime.now(timezone('UTC'))
jst_now = utc_now.astimezone(timezone('Asia/Tokyo'))
ts = jst_now.strftime("%Y%m%d-%H%M%S")

# Declare pointcloud object, for calculating pointclouds and texture mappings
pc = rs.pointcloud()
# We want the points object to be persistent so we can display the last cloud when a frame drops
points = rs.points()

# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe = rs.pipeline()
config = rs.config()
# Enable depth stream
config.enable_stream(rs.stream.depth)

# Start streaming with chosen configuration
pipe.start(config)

# We'll use the colorizer to generate texture for our PLY
# (alternatively, texture can be obtained from color or infrared stream)
colorizer = rs.colorizer()

while 1:
    # Wait for the next set of frames from the camera
    frames = pipe.wait_for_frames()
    colorized = colorizer.process(frames)

    utc_now = datetime.now(timezone('UTC'))
    jst_now = utc_now.astimezone(timezone('Asia/Tokyo'))
    ts = jst_now.strftime("%Y%m%d-%H%M%S")
    date = ts[:8]

    # ディレクトリが無いときは作成する
    my_makedirs("data/"+date)
    # Create save_to_ply object
    ply = rs.save_to_ply("data/"+date+"/"+ts+".ply")

    # Set options to the desired values
    # In this example we'll generate a textual PLY with normals (mesh is already created by default)
    ply.set_option(rs.save_to_ply.option_ply_binary, True)
    ply.set_option(rs.save_to_ply.option_ply_normals, True)

    print("Saving to"+ ts + "ply...")
    # Apply the processing block to the frameset which contains the depth frame and the texture
    ply.process(colorized)
    print("Done")
    
