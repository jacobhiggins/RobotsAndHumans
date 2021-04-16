import qi
from naoqi import ALProxy
import argparse
import sys
import pdb
import time
import pandas as pd
import numpy as np


class QuestionAnalyzer():
    def __init__(self,filename):
        self.orig_data = pd.read_csv(filename, header=0)
        self.current_data = pd.read_csv(filename, header=0)
        self.questions_idxs = np.arange(0,len(self.current_data.columns)-1) # list of questions not asked yet

    def faces_in_play(self,faces_list):
        '''
        Gets list of strings of faces that are in play
        Changes self.current_data to have only these faces
        '''
        self.current_data = self.current_data[self.current_data['Name'].isin(faces_list)]

    def get_information_gain(self):
        '''
        Get information gain for each available question
        Return -1 for a question that is not available
        '''
        information_gain = np.array([])
        num_characters = self.current_data.shape[0]
        entropy = np.log2(num_characters)
        for question_idx in self.questions_idxs:
            question = self.current_data.columns[question_idx+1] # offset since first column is name
            subset = self.current_data[question]
            data_false = subset[subset<0.5].shape[0]
            data_true = subset[subset>0.5].shape[0]
            if data_true==num_characters or data_false==num_characters:
                conditional_entropy = entropy
            else:
                conditional_entropy = (float(data_false)/num_characters)*np.log2(data_false) + (float(data_true)/num_characters)*np.log2(data_true)
            information_gain = np.append(information_gain,entropy-conditional_entropy)
            # pdb.set_trace()
        return information_gain
            
    def rank_questions(self):
        information_gain = self.get_information_gain()
        sorted_questions = np.argsort(information_gain) # find indices to sort from smallest to greatest
        sorted_questions = sorted_questions[::-1] # sort from greatest to least
        return sorted_questions
        # pdb.set_trace()

    def choose_question(self):
        '''
        Chooses a question to ask human
        Returns index of question to ask
        Returns -1 if there is only one person left
        '''
        if self.current_data.shape[0]==1:
            return -1
        sorted_questions = self.rank_questions()
        question_idx= sorted_questions[0]
        return question_idx

    def update_current_data(self,question_index,answer):
        '''
        Given question index and humans answer, update current data df and array of question idxs
        '''
        question = self.current_data.columns[self.questions_idxs[question_index+1]]
        subset = self.current_data[question]
        # pdb.set_trace()
        if answer<0.5:
            self.current_data = self.current_data[subset<0.5]
        else:
            self.current_data = self.current_data[subset>0.5]
        mask = np.ones(len(self.questions_idxs),dtype=bool)
        mask[question_index] = False
        self.questions_idxs = self.questions_idxs[mask]

class Robot:
    IP = "192.168.86.55"
    PORT = 9559
    ACTIONS = ["Yes_1", "Yes_2", "Yes_3", "Please_1", "Explain_1", "Explain_2", "IDontKnow_1", "IDontKnow_2",
               "No_3", "No_8", "No_9"]
    # QUESTIONS = ["Can your person fly?"]
    # TODO populate the whole list of questions
    QUESTIONS = ["Does your person have a mask?",
                 "Is your person wearing a helmet?",
                 "Does your person have hair that is visible?",
                 "Is your person a male?",
                 "Is your person a Marvel superhero?",
                 "Is your person a DC superhero?",
                 "Does your person have facial hair?",
                 "Is your person a hero?",
                 "Is your person a villian?",
                 "Can your person fly?",
                 "Is your person an Avenger?",
                 "Is your person in the Justice League?",
                 "Is your person an X-man?"]
    roster = ["joker", "wonderWoman", "theFlash", "greenGoblin", "catwoman", "cyborg",
              "theHulk", "captainAmerica", "wolverine", "superman", "ironMan", "aquaman", "mystique", "blackPanther",
              "batman", "harleyQuinn", "spiderman", "thor", "storm", "blackWidow"]

    def __init__(self):
        self.qa = QuestionAnalyzer("../data/guesswho_superherodata1.csv")
        self.attendance = {}
        self.selected_characters = []
        self.head_pat = 0
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
        self.initialize_shared_memory()
        # self.check_attendance()
        # pdb.set_trace()

    def speak(self, string):
        self.tts.say(string)

    def act(self, action):

        # Action list:
        # yes, no, explain, you, warm

        self.action_service.run("animations/Stand/Gestures/"+action, _async=True)
        # future.value()
        # self.action_service.run("animations/Stand/Gestures/"+action)

    # Returns list of selected characters
    def get_selected_characters(self):
        return self.selected_characters

    # Sets all values in the shared memory to zero, and sets all stored attendance values to zero.
    # Also resets selected characters
    def initialize_shared_memory(self):
        for i in self.roster:
            self.attendance[i] = 0
            self.memory.insertData(i, 0)
        self.selected_characters = []
        self.head_pat = 0

    def check_attendance(self):
        for r in self.roster:
            if self.memory.getData(r) == 1:
                self.attendance[r] = 1
            else:
                self.attendance[r] = 0

    def game_start(self):
        self.act("Yes_1")
        self.speak("Would you like to play a game?")
        print("Would human like to start a game? (y/n):")
        answer = raw_input()
        if answer == 'y':
            self.act("Enthusiastic_4")
            self.speak("Yay!")
            self.speak("Please show me a set of characters that you would like to play with.")
            self.speak("Pat my head when you've finished")
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
            return 1
        else:
            self.act("No_1")
            self.speak("That's interesting")
            return 0
        

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

    def roll_call(self):
        self.check_attendance()
        valid_set = 0
        for hero in self.attendance:
            if self.attendance[hero] == 1:
                valid_set = 1

        if valid_set:
            self.speak("The following characters have been selected:")
            for hero in self.attendance:
                if self.attendance[hero] == 1:
                    self.selected_characters.append(hero)
                    self.speak(hero)

        else:
            self.speak("No Characters Have Been Selected.")
            self.speak("Please show me at least one character before patting my head again.")
            # self.speak("Fuck this bullshit!")
            self.head_pat = 0
            self.memory.insertData("headPat", 0)
            self.observe_faces()

    def observe_faces(self):
        self.head_pat = 0
        self.memory.insertData("headPat", 0)
        while self.head_pat != 1:
            self.head_pat = self.memory.getData("headPat")
        self.roll_call()

    def game(self):
        val = self.game_start()
        self.observe_faces()
        faces_list = self.get_selected_characters()
        self.qa.faces_in_play(faces_list)
        pdb.set_trace()
        question_idx = 0
        while True:
            question_idx = self.qa.choose_question()
            if question_idx<0:
                name = self.qa.current_data['Name'].tolist()
                name = name[0]
                self.speak("I figured out your person!")
                self.speak("You are thinking of {}".format(name))
                break
            answer = self.ask_question(question_idx)
            self.qa.update_current_data(question_idx,answer)
            self.ask_to_answer()
            self.answer_question()


if __name__ == '__main__':
    journey = Robot()
    # journey.speak("Hello everyone")
    # journey.act("Yes_1")
    journey.game()
