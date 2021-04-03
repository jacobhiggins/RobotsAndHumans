from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
import pandas as pd
import graphviz
from sklearn.datasets import load_iris
import pdb

df = pd.read_csv("./data/guesswho_data1.csv", header=0)
pdb.set_trace()