import json
import open3d as o3d
import keyboard

# open3d使って，カラー動画とデプス動画をbag形式で保存する

config_filename = 'config.json'
with open(config_filename) as cf:
    rs_cfg = o3d.t.io.RealSenseSensorConfig(json.load(cf))

bag_filename = 'D:/pointcloud/eating4.bag'

rs = o3d.t.io.RealSenseSensor()
rs.init_sensor(rs_cfg, 0, bag_filename)
rs.start_capture(True)  # true: start recording with capture
# for fid in range(150):
while True:
    im_rgbd = rs.capture_frame(True, True)  # wait for frames and align them
    # process im_rgbd.depth and im_rgbd.color
    if keyboard.read_key() == "q":
        break

rs.stop_capture()