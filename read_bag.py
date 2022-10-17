import open3d as o3d
bag_reader = o3d.t.io.RSBagReader()
bag_reader.open('20221012_010032.bag')
im_rgbd = bag_reader.next_frame()
while not bag_reader.is_eof():
    # process im_rgbd.depth and im_rgbd.color
    im_rgbd = bag_reader.next_frame()
    print(im_rgbd)

bag_reader.close()