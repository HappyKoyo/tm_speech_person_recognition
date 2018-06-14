# Speech Person Recognition 2018
## Writter
1. Enomoto
2. Makino
3. Okano
## Use
~~~
1. Connect Realsence
$ roslaunch realsense realsense_r200_launch.launch

2. Human detector activate
$ cd ~/catkin_ws/src/e_human_detector/darknet
$ rosrun e_human_detector e_human_detector.py

3. Hark
3.1 Connect hark
$ sudo chmod 666 /dev/ttyACM0
$ roslaunch turtlebot_bringup minimal.launch

3.2 HarkLocalize
$ cd ~/catkin_ws/src/hark_localize
$ arecord -l
Adjust device hw
$ vim hark_localize.sh
$ ./ros-localize.sh

3.3 SpeechMove
$ cd ~/catkin_ws/src/speech_move/src
$ python speech_move.py

4. Base activate
$ roslaunch turtlebot_bringup minimal.launch

5. Command controler activate
$ cd ~/catkin_ws/src/CommandControler/scripts/
$ python CommandControler.py

6. Speech Recognition (Google Speech API)
$ python ~/catkin_ws/src/speech_recog/scripts/speech_recog_normal.py

7. Finally,execute GPSR
$ python ~/catkin_ws/src/tm_speech_person_recognition/scripts/spr.py
~~~


## Memo 
activate:  
$ crowd_list_req_pub.py

Human detecter topic:  
$ rostopic pub /human_detect_req std_msgs/Bool "data: false"

3D Rider activate:  
$ roslaunch turtlebot_bringup 3dsensor.launch

Base activate:  
$ roslaunch turtlebot_bringup minimal.launch

## Please fix it!
```
rospy.sleep(1)#wait 10 seconds
```

## Install
Google TTS  
```
$ pip install google-cloud-texttospeech==0.1.0
```
