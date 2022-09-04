# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 04:05:17 2022

@author: samay
"""

from keras.preprocessing import sequence, text
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding, LSTM
from keras.layers import Conv1D, Flatten, MaxPooling1D

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

vocab_size = 1000
max_len =1000
batch_size = 32
embedding_dims =10
filters = 16
ker_size = 3 # kernel size
hidden_dims = 250
epochs = 10


data = pd.read_csv('mbti_cleaned.csv')
data.dropna(inplace=True)  # ignoring the NaN values


# One Hot encoding on the dataset output classes 

from numpy import asarray
from sklearn.preprocessing import OneHotEncoder
# define data
data = asarray([data['type']])
print(data)
# define one hot encoding
encoder = OneHotEncoder(drop='first', sparse=False)
# transform data
y = encoder.fit_transform(data)
print(y)

x_train,x_test,y_train,y_test = train_test_split(data['Posts'], y,random_state=0)


tokenizer = text.Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(x_train)


x_train = tokenizer.texts_to_matrix(x_train)
x_test = tokenizer.texts_to_matrix(x_test)


x_train = sequence.pad_sequences(x_train,maxlen=max_len)
x_test = sequence.pad_sequences(x_test,maxlen=max_len)


model = Sequential()
# First we add an embedding layer 
model.add(Embedding(vocab_size,embedding_dims,input_length=max_len)) 
# Adding a 1D convolutional Layer
model.add(Conv1D(filters, ker_size, padding='valid', activation='relu'))
# Max Pooling the Convolutions
model.add(MaxPooling1D())
# Again Computing the Convolutions
model.add(Flatten())
model.add(Dense(hidden_dims, activation='relu'))
model.add(Dense(4, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])


# Training the modeL
model.fit(x_train,y_train, batch_size=batch_size, epochs=5, validation_data=(x_test, y_test),)


model.evaluate(x_test,y_test)[1]*100  # Accuracy of the model


model.evaluate(x_test,y_test)[1]*100  # Accuracy of the model



# Saving the model into a pickle file 
import pickle
pickle.dump(model,open('cnn_model.pkl','wb'))

pickle.dump(tokenizer,open('tokenizer','wb'))


s ='Idealistic, loyal to their values and to people who are important to them. Want an external life that is congruent with their values. Curious, quick to see possibilities, can be catalysts for implementing ideas. Seek to understand people and to help them fulfill their potential. Adaptable, flexible, and accepting unless a value is threatened.'
s = pd.Series(s)
s= tokenizer.texts_to_matrix(s)
s = sequence.pad_sequences(s)
l = model.predict(s)
a,b= l[0][0]*(1/1999), l[0][1]*(1/1197)
a = a/(1/1999)+(1/1197)
b = b/(1/1999)+(1/1197)
l = [a,b,l[0][2],l[0][3]]
s=''
if l[0] >0.5:
    s +='E'
else:
    s+='I'
if l[1] >0.5:
    s+='S'
else:
    s+='N'
if l[2] >0.5:
    s+='T'
else:
    s+='F'
if l[3] >0.5:
    s+='J'
else:
    s+='P'
print('Your Personality is:',s)


