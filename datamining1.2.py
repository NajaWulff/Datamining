#!/usr/bin/python

"""Hand-in code for the assignment of the Data Mining part of the
course Databases and Data Mining
"""

__author__ = 'Naja Wulff Mottelson'
__version__= '1.1'
__modified__='27032012'

# import SQLite database engine 
import sqlite3 as sql
import numpy as num 

# connect to database and get cursor
sqlserver = sql.connect("DataMiningAssignment.db")
cursor = sqlserver.cursor()

# calculate mean of fish length in database
mean_data = cursor.execute("select avg(length) from Fish_Y")
mean = mean_data.fetchall()[0][0]
print("Mean fish legth: " + str(mean))

# calculate variance of fish lengths in database
response_data  = (cursor.execute("select length from Fish_Y")).fetchall()
fishlengths = []
for x in response_data:
   fishlengths.append((float(x[0])))

return_sum = 0
for x in fishlengths:
    return_sum += ((x - mean)**2) // len(fishlengths)

print("Variance: " + str(return_sum))

#Get input data and turn it into 3x24 matrix padded with ones
input_data = (cursor.execute("select age, temperature from Fish_X")).fetchall()
input = []
for x in input_data:
    input.append((float(x[0]), float(x[1]), 1))

input_matrix = num.matrix(input)

#Turn response data into 1x24 matrix
ys = []
for y in response_data:
    ys.append(float(y[0]))

response_matrix = num.matrix(ys)

#calculate the algorithm's parameters
wT =((input_matrix.T * input_matrix).I) * (input_matrix.T * response_matrix.T)

#define the affine linear model
def model(x0, x1): 
    return x0 * wT[0, 0] + x1 * wT[1, 0] + wT[2, 0]

#calculate mean squared error
def mse(x, y, wT):
    pred = []
    for i in range(0, len(x)):
        y_pred = model(x[i, 0], x[i, 1])
        y_real = y[0, i]
        pred.append((y_pred - y_real)**2)
    return sum(pred) // len(x)

MSE = mse(input_matrix[:, :-1], response_matrix, wT)
print("MSE: " + str(MSE))
cursor.close()
sqlserver.close()
