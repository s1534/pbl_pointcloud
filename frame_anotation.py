import cv2
import numpy as np

filepath = "eating1_color.mp4"

# 動画の読み込み
cap = cv2.VideoCapture(filepath)

# 200フレーム目から取得
# cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

flag = 0

# 動画終了まで繰り返し
while(cap.isOpened()):
    # フレームを取得
    ret, frame = cap.read()

    # フレームを表示
    cv2.imshow("Frame", frame)
    if(flag % 10 == 0):
        print(flag)
    flag+=1
    # qキーが押されたら途中終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(flag)