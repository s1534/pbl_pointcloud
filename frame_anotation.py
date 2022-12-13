import cv2
import numpy as np
import csv
import pandas as pd

def save_file():
    return 1

filepath = "eating1_color.mp4"

label = {
    1: '料理-主菜を置く', 2: '料理-主菜を掴む',
    3: '料理-主菜を食べる', 4: '料理-副菜を置く', 5: '料理-副菜を掴む', 6: '料理-副菜を食べる', 7: '料理-主食を置く', 8: '料理-主食を掴む',
    9: '料理-主食を食べる', 10: '食事用具を持つ', 11: '食事用具を置く', 12: '食器類を持つ', 13: '食器類を置く'
}

columns_label = ['first_frame', 'last_frame', 'action_label']

df = pd.DataFrame(columns=['first_frame', 'last_frame', 'action_label'])



# 動画の読み込み
cap = cv2.VideoCapture(filepath)
cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

telop_height = 50

fps = 0
first = 0
flag = False

# 動画終了まで繰り返し
while(cap.isOpened()):
    # フレームを取得
    ret, frame = cap.read()


    telop = np.zeros((telop_height, cap_width, 3), np.uint8)
    telop[:] = tuple((128, 128, 128))

    images = [frame, telop]
    frame = np.concatenate(images, axis=0)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "{}[fps]".format(fps),
                (cap_width - 250, cap_height + telop_height - 10),
                font,
                1,
                (0, 0, 255),
                2,
                cv2.LINE_AA)
    # フレームを表示
    cv2.imshow("Frame", frame)

    # qキーが押されたら途中終了
    key = cv2.waitKey(70) & 0xff
    if key == ord('q'):
        break

    # 現在のフレーム番号を取得
    # curpos = int(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))

    # トラックバーにセットする（コールバック関数が呼ばれる）
    cv2.setTrackbarPos('temp', 'aiueo', fps)

    # 開始フレームを選択
    if key == ord('s'):
        flag = False
        first = fps
        print("開始フレーム：", first)


    # 終了フレームを選択
    if key == ord('d'):
        flag = True
        last = fps
        print("終了フレーム：", last)

    # アノテーション結果をcsvに出力
    if key == ord('f'):
        save_file()

    # ラベルを付与
    if flag:
        flag = False
        label_num = int(input())
        # print("開始フレーム：", first)
        # print("終了フレーム：", last)
        print("付与されたラベル：", label[label_num])
        action_label = label[label_num]
        # 開始フレームと終了フレームを初期化
        tmp = pd.DataFrame(data=[[first, last, action_label]],columns=columns_label)
        df = df.append(tmp, ignore_index=True)

        print(df)
        first = 0
        last = 0


    # フレームを戻す
    if key == ord('j'):
        cap.set(cv2.CAP_PROP_POS_FRAMES, first)
        if fps-10 >=0:
            fps-=10
            first = 0
            last = 0

    fps += 1


cap.release()
cv2.destroyAllWindows()
