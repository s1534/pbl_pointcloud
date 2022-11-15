import open3d as o3d
import numpy as np

pcd = o3d.io.read_point_cloud("hayashi_outlier.ply")

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

downpcd = farthest_point_sampling(pcd,4096)
o3d.visualization.draw_geometries([downpcd])

o3d.io.write_point_cloud("hayashi_fps.ply", downpcd, write_ascii=False, compressed=False, print_progress=False)
