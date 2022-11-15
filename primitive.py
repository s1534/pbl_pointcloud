import open3d as o3d
import numpy as np

pcd = o3d.io.read_point_cloud("hayashi_outlier.ply")

plane_model,inliers = pcd.segment_plane(distance_threshold=0.0025,ransac_n=3,num_iterations=500)
plane_cloud =pcd.select_by_index(inliers)
plane_cloud.paint_uniform_color([1.0,0,0])
outlier_cloud =pcd.select_by_index(inliers,invert=True)

o3d.visualization.draw_geometries([outlier_cloud])
# o3d.visualization.draw_geometries([downpcd])

o3d.io.write_point_cloud("hayashi_primitive.ply", outlier_cloud, write_ascii=False, compressed=False, print_progress=False)
