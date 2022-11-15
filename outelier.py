import open3d as o3d
import numpy as np

def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_by_index(ind)
    outlier_cloud = cloud.select_by_index(ind, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_cloud.paint_uniform_color([0, 0, 1])
    inlier_cloud.paint_uniform_color([0.54901961,0.3372549,0.29411765])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

pcd = o3d.io.read_point_cloud("hayashi_primitive.ply")

cl,ind = pcd.remove_radius_outlier(nb_points=16,radius=0.015)
o3d.visualization.draw_geometries([cl])
o3d.io.write_point_cloud("hayashi_outlier.ply", cl, write_ascii=False, compressed=False, print_progress=False)


tmp = np.asarray(cl.colors)
print(tmp[0])
# display_inlier_outlier(pcd,ind)