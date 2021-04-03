import qi
from naoqi import ALProxy
import argparse
import sys
import pdb
import time

class Robot():
    IP = "192.168.86.55"
    PORT = 9559
    ACTIONS = ["Yes_1","Yes_2","Yes_3",
                "Please_1",
                "Explain_1","Explain_2",
                "IDontKnow_1","IDontKnow_2",
                "No_3","No_8","No_9"]
    # QUESTIONS = ["Can your person fly?"]
    QUESTIONS = ["Does your person have a mask?",
                "Is your person human?"]
    def __init__(self):
        self.tts = ALProxy("ALTextToSpeech", self.IP, self.PORT)
        self.session = qi.Session()
        try:
            self.session.connect("tcp://" + self.IP + ":" + str(self.PORT))
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + self.IP + "\" on port " + str(self.PORT) +".\n"
                   "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)
        self.action_service = self.session.service("ALAnimationPlayer")
        self.memory = self.session.service("ALMemory")
        print(self.memory.getData("testKey"))

    def speak(self,string):
        self.tts.say(string)

    def act(self,action):
        '''
        Action list:
        yes, no, explain, you, warm
        '''
        self.action_service.run("animations/Stand/Gestures/"+action, _async=True)
        # future.value()
        # self.action_service.run("animations/Stand/Gestures/"+action)
        

    def game_start(self):
        self.act("Yes_1")
        self.speak("Would you like to play a game?")
        print("Would human like to start a game? (y/n):")
        answer = raw_input()
        if answer=='y':
            self.act("Enthusiastic_4")
            self.speak("Yay!")
            return 0
        else:
            self.speak("Okay, maybe next time!")
            self.act("BowShort_1")
            return 1

    def ask_question(self,idx):
        self.act("IDontKnow_2")
        self.speak(self.QUESTIONS[idx])
        print("Human's answer to robot's question:")
        answer = raw_input()
        if answer=='y':
            self.act("Yes_1")
            self.speak("Hmmm, okay")
        else:
            self.act("No_1")
            self.speak("That's interesting")
        if idx<len(self.QUESTIONS)-1:
            return 0
        else:
            return 1

    def ask_to_answer(self):
        self.act("Explain_1")
        time.sleep(1)
        self.speak("Now you ask me a question")

    def answer_question(self):
        print("Robots answer to humans question(y/n):")
        answer = raw_input()
        if answer=='y':
            self.act("Yes_1")
            self.speak("Yes!")
            return 0
        else:
            self.act("No_1")
            self.speak("Nope!")
            return 0

    def game(self):
        val = self.game_start()
        question_idx = 0
        while val==0:
            val = self.ask_question(question_idx)
            question_idx+=1
            self.ask_to_answer()
            self.answer_question()

if __name__=='__main__':
    journey = Robot()
    # journey.speak("Hello everyone")
    # journey.act("Yes_1")
    journey.game()