import open3d as o3d
import numpy as np


def down_sampling():
    print("Load a ply point cloud, print it, and render it")
    # ply_point_cloud = o3d.data.PLYPointCloud()
    pcd = o3d.io.read_point_cloud('data/20221018/2.ply')
    print(pcd)
    print(np.asarray(pcd.points))

    # o3d.visualization.draw_geometries([pcd])

    voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.001)
    o3d.visualization.draw_geometries([voxel_down_pcd])


    print('original:',pcd)
    print('voxel_down_sampling:',voxel_down_pcd)

if __name__ == '__main__':
    down_sampling()
