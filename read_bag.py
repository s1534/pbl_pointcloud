#必要なパッケージのインポート
import bagpy 
import glob
import sys
import rosbag


csvfiles =[]
#ファイル検索
bag_filename = rosbag.Bag("d435data.bag")
print(bag_filename)
# for t in bag_filename.read_messages():
#     print(t)

# for t in b.topics:
#     data = b.message_by_topic(t)
#     csvfiles.append(data) 