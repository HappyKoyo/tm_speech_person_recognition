#!/usr/bin/env python
# -*- coding: utf-8 -*

import json
import rospy
import time
from std_msgs.msg import String, Float64,Bool
import subprocess
from geometry_msgs.msg import Twist

class SpeechAndPersonRecognition:
    def __init__(self):
        # Subuscriver----->
        self.crowd_list_res_sub = rospy.Subscriber('/object/list_res',String,self.getCrowdSizeCB)
        self.speech_word_sub = rospy.Subscriber('/voice_recog',String,self.recogVoiceWordCB)
        #self.speech_dict_sub = rospy.Subscriber('/voice_recog_dict',String,self.recogVoiceDictCB)
        self.riddle_req_sub = rospy.Subscriber('/riddle_res/is_action_state',Bool,self.setIsActionSuccessCB)

        # Publisher------->
        self.crowd_list_req_pub = rospy.Publisher('/object/list_req',Bool,queue_size=1)
        self.speech_req_pub = rospy.Publisher('/speech/is_active',Bool,queue_size=1)
        self.riddle_req_word_pub = rospy.Publisher('/riddle_req/question_word',String,queue_size=1)
        #self.riddle_req_dict_pub = rospy.Publisher('/riddle_req/question_dict',String,queue_size=1)
        self.head_angle_pub = rospy.Publisher('/m6_controller/command',Float64,queue_size=1)
        self.cmd_vel_pub = rospy.Publisher('/cmd_vel_mux/input/teleop',Twist,queue_size=1)
        #self.command_pub = rospy.Publisher('/command/question',String,queue_size=1)

        self.crowd_list = []
        self.male_count = -1
        self.female_count = -1
        self.recog_word = ''
        self.is_action_state = None # Success -> True, Failure -> False, No input -> None

    # CallBack Functions ---------------->

    def getCrowdSizeCB(self,result):
        self.crowd_list = result.data.split(' ')
        self.crowd_list[-1:] = []
        self.male_count = self.crowd_list.count('male')
        self.female_count = self.crowd_list.count('female')


    def recogVoiceWordCB(self,sentence):
        ''' receive result word in speech_recog/scripts/speech_recog_normal.py '''
        if main_state == 2 or main_state == 3:
            print "Q : " + sentence.data
            #self.recog_word = sentence
            self.riddle_req_word_pub.publish(sentence.data)
            print "send riddle request."
    
    def recogVoiceDictCB(self,_json_str):
        '''
            Receive json string. It need to perse json().
            It function pass voice recognition result without change.
        '''
        voice_json = self.JsonStringToDictation(_json_str.data)
        print(voice_json['word'])
        if main_state == 2 or main_state == 3:
            print "Q : " + voice_json['word']
            #self.recog_word = sentence
            self.riddle_req_dict_pub.publish(_json_str) # without change
            print "send riddle request."


    def setIsActionSuccessCB(self,is_complete):
        ''' receive message CommandControl/scripts/CommandControl.py '''
        import types
        print "success : " + str(is_complete.data)
        self.is_action_state = is_complete.data


    def JsonStringToDictation(self, _json):
        ''' jsonで書かれた文字列を辞書型にする '''
        # json.loadsでunicodeに変換された文字列をstrにする
        import types
        dictation = json.loads(_json)
        for key in dictation:
            key_type = dictation[key]
            if type(key_type) == unicode: # unicodeをstrにする
                dictation[key] = dictation[key].encode('utf-8')
        return dictation


    # Move Function ------------------->

    def rotateBase(self,angle):
        rotate_cmd = Twist()
        for i in range(angle):
            c = float(angle)
            rotate_cmd.angular.z = (c/2-abs(c/2-i))/c*4.0+0.3
            print rotate_cmd.angular.z
            self.cmd_vel_pub.publish(rotate_cmd)
            rospy.sleep(0.035)


    def rotateVoiceDirection(self):
        pass


    def speak(self,sentence):
        try:
            voice_cmd = '/usr/bin/picospeaker %s' %sentence
            subprocess.call(voice_cmd.strip().split(' '))
            print "[PICO]" + sentence
        except OSError:
            print "[PICO] Speacker is not activate."


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
        rospy.sleep(1.0)
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
            self.speak('There is not male.')
        elif self.male_count == 1:
            self.speak('There is ' + str(self.male_count) + ' male.')
        else:
            self.speak('There are ' + str(self.male_count) + ' males.')
        rospy.sleep(1)
        self.speak("and ")
        rospy.sleep(1)
        #state number of female
        if self.female_count == 0:
            self.speak('There is not female.')
        elif self.female_count == 1:
            self.speak('There is ' + str(self.female_count) + ' female.')
        else:
            self.speak('There are ' + str(self.female_count) + ' females.')
        #state sum of crowd
        self.speak("There are "+str(self.male_count+self.female_count)+" people in total.")
        rospy.sleep(2.0)
        
        return 2 #next state


    def playRiddleGame(self):#----------state 2
        ''' 
            Writter: okano
            Robot is not move in this function.
        '''
        print 'state : 2'
        self.speak("Who want to play riddles with me?")
        #self.speech_req_pub.Publish(True) # start GoogleSpeechAPI's stream voice recognition
        rospy.sleep(3.0)

        # loop 5 times
        reply_count = 0
        while reply_count < 5:
            if self.is_action_state != None:
                print "count : " + str(reply_count)
                self.is_action_state = None
                reply_count += 1

        return 3 #this state


    def startBlindMansBluffGame(self):#--state 3
        ''' 
            Writter: okano
            Robot rotate in this function.
        '''
        print 'state : 3'
        #self.speak("Let play blind mans bluff game")

        # loop 10 times
        reply_count = 0
        failure = None 
        while reply_count < 5:
            if self.is_action_state != None:
                print "count : " + str(reply_count)
                self.rotateVoiceDirection()
                rospy.sleep(1.0) # wait rotate
                if self.is_action_state is True: # Action success.
                    reply_count += 1
                    failure = False
                else: # Action failure.
                    if failure is True:
                        reply_count += 1
                        failure = False
                    else:
                        failure = True

                self.is_action_state = None

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
            
