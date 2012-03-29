"""Hand-in code for the assignment of the Data Mining part of the
course Databases and Data Mining
"""

__author__ = 'Naja Wulff Mottelson'
__version__= '1.0'
__modified__='29032012'

# import SQLite database engine 
import sqlite3 as sql
import numpy as num 
import random

# connect to database and get cursor
sqlserver = sql.connect("DataMiningAssignment.db")
cursor = sqlserver.cursor()

# import input data from database
x_data = cursor.execute("select X0, X1, X2, X3, X4, X5, X6, X7 from Yeast_Train_X")
X = x_data.fetchall()
y_data = cursor.execute("select Y from Yeast_Train_Y")
Y = y_data.fetchall()

# calculate euclidean distance
def dist(p, q):
   return  num.linalg.norm(num.array(p) - num.array(q)) 

# calculate nearest neighbour classification
def train_classifier(X, Y): 
    train_set = zip(X, Y)
    def classify(x):
       distances = []
       for (xi, yi) in train_set:
          distances.append((dist(x, xi), yi))
       return min(distances)[1]
    return(classify)

# get test data from database
xtest_data = cursor.execute("select X0, X1, X2, X3, X4, X5, X6, X7\
                                 from Yeast_Test_X")
Xtest = xtest_data.fetchall()
ytest_data = cursor.execute("select Y from Yeast_Test_Y")
Ytest = ytest_data.fetchall()

# test the 1-nn algorithm on the test data
def test_classify(classify):
    correct = 0
    incorrect = 0
    for (x, y) in zip(Xtest, Ytest):
       pred = classify(x)
       if pred == y:
          correct += 1
       else:
          incorrect += 1
    return (correct, incorrect)

print(test_classify(train_classifier(X, Y)))

#define a classifier choosing y values at random
def random_classifier(x):
   return (random.randint(0, 9),)

# test the random classifier on the test data
print(test_classify(random_classifier))

