import open3d as o3d
import numpy as np
import os
import numpy as np

action_dict = {'eat':'01','hold':'02','glab':'03','put':'04'}
object_dict = {'main-dish':'01','main-side-dish':'02','staple-dish':'03','tableware_hold':'04'}

def my_makedirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def create_dataset(path,pcd_numpy,num):
    print(path)
    sep_num = path.rfind('_')
    action = path[sep_num+1:]
    action = action_dict[action]
    object = path[:sep_num]
    object = object_dict[object]
    s = '01'
    e = num.zfill(2)
    file_name = 'a'+action+'_o'+object+'_s'+s+'_e'+e
    np.savez('data/dataset/'+file_name,pcd_numpy)


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

def down_sampling(pcd):
    downpcd = pcd.voxel_down_sample(voxel_size=0.4)
    return downpcd

def read_dir():
    # カレントディレクトリを取得
    current_dir = os.getcwd()
    path = current_dir+'/data/eating1/'
    files = os.listdir(path)
    files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
    print(files_dir)
    for action_label in files_dir:
        print(action_label)
        current_path = path+action_label+'/'
        tmp = os.listdir(current_path)
        i = 0
        for each_action_dir in tmp:
            bottom_dir = current_path+each_action_dir
            # bottom_dirは2184とかのところ（.ply）の上の階層
            ply_path = os.listdir(bottom_dir)
            i+=1
            j = 0
            for ply in ply_path:
                pcd_dir = bottom_dir+'/'+ply
                print(pcd_dir)
                print(len(ply_path))
                pcd = o3d.io.read_point_cloud(pcd_dir)
                pcd = down_sampling(pcd)
                print(pcd)
                pcd,ind = pcd.remove_radius_outlier(nb_points=16, radius=2)
                print(pcd)
                xyz_load = np.asarray(pcd.points)
                if j == 0:
                    pcd_concat_np = xyz_load
                else:
                    pcd_concat_np = np.concatenate([pcd_concat_np,xyz_load])
                j+=1
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(pcd_concat_np)
            pcd = farthest_point_sampling(pcd,1024)
            # o3d.visualization.draw_geometries([pcd])
            pcd_numpy = np.asarray(pcd.points)
            create_dataset(action_label,pcd_numpy,str(i))
            # print('each_action_dir',each_action_dir)

if __name__ == '__main__':
    print('処理開始')
    read_dir()