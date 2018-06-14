# Speech Person Recognition 2018 in Canada
## Writter
1. Enomoto
2. Makino
3. Okano
## 大会チェックリスト
[ ] USE+イヤホンジャックが刺さっているかを確認
[ ] 緊急停止スイッチOFF
[ ] PC起動後にスピーカーの電源ON**(青く光っているか)**
[ ] スピーカーはしっかりと接触しているか
[ ] 設定->サウンド->入力装置->内部オーディオを消音にし、MobilePreをONにする
[ ] 音声の出力をunavailableにする
[ ] $ sh mic_check.sh(一度エラーが起こる)
[ ] $ 機体のスイッチをONにする
[ ] 充電器を抜く
## Use
1. リアルセンス
[ ] リアルセンスが起動できるか
```
$ roslaunch realsense realsense_r200_launch.launch
```
2. 人検知
[ ] HumanDetectorを起動する
```
$ cd ~/catkin_ws/src/e_human_detector/darknet
$ rosrun e_human_detector e_human_detector.py
```
3. Hark
[ ] Harkとの接続
```
$ sudo chmod 666 /dev/ttyACM0
```
[ ] マニピュレーションの有効化
```
$ roslaunch turtlebot_bringup minimal.launch
```
[ ] 方向同定プログラム起動
```
$ cd ~/catkin_ws/src/hark_localize.py
```
[ ] Harkのデバイス番号を確認、harkのデバイス設定
```
$ arecord -l
$ vim hark_localize.sh
$ ./ros-localize.sh
```
[ ] SpeechMove起動
```
$ cd ~/catkin_ws/src/speech_move/src
$ python speech_move.py
```
[ ] Command controler起動
```
$ cd ~/catkin_ws/src/CommandControler/scripts/
$ python CommandControler.py
```
[ ] ブラウザを開いて、インターネットに繋がっているか確認
[ ] Speech recognition起動(Google Speech API)
```
$ python ~/catkin_ws/src/speech_recog/scripts/speech_recog_normal.py
```
[ ] sprのプログラムをrospy.sleep(1)からrospy.sleep(10)に直しているか
[ ] sprの起動
```
$ python ~/catkin_ws/src/tm_speech_person_recognition/scripts/spr.py
```

## Please fix it!
```
rospy.sleep(1)#wait 10 seconds
```

## Install
Google TTS  
```
$ pip install google-cloud-texttospeech==0.1.0
```

## Memo 
activate:  
$ crowd_list_req_pub.py

Human detecter topic:  
$ rostopic pub /human_detect_req std_msgs/Bool "data: false"

3D Rider activate:  
$ roslaunch turtlebot_bringup 3dsensor.launch

Base activate:  
$ roslaunch turtlebot_bringup minimal.launch


