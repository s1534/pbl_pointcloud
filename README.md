# pbl_pointcloud
点群pbl用のリポジトリ

# Usage
## bagファイルを生成
RGBとDepthを取得し，bagファイルを生成
```
python open3d_make_bag_file.py
```
設定はconfig.jsonに記載

## bagファイルから1フレームずつ点群データ(.ply)を生成
```
python bag2ply.py
```
