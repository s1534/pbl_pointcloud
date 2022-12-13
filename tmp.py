import cv2
import numpy as np
import PySimpleGUI as sg

layout = [[sg.Text('名前は？'), sg.Input(key='-NAME-')],
          [sg.Text('', key='-ACT-')],
          [sg.Button('決定'), sg.Button('終了')]]

window = sg.Window('sample', layout)


filepath = "eating1_color.mp4"

# 動画の読み込み
cap = cv2.VideoCapture(filepath)

# 200フレーム目から取得
# cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

flag = 0


# 動画終了まで繰り返し
while(True):
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == '終了':
        break
    if event == '決定':
        window['-ACT-'].update(f'成功！ あなたの名前は{values["-NAME-"]}さんですね')

    # フレームを取得
    ret, frame = cap.read()

    if ret is True:
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['image'].update(data=imgbytes)

    # フレームを表示
    cv2.imshow("Frame", frame)
    if(flag % 10 == 0):
        print(flag)
    flag += 1



    # qキーが押されたら途中終了
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

window.close()
cap.release()
cv2.destroyAllWindows()

print(flag)
print(f'eventは{event}')
print(f'valuesは{values}')
