import pandas as pd
import numpy as np
import pdb

class QuestionAnalyzer():
    def __init__(self,filename):
        self.orig_data = pd.read_csv(filename, header=0)
        self.current_data = pd.read_csv(filename, header=0)
        self.questions_idxs = np.arange(1,len(self.current_data.columns)) # list of questions not asked yet

    def get_information_gain(self):
        '''
        Get information gain for each available question
        Return -1 for a question that is not available
        '''
        information_gain = np.array([])
        num_characters = self.current_data.shape[0]
        entropy = np.log2(num_characters)
        for question_idx in self.questions_idxs:
            question = self.current_data.columns[question_idx]
            subset = self.current_data[question]
            data_false = subset[subset<0.5].shape[0]
            data_true = subset[subset>0.5].shape[0]
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
        sorted_questions = self.rank_questions()
        sorted_index = sorted_questions[0]
        return sorted_index

    # def 

if __name__=='__main__':
    filename = "../data/guesswho_superherodata1.csv"
    qa = QuestionAnalyzer(filename)
    # ig = qa.get_information_gain()
    qa.rank_questions()
    pdb.set_trace()