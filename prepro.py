import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt


# rowデータをボクセルダウンサンプリング
# DBSCAN
# 人を抜き出す
# プリミティブ
# 外れ値除去
# FPS

# -------------------------ファイル入力-------------------------
pcd = o3d.io.read_point_cloud("data/20221110/1.ply")

# -------------------------ダウンサンプリング-------------------------
downpcd = pcd.voxel_down_sample(voxel_size=0.004)

pcd = downpcd
with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    labels = np.array(
        pcd.cluster_dbscan(eps=0.2, min_points=10, print_progress=True))
# print(labels)
max_label = labels.max()
print(f"point cloud has {max_label + 1} clusters")
colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
colors[labels < 1] = 0
pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
# o3d.visualization.draw_geometries([pcd])

# -------------------------人を切り出す-------------------------
pcd_points = np.asarray(pcd.points)
pcd_colors = np.asarray(pcd.colors)

num = pcd_colors.shape[0]

pcd_points_dash = np.zeros((1, 3))
pcd_colors_dash = np.zeros((1, 3))

pcd_clipping_human = o3d.geometry.PointCloud()

for i in range(num):
    if pcd_colors[i][0] == 0 and pcd_colors[i][1] == 0 and pcd_colors[i][2] == 0:
        continue
    else:
        pcd_clipping_human.points.append(pcd_points[i])
        pcd_clipping_human.colors.append(pcd_colors[i])

# -------------------------プリミティブ-------------------------
plane_model,inliers = pcd_clipping_human.segment_plane(distance_threshold=0.0025,ransac_n=3,num_iterations=500)
plane_cloud =pcd_clipping_human.select_by_index(inliers)
plane_cloud.paint_uniform_color([1.0,0,0])
outlier_cloud =pcd_clipping_human.select_by_index(inliers,invert=True)

# o3d.visualization.draw_geometries([outlier_cloud])

# -------------------------外れ値除去-------------------------
pcd_out_lier,ind = outlier_cloud.remove_radius_outlier(nb_points=16,radius=0.02)

# -------------------------FPS-------------------------

def l2_norm(a, b):
    return ((a - b) ** 2).sum(axis=1)

def farthest_point_sampling(pcd, k, metrics=l2_norm):
    indices = np.zeros(k, dtype=np.int32)
    points = np.asarray(pcd.points)
    distances = np.zeros((k, points.shape[0]), dtype=np.float32)
    indices[0] = np.random.randint(len(points))
    farthest_point = points[indices[0]]
    min_distances = metrics(farthest_point, points)
    distances[0, :] = min_distances
    for i in range(1, k):
        indices[i] = np.argmax(min_distances)
        farthest_point = points[indices[i]]
        distances[i, :] = metrics(farthest_point, points)
        min_distances = np.minimum(min_distances, distances[i, :])
    pcd = pcd.select_by_index(indices)
    return pcd

output_ply = farthest_point_sampling(pcd_out_lier,4096)

o3d.visualization.draw_geometries([output_ply])
