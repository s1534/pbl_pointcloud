import open3d as o3d
import numpy as np

pcd = o3d.io.read_point_cloud("hayashi_dbscan.ply")

# print(pcd.points)

pcd_points = np.asarray(pcd.points)
pcd_colors = np.asarray(pcd.colors)
print(pcd_points.shape,pcd_colors.shape)

print(pcd_colors.shape[0])

num = pcd_colors.shape[0]

pcd_points_dash = np.zeros((1, 3))
pcd_colors_dash = np.zeros((1, 3))

print(pcd_points_dash)
pcd_dash = o3d.geometry.PointCloud()

for i in range(num):
    if pcd_colors[i][0] == 0 and pcd_colors[i][1] == 0 and pcd_colors[i][2] == 0:
        continue
    else:
        pcd_dash.points.append(pcd_points[i])
        pcd_dash.colors.append(pcd_colors[i])

o3d.visualization.draw_geometries([pcd_dash])
o3d.io.write_point_cloud("hayashi_only_person.ply", pcd_dash, write_ascii=False, compressed=False, print_progress=False)
