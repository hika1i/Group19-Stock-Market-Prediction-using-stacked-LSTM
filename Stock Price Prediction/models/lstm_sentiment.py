# -*- coding: utf-8 -*-
"""LSTM-Sentiment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mS6djrz6wJgsyv95otQq7E-faW9dHZHt
"""

from google.colab import drive
drive.mount('/content/drive')

!pip install -r /content/drive/MyDrive/requirements2.txt

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from time import time
import keras
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.layers import LSTM
from keras.optimizers import Adam
from time import time
from keras.callbacks import EarlyStopping
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler()

df = pd.read_csv("/content/drive/MyDrive/newdata/Stock_Data_with_Sentiment_new.csv",parse_dates=True,index_col="Date")
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

xtrain,ytrain,xval,yval,xtest,ytest = train[:,:9],train[:,8],val[:,:9],val[:,8],test[:,:9],test[:,8]

lookback = 60
n_features = 9
train_len = len(xtrain) - lookback
test_len = len(xtest) - lookback
val_len = len(xval) - lookback

x_train = np.zeros((train_len, lookback, n_features))
y_train = np.zeros((train_len))
for i in range(train_len):
    ytemp = i+lookback
    x_train[i] = xtrain[i:ytemp]
    y_train[i] = ytrain[ytemp]


x_test = np.zeros((test_len, lookback, n_features))
y_test = np.zeros((test_len))
for i in range(test_len):
    ytemp = i+lookback
    x_test[i] = xtest[i:ytemp]
    y_test[i] = ytest[ytemp]

x_val = np.zeros((val_len, lookback, n_features))
y_val = np.zeros((val_len))
for i in range(val_len):
    ytemp = i+lookback
    x_val[i] = xval[i:ytemp]
    y_val[i] = yval[ytemp]

model = Sequential() 
model.add(LSTM(100,input_shape = (lookback, n_features), return_sequences=True))
model.add(LSTM(50))
model.add(Dropout(0.15))
model.add(Dense(1))
print(model.summary())
#optimizer = keras.optimizers.Adam(lr=0.000025)

model.compile(loss = 'mse', optimizer = optimizer)
earlystop = EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=80,  verbose=1, mode='min')

start = time()
print("start:",0)
history = model.fit(x_train,y_train, epochs =100, batch_size=120, 
          validation_data=(x_val,y_val),verbose = 1, 
          shuffle = False, callbacks=[earlystop])
print("end:",time()-start)

model.save("/content/drive/MyDrive/models/model-vadercase3.2.h5")
loss = history.history
plt.plot(loss['loss'])
plt.plot(loss['val_loss'])
#plt.savefig("./myplots/loss-vadercase1.jpg")
plt.show()
y_pred = model.predict(x_test)
print("r2_score:",r2_score(y_test,y_pred))

plt.figure(figsize=(15,5))
plt.plot( y_test, '.-', color='blue', label='Real values', alpha=0.5)
plt.plot( y_pred, '.-', color='red', label='Predicted values', alpha=1)
#plt.yticks(range(1500, 4800, 300))
#plt.savefig("./myplots/result-vadercase1.jpg")
plt.title('LSTM with Sentiment Results')
plt.legend()
plt.show()

y_test2 = y_test * (max(df['Close']) - min(df['Close']) ) + min(df['Close'])
y_pred2 = y_pred * (max(df['Close']) - min(df['Close']) ) + min(df['Close'])

from sklearn.metrics import median_absolute_error
median_absolute_error(y_test2, y_pred2)

from sklearn.metrics import mean_squared_error
mean_squared_error(y_test2, y_pred2)

plt.figure(figsize=(10,3))
plt.plot( y_test2, '.-', color='blue', label='Real values', alpha=0.5)
plt.plot( y_pred2, '.-', color='red', label='Predicted values', alpha=1)
plt.yticks(range(2000, 3600, 200))
#plt.savefig("./myplots/result-vadercase1.jpg")
plt.title('LSTM with Sentiment')
plt.legend()
plt.show()