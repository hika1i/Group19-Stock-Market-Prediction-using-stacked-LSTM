# -*- coding: utf-8 -*-
"""LSTM-Pure.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KVG8DjaRssEzmxAOtnB4x73d7zyGHN5z
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install -r requirements.txt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from time import time
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.layers import LSTM
from keras.optimizers import Adam
from time import time
from keras.callbacks import EarlyStopping
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler()

df = pd.read_csv("./Stock_Data.csv",parse_dates=True,index_col="Date")
df

print("--scaling data---")
data = sc.fit_transform(df)

train_ind = int(0.6*len(df))
val_ind = train_ind + int(0.2*len(df))

train = data[:train_ind]
val = data[train_ind:val_ind]
test = data[val_ind:]

print("--shapes--")
print("train,test,val",train.shape, test.shape, val.shape)

xtrain,ytrain,xval,yval,xtest,ytest = train[:,:6],train[:,5],val[:,:6],val[:,5],test[:,:6],test[:,5]

lookback = 60
n_features = 6
train_len = len(xtrain) - lookback
test_len = len(xtest) - lookback
val_len = len(xval) - lookback

x_train = np.zeros((train_len, lookback, n_features))
y_train = np.zeros((train_len))
for i in range(train_len):
    ytemp = i+lookback
    x_train[i] = xtrain[i:ytemp]
    y_train[i] = ytrain[ytemp]
print("x_train", x_train.shape)
print("y_train", y_train.shape)

x_test = np.zeros((test_len, lookback, n_features))
y_test = np.zeros((test_len))
for i in range(test_len):
    ytemp = i+lookback
    x_test[i] = xtest[i:ytemp]
    y_test[i] = ytest[ytemp]
print("x_test", x_test.shape)
print("y_test", y_test.shape)

x_val = np.zeros((val_len, lookback, n_features))
y_val = np.zeros((val_len))
for i in range(val_len):
    ytemp = i+lookback
    x_val[i] = xval[i:ytemp]
    y_val[i] = yval[ytemp]
print("x_val", x_val.shape)
print("y_val", y_val.shape)

model = Sequential() 
model.add(LSTM(100,input_shape = (lookback, n_features), return_sequences=True))
model.add(LSTM(50))
model.add(Dropout(0.15))
model.add(Dense(1))
print(model.summary())

model.compile(loss = 'mse', optimizer = 'adam')
earlystop = EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=80,  verbose=1, mode='min')

start = time()
print("start:",0)
history = model.fit(x_train,y_train, epochs =100, batch_size=120, 
          validation_data=(x_val,y_val),verbose = 1, 
          shuffle = False, callbacks=[earlystop])
print("end:",time()-start)

#model.save("./mymodels/model-vadercase1.h5")
loss = history.history
plt.plot(loss['loss'])
plt.plot(loss['val_loss'])
#plt.savefig("./myplots/loss-vadercase1.jpg")
plt.show()
y_pred = model.predict(x_test)
print("r2_score:",r2_score(y_test,y_pred))

plt.figure(figsize=(20,10))
plt.plot( y_test, '.-', color='red', label='Real values', alpha=0.5)
plt.plot( y_pred, '.-', color='blue', label='Predicted values', alpha=1)
#plt.savefig("./myplots/result-vadercase1.jpg")
plt.show()