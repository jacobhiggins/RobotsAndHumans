import pandas as pd
import numpy as np
import pdb

class QuestionAnalyzer():
    def __init__(self,filename):
        self.orig_data = pd.read_csv(filename, header=0)
        self.current_data = pd.read_csv(filename, header=0)
        self.questions_idxs = np.arange(0,len(self.current_data.columns)-1) # list of questions not asked yet

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
        question = self.current_data.columns[self.questions_idxs[question_idx+1]]
        subset = self.current_data[question]
        # pdb.set_trace()
        if answer<0.5:
            self.current_data = self.current_data[subset<0.5]
        else:
            self.current_data = self.current_data[subset>0.5]
        mask = np.ones(len(self.questions_idxs),dtype=bool)
        mask[question_index] = False
        self.questions_idxs = self.questions_idxs[mask]
        

if __name__=='__main__':
    filename = "../data/guesswho_superherodata1.csv"
    qa = QuestionAnalyzer(filename)
    faces = ['batman','superman','spiderman','ironman','wonderWoman']
    qa.current_data = qa.current_data[qa.current_data['Name'].isin(faces)]
    pdb.set_trace()
    # ig = qa.get_information_gain()
    while True:
        question_idx = qa.choose_question()
        answer = 0
        if question_idx<0:
            name = qa.current_data['Name'].tolist()
            name = name[0]
            print("Person found: {}".format(name))
            break
        print("Question: {}, Answer: {}".format(qa.current_data.columns[question_idx+1],answer))
        qa.update_current_data(question_idx,answer)
        print(qa.current_data)
    # pdb.set_trace()