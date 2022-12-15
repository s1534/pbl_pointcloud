import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt


pcd = o3d.io.read_point_cloud("data/20221110/1.ply")

print("Load a ply point cloud, print it, and render it")
print(pcd)
# print(np.asarray(pcd.points))
downpcd = pcd.voxel_down_sample(voxel_size=0.004)
# downpcd = o3d.ml.tf.ops.furthest_point_sampling(pcd, 1024, name=None)
# downpcd = pcd.sample_points_poisson_disk(number_of_points = 1024)

print(downpcd)

o3d.visualization.draw_geometries([downpcd])

pcd=downpcd

with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    labels = np.array(
        pcd.cluster_dbscan(eps=0.2, min_points=10, print_progress=True))
print(labels)
max_label = labels.max()
print(f"point cloud has {max_label + 1} clusters")
colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
colors[labels < 1] = 0
pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
# o3d.visualization.draw_geometries([pcd])  

# -------------------------外れ値除去-------------------------
# cl,ind = pcd.remove_radius_outlier(nb_points=16,radius=0.02)


# print(pcd)

o3d.io.write_point_cloud("hayashi_dbscan.ply", pcd, write_ascii=False, compressed=False, print_progress=False)
