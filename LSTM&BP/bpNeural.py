# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas
import numpy
import keras
from keras.layers.core import Dense, Activation, Dropout
from keras.layers import LeakyReLU
from keras.models import Sequential
import matplotlib.pyplot as plt

CONST_TRAINING_SEQUENCE_LENGTH = 7
CONST_TESTING_CASES = 18
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def dataNormalization(nondata):
    return (nondata - nondata.mean())/(nondata.max()-nondata.min()) 
    #return (nondata - nondata.mean())/(nondata.std()) 
def dataDeNormalization(data,datamax,datamin,datamean,datastd):
    return data*(datamax-datamin) + datamean
    #return (data*datastd + datamean)

def getDeepLearningData(ticker):
     #Load data,build xsum
    
    xsum = []
    data = pandas.read_excel('/Users/houjiani/Downloads/作业/srtp/'+ticker+'.xlsx')[
    'Solar Radiation, W/m^2, SEU ARCH solar radiation'].tolist()
    
    
    #Building xsum
    for i in range(len(data) - 133 ):
        dataSegment = data[i:i + CONST_TRAINING_SEQUENCE_LENGTH]
        xsum1 = 0
        for j in range(len(dataSegment)-1):
            xsum1 += dataSegment[0]-dataSegment[j+1]
        xsum.append(xsum1/6)

        
    front = (CONST_TESTING_CASES+ 1) * CONST_TRAINING_SEQUENCE_LENGTH
    back = CONST_TESTING_CASES * CONST_TRAINING_SEQUENCE_LENGTH
    while front>CONST_TRAINING_SEQUENCE_LENGTH:
        dataSeg = data[-front:-back]
        xsum2 = 0
        for j in range(len(dataSeg)-1):
            xsum2 += dataSeg[0]-dataSeg[j+1]
        xsum.append(xsum2/6)
        front = front - 1
        back = back - 1
        
    #normalizing data
    predata = pandas.DataFrame(data)
    integratedata = predata.append(xsum)
    #nordata = dataNormalization(integratedata)
    nordata = integratedata
    DATA_MAX = integratedata.max()
    DATA_MIN = integratedata.min()
    DATA_STD = integratedata.std()
    DATA_MEAN = integratedata.mean()
    
    
    #spliting data
    
    #调试
    
    #xArray = numpy.array(integratedata[:predata.shape[0]]).tolist()
    #sumArray = numpy.array(integratedata[predata.shape[0]:integratedata.shape[0]]).tolist()
    
    xArray = numpy.array(nordata[:predata.shape[0]]).tolist()
    sumArray = numpy.array(nordata[predata.shape[0]:integratedata.shape[0]]).tolist()
    
    #building X_Training,Y_Training
    flag = 0
    X_Training = []
    Y_Training = []
    for i in range(len(xArray) - 133 ):
        dataSegment = xArray[i:i + CONST_TRAINING_SEQUENCE_LENGTH]
        dataSegment.append(sumArray[flag])
        Y_Training.append(xArray[i + CONST_TRAINING_SEQUENCE_LENGTH+1])
        flag += 1
        X_Training.append(dataSegment)
    X_Training = numpy.array(X_Training)
    Y_Training = numpy.array(Y_Training)

    
    #building X_Testing,Y_Testing
    X_Testing = []
    front = (CONST_TESTING_CASES+ 1) * CONST_TRAINING_SEQUENCE_LENGTH
    back = CONST_TESTING_CASES * CONST_TRAINING_SEQUENCE_LENGTH
    while front>CONST_TRAINING_SEQUENCE_LENGTH:
        dataSeg = xArray[-front:-back]
        dataSeg.append(sumArray[flag])
        X_Testing.append(dataSeg)
        front = front - 1
        back = back - 1
    Y_Testing = xArray[-CONST_TESTING_CASES * CONST_TRAINING_SEQUENCE_LENGTH:]
    X_Testing = numpy.array(X_Testing)
    Y_Testing = numpy.array(Y_Testing)
    
    X_Training = numpy.reshape(X_Training,(X_Training.shape[0], X_Training.shape[1]))
    X_Testing = numpy.reshape(X_Testing,(X_Testing.shape[0], X_Testing.shape[1]))
    
    
    
    return X_Training, Y_Training, X_Testing, Y_Testing,  DATA_MAX, DATA_MIN, DATA_STD, DATA_MEAN

def predict(model, X):
    predictionsNormalized = []
    
    for i in range(len(X)):
        
        data = X[i]
        #print(data)
        predicted = model.predict(data[numpy.newaxis, :])[0, 0]
        #print(predicted)
        predictionsNormalized.append(predicted)

    return predictionsNormalized


def plotResults(Y_Hat, Y):
    plt.plot(Y)
    Y_Hat = numpy.reshape(Y_Hat, (CONST_TRAINING_SEQUENCE_LENGTH*CONST_TESTING_CASES, 1))
    plt.plot(Y_Hat)
    xValue = list(range(0, CONST_TRAINING_SEQUENCE_LENGTH*CONST_TESTING_CASES))
    plt.scatter(xValue, Y_Hat, s=20, c='#FF0000', marker='.')
    plt.scatter(xValue, Y, s=20, c='#000000', marker='.')
    #print(Y)
    #print(Y_Hat)
    plt.show()
    
    Y_Hat = pandas.DataFrame(Y_Hat)
    Y = pandas.DataFrame(Y)
    new = pandas.concat([Y_Hat, Y], axis=1)
    print(new)
    new.to_excel("bp太阳辐射总值预测总值.xlsx",sheet_name='Sheet1')
    print(Y,Y_Hat)
    


def predictLSTM(ticker):
    # Step 1. Load data
    X_Training, Y_Training, X_Testing, Y_Testing, DATA_MAX, DATA_MIN, DATA_STD, DATA_MEAN  = getDeepLearningData(ticker)
    
    # Step 2. Build model
    keras.activations.relu(x = X_Training, alpha=0.0, max_value=None, threshold= -1.0)
    model = Sequential()
    model.add(Dense(64, input_dim=8))
    model.add(LeakyReLU(alpha=0.2))
    #model.add(Activation('tanh'))
    model.add(Dropout(0.05))

    model.add(Dense(100,))
    model.add(Dropout(0.2))

    model.add(Dense(output_dim=1))
    model.add(LeakyReLU(alpha=0.5))
    #model.add(Activation('tanh'))
    keras.optimizers.Adam(lr=0.00001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
    keras.optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
    model.compile(loss='mse', optimizer="Adam")

    
    model.fit(X_Training, Y_Training,
              batch_size=64,
              epochs=120,
              validation_split=0.05)
    
    print(model.summary())
    #Predict
    predictionsNormalized = predict(model, X_Testing)
    print(predictionsNormalized)
    #De-normalize
    predictions = []
    Y_Testings = []
    
    for i, row in enumerate(predictionsNormalized):
        predictions.append(dataDeNormalization(row, DATA_MAX, DATA_MIN, DATA_MEAN, DATA_STD))
    
    for i, row in enumerate(Y_Testing):
        Y_Testings.append(dataDeNormalization(row, DATA_MAX, DATA_MIN, DATA_MEAN, DATA_STD))
       
    #Plot
    plotResults(predictionsNormalized, Y_Testing)
    #plotResults(predictions, Y_Testings)
    
    


predictLSTM(ticker='solarsum')

