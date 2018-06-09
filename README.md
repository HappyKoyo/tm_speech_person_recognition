# Speech Person Recognition 2018
## Writter
1. Enomoto
2. Makino
3. Okano
## Use
1. Connect Realsence
2. Human detector activate
3. Command controler
4. Finally,execute spr
~~~
$ roslaunch realsense realsense_r200_launch.launch

$ cd ~/catkin_ws/src/e_human_detector/darknet
$ rosrun e_human_detector e_human_detector.py

## TODO CommandCon

$ python ~/catkin_ws/src/tm_speech_person_recognition/scripts/spr.py
~~~
## Memo 
activate:  
'$ crowd_list_req_pub.py'

Human detecter topic:  
'$ rostopic pub /human_detect_req std_msgs/Bool "data: false"'

3D Rider activate:  
'$ roslaunch turtlebot_bringup 3dsensor.launch'

Base activate:  
'$ roslaunch turtlebot_bringup minimal.launch'

## Please fix it!
~~~
rospy.sleep(1)#wait 10 seconds
~~~

