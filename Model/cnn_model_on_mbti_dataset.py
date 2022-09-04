# -*- coding: utf-8 -*-
"""CNN Model on MBTI dataset.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MLrWT4iTYaWFDXiY1IXYJ5OUcQXwN2w8

## Importing the Necessary Libraries
"""

from keras.preprocessing import sequence, text
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding, LSTM
from keras.layers import Conv1D, Flatten, MaxPooling1D

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

"""## Setting the Hyperparameters
These will be required for building the neural network. We can play around with these and they will largely affect the accuracy of our model
"""

vocab_size = 1000
max_len =1000
batch_size = 32
embedding_dims =100
filters = 16
ker_size = 3 # kernel size
hidden_dims = 250
epochs = 100

"""## Reading the Dataset from CSV file"""

data = pd.read_csv('mbti_cleaned.csv')
data.dropna(axis=0,how="all") # ignoring the NaN values

data.type.unique()

#@title Default title text
first = []
second = []
third = []
fourth = []
set_to_one = ['E', 'S', 'T', 'J']
for x in data.type:
  for idx, curr in enumerate(x):
    if idx == 0:
      if curr == 'E':
        first.append(1)
      else:
        first.append(0)
    elif idx == 1:
      if curr == 'S':
        second.append(1)
      else:
        second.append(0)
    elif idx == 2:
      if curr == 'T':
        third.append(1)
      else:
        third.append(0)
    else:
      if curr == 'J':
        fourth.append(1)
      else:
        fourth.append(0)

data['Is E'] = pd.Series(first)
data['Is S'] = pd.Series(second)
data['Is T'] = pd.Series(third)
data['Is J'] = pd.Series(fourth)
data.head()

y = pd.DataFrame(data, columns = ['Is E', 'Is S', 'Is T','Is J'])
print(y)

data['Posts'] = data['Posts'].astype(str)

# One Hot encoding on the dataset output classes 
x_train,x_test,y_train,y_test = train_test_split(data['Posts'], y,random_state=0)
y



tokenizer = text.Tokenizer(num_words=vocab_size)
tokenizer.fit_on_texts(x_train)

x_train = tokenizer.texts_to_matrix(x_train)
x_test = tokenizer.texts_to_matrix(x_test)

x_train = sequence.pad_sequences(x_train,maxlen=max_len)
x_test = sequence.pad_sequences(x_test,maxlen=max_len)

"""## Building the Sequential Neural Network using Keras"""

model = Sequential()
# First we add an embedding layer 
model.add(Embedding(vocab_size,embedding_dims,input_length=max_len)) 
# Adding a 1D convolutional Layer
model.add(Conv1D(256, ker_size, padding='valid', activation='relu'))
model.add(MaxPooling1D())
model.add(Conv1D(128, ker_size, padding='valid', activation='relu'))
# Max Pooling the Convolutions
model.add(MaxPooling1D())
# Again Computing the Convolutions
model.add(Flatten())
model.add(Dense(2048, activation='relu'))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))


model.add(Dense(4, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Training the modeL
model.fit(x_train,y_train, batch_size=batch_size, epochs=10, validation_data=(x_test, y_test))

"""## Evaluating the Performance of the Model"""

model.evaluate(x_test,y_test)[1]*100  # Accuracy of the model

model.evaluate(x_test,y_test)[1]*100  # Accuracy of the model

# Saving the model into a pickle file 
import pickle
pickle.dump(model,open('cnn_model.pkl','wb'))

pickle.dump(tokenizer,open('tokenizer','wb'))

"""# For Single Input """

#s ='Idealistic, loyal to their values and to people who are important to them. Want an external life that is congruent with their values. Curious, quick to see possibilities, can be catalysts for implementing ideas. Seek to understand people and to help them fulfill their potential. Adaptable, flexible, and accepting unless a value is threatened.'
s = '  interested hat is congruent with their values. Curious, quick to see possibilities, can be catalysts for implementing ideas. Seek to understand people and to help them fulfill their potential. Adaptable, flexible, and accepting unless a value is threatened.  '
s = pd.Series(s)
s= tokenizer.texts_to_matrix(s)
s = sequence.pad_sequences(s)
l = model.predict(s)
print(l)

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


