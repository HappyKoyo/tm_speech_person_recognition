#!/usr/bin/env python
# -*- coding: utf-8 -*

import rospy
import time
from std_msgs.msg import String, Float64,Bool
import subprocess
from geometry_msgs.msg import Twist

class SpeechAndPersonRecognition:
    def __init__(self):
        self.crowd_list_res_sub = rospy.Subscriber('/object/list_res',String,self.getCrowdSizeCB)
        self.speech_sub = rospy.Subscriber('/voice_recog',String,self.recogVoiceCB)

        self.crowd_list_req_pub = rospy.Publisher('/object/list_req',Bool,queue_size=1)
        self.speech_req_pub = rospy.Publisher('/speech/is_active',Bool,queue_size=1)
        self.riddle_req_pub = rospy.Publisher('/riddle_req',Bool,queue_size=1)
        self.head_angle_pub = rospy.Publisher('/m6_controller/command',Float64,queue_size=1)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel_mux/input/teleop',Twist,queue_size=1)

        self.crowd_list = []
        self.male_count = -1
        self.female_count = -1


    def getCrowdSizeCB(self,result):
        self.crowd_list = result.data.split(' ')
        self.crowd_list[-1:] = []
        self.male_count = self.crowd_list.count('male')
        self.female_count = self.crowd_list.count('female')


    def recogVoiceCB(self,sentence):
        self.riddle_req_pub.Publish(sentence)
        print "send riddle request."


    def rotateBase(self,angle):
        rotate_cmd = Twist()
        for i in range(angle):
            c = float(angle)
            rotate_cmd.angular.z = (c/2-abs(c/2-i))/c*4.0+0.3
            print rotate_cmd.angular.z
            self.cmd_vel_pub.publish(rotate_cmd)
            rospy.sleep(0.035)


    def speak(self,sentence):
        try:
            voice_cmd = '/usr/bin/picospeaker %s' %sentence
            subprocess.call(voice_cmd.strip().split(' '))
            print "[PICO]" + sentence
        except OSError:
            print "[PICO] not activate"


    def startSPR(self):#-----------------state 0
        print 'state : 0'
        #set head angle
        head_angle = Float64()
        head_angle.data = -0.4
        self.head_angle_pub.publish(head_angle)
        rospy.sleep(2.0) # move time
        #start riddle game
        self.speak("I want to play riddle game!")
        rospy.sleep(1)#wait 10 seconds
        self.rotateBase(100) # rotateBase(): 
        rospy.sleep(1)
        self.crowd_list_req_pub.publish(True)    
        return 1 #next state


    def stateSizeOfTheCrowd(self):#------state 1
        '''
        '''
        print 'state : 1'
        if len(self.crowd_list) == 0: # tuusinn yabai?
            print "wait for response from object recognizer"
            return 1 #this state
        #state number of male
        if self.male_count == 0:
            speak('There is not male.')
        elif self.male_count == 1:
            speak('There is ' + str(self.male_count) + ' male.')
        else:
            speak('There are ' + str(self.male_count) + ' males.')
        rospy.sleep(1)
        speak("and ")
        rospy.sleep(1)
        #state number of female
        if self.female_count == 0:
            speak('There is not female.')
        elif self.female_count == 1:
            speak('There is ' + str(self.female_count) + ' female.')
        else:
            speak('There are ' + str(self.female_count) + ' females.')
        #state sum of crowd
        speak("There are "+str(self.male_count+self.female_count)+" people in total.")
        rospy.sleep(2.0)
        speak("Who want to play riddles with me?")
        rospy.sleep(3.0)
        self.speech_req_pub.Publish(True) # start google speech api stream
        
        return 2 #next state


    def playRiddleGame(self):#----------state 2
        print 'state : 2'
        
        # loop five count
        return 2 #this state


    def startBlindMansBluffGame(self):#--state 3
        print 'state : 3'

        return 4


    def leaveArena(self):#---------------state 4
        print 'state : 4'
        navigation_req = String()
        navigation_req.data = 'entrance'
        self.navigation_req_pub.publish

        return 5


if __name__ == '__main__':
    rospy.init_node('speech_and_person_recognition')
    spr = SpeechAndPersonRecognition()
    main_state = 0
    while not rospy.is_shutdown():
        if main_state == 0:
            main_state = spr.startSPR()
        elif main_state == 1:
            main_state = 2 # pass main state
            #main_state = spr.stateSizeOfTheCrowd()
        elif main_state == 2:
            main_state = spr.playRiddleGame()
        elif main_state == 3:
            main_state = spr.startBlindMansBluffGame()
        elif main_state == 4:
            main_state = spr.leaveArena()
        rospy.sleep(0.1)
            
