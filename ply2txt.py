import open3d as o3d
import numpy as np

if __name__ == "__main__":
    
    # Loading point cloud
    print("Loading point cloud")
    # ptCloud = o3d.io.read_point_cloud("data/20221115/2.ply")
    ptCloud = o3d.io.read_point_cloud("a.obj")

    # confirmation
    print(ptCloud)
    print(np.asarray(ptCloud.points))

    # points = np.asarray(ptCloud.points)
    # size = points.shape
    # zero = np.zeros((size[0], 3))
    # points = np.concatenate([points,zero],1)
    # print(points.shape)

    # print(ptCloud.points)
    
    # Visualization in window
    # o3d.visualization.draw_geometries([ptCloud])
    
    # Saving point cloud
    # o3d.io.write_point_cloud("output.ply", ptCloud)

    # np.savetxt('data.txt',points)