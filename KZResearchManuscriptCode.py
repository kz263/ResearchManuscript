# -*- coding: utf-8 -*-

## Import Relevent Libraries
import numpy as np ##Maths functions and arrays
import csv         ##CSV file reader
from sklearn.neighbors import KNeighborsClassifier   ##KNN algorithm code
from collections import Counter                      ##Counter of entities in array
import serial                                        ##Arduino Serial read library

## Read the arduino USB
ser = serial.Serial('COM3', 9600, timeout=0.05)         # 1/timeout is the frequency at which the port is read
## Define Variables
ValidValues = []

## Training data imported from CSV
def TestingData(Type):
    file = open('KNNTrainingDataCSV.csv')
    type(file)
    csvreader = csv.reader(file)
    rows =[]
    for row in csvreader:
        rows.append(row)
    Values = np.zeros([len(rows),2])
    for j in range(len(rows)):

        Values[j] = rows[j]
    SplitValues = np.array_split(Values,9)
    MechValues = np.concatenate((SplitValues[0],SplitValues[1],SplitValues[2],SplitValues[3],SplitValues[8]))
    OvenValues = np.concatenate((SplitValues[4],SplitValues[5],SplitValues[6],SplitValues[7],SplitValues[8]))
    ## Selection of training data depending if Mechanical / Temperature deformation sample
    if Type == "Oven":
        X = OvenValues[:,0]
        classes = OvenValues[:,1]
    if Type == "Mech":
        X = MechValues[:,0]
        classes = MechValues[:,1]
    return X, classes

## initialise KNN algorithm using k value and training data
def InitialiseKNN(k,Type):
    ## Define Constants for KNN
    x , classes = TestingData(Type) ## Select Training data ("Oven" // "Mech")
    y = np.zeros(len(x))
    
    data = list(zip(x, y))
    knn = KNeighborsClassifier(n_neighbors = k)
    knn.fit(data, classes)
    return knn

## predict deformation state using KNN
def ValuePredictionFunc(X, knn):
    newX = X
    newY = 0
    newPoint = [(newX, newY)]
    prediction = knn.predict(newPoint)
    return prediction

## calculate deformation prediction with differnt K values
def OutputFunc(Type):
    Output = [[]] * 3
    for i in range(3):
        ## Vary K values 10/15/20
        knn = InitialiseKNN( (i * 5) + 10 ,Type)
        ValuePrediction = []
        ## calculate deformation prediction for all 30 samples
        for j in range(30):
            prediction = ValuePredictionFunc(ValidValues[j], knn)
            ValuePrediction.append(prediction[0])
        ## Print k values & number of deformation predictions from 30 sample
        print("k = ", ((i*5)+10))
        print(Counter(ValuePrediction))
        Output[i] = ValidValues
    return Output

## Calculate first 30 valid values
# Loop until 30 valid values are recorded
while len(ValidValues) < 30:

    ##Read Serial input from arduino
    SerData = ser.readline().decode().strip()
    ##If no value coming from arduino print "null"
    if SerData == "":
        print("null")
    else:
        ## If the value is valid, above error signal and below maximum peak save it
        if (int(SerData) > 90) & (int(SerData) < 1000):
            ValidValues.append(int(SerData))
            
        ## Print information depending on range of data
        if int(SerData) > 1000:
            print("ERROR....ERROR....ERROR....ERROR....ERROR....ERROR....ERROR....ERROR....ERROR....ERROR....")
        if (int(SerData) < 1000) & (int(SerData) > 600):
            print("600 - 1000   High Values ----- High Values -----  600 - 1000")
        
        if (int(SerData) < 600) & (int(SerData) > 300):
            print("300 - 600 Medium Medium Medium  300 - 600")
            
        if (int(SerData) < 300) & (int(SerData) > 90):
            print("100 - 300   low .....   100 - 300")

Output = OutputFunc("Mech")

ValuePrediction = []

knn = InitialiseKNN(15,"Oven")
for i in range(30):
    prediction = ValuePredictionFunc(ValidValues[i], knn)
    ValuePrediction.append(prediction[0])
#print deformation predictions
print(Counter(ValuePrediction))