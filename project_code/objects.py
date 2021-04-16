import qi
from naoqi import ALProxy
import argparse
import sys
import pdb
import time


class Robot:
    IP = "192.168.86.55"
    PORT = 9559
    ACTIONS = ["Yes_1", "Yes_2", "Yes_3", "Please_1", "Explain_1", "Explain_2", "IDontKnow_1", "IDontKnow_2",
               "No_3", "No_8", "No_9"]
    # QUESTIONS = ["Can your person fly?"]
    # TODO populate the whole list of questions
    QUESTIONS = ["Does your person have a mask?",
                 "Is your person human?"]
    roster = ["joker", "wonderWoman", "theFlash", "greenGoblin", "catwoman", "cyborg",
              "theHulk", "captainAmerica", "wolverine", "superman", "ironMan", "aquaman", "mystique", "blackPanther",
              "batman", "harleyQuinn", "spiderman", "thor", "storm"]

    def __init__(self):
        self.attendance = {}
        for i in self.roster:
            self.attendance[i] = 0
        self.tts = ALProxy("ALTextToSpeech", self.IP, self.PORT)
        self.session = qi.Session()
        try:
            self.session.connect("tcp://" + self.IP + ":" + str(self.PORT))
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + self.IP + "\" on port " + str(self.PORT) + ".\n"
                   "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)
        self.action_service = self.session.service("ALAnimationPlayer")
        self.memory = self.session.service("ALMemory")
        # print(self.memory.getData("testKey"))
        self.check_attendance()
        pdb.set_trace()

    def speak(self, string):
        self.tts.say(string)

    def act(self, action):

        # Action list:
        # yes, no, explain, you, warm

        self.action_service.run("animations/Stand/Gestures/"+action, _async=True)
        # future.value()
        # self.action_service.run("animations/Stand/Gestures/"+action)

    def initialize_sharedmemory(self):
        for i in self.roster:
            self.attendance[i] = 0
            self.memory.insertData(self.memory.getData(i), 0)

    def check_attendance(self):
        for r in self.roster:
            if self.memory.getData(r) == 0:
                self.attendance[r] = 1

    def game_start(self):
        self.act("Yes_1")
        self.speak("Would you like to play a game?")
        print("Would human like to start a game? (y/n):")
        answer = raw_input()
        if answer == 'y':
            self.act("Enthusiastic_4")
            self.speak("Yay!")
            return 0
        else:
            self.speak("Okay, maybe next time!")
            self.act("BowShort_1")
            return 1

    def ask_question(self, idx):
        self.act("IDontKnow_2")
        self.speak(self.QUESTIONS[idx])
        print("Human's answer to robot's question:")
        answer = raw_input()
        if answer == 'y':
            self.act("Yes_1")
            self.speak("Hmmm, okay")
        else:
            self.act("No_1")
            self.speak("That's interesting")
        if idx < len(self.QUESTIONS)-1:
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
        if answer == 'y':
            self.act("Yes_1")
            self.speak("Yes!")
            return 0
        else:
            self.act("No_1")
            self.speak("Nope!")
            return 0

    def game(self):
        valid_set = 0
        for hero in self.attendance:
            if self.attendance[hero] == 1:
                valid_set = 1

        if valid_set:
            self.speak("The following characters have been seen:")
            for hero in self.attendance:
                if self.attendance[hero] == 1:
                    self.speak(hero)
        else:
            journey.speak("Nobody Loves Me, Frowny Face Emoji")

        val = self.game_start()
        question_idx = 0
        while val == 0:
            val = self.ask_question(question_idx)
            question_idx += 1
            self.ask_to_answer()
            self.answer_question()


if __name__ == '__main__':
    journey = Robot()
    # journey.speak("Hello everyone")
    # journey.act("Yes_1")
    journey.game()
