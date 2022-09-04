# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 23:25:32 2022

@author: samay
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May  2 05:52:26 2021

@author: samay
"""


from tkvideo import tkvideo

import cv2

from tkinter import *
import pyttsx3
import speech_recognition as sr


import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import os
import wikipedia #pip install wikipedia
from bot import ask

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

x = "AI_model.mp4" 
y = "temp.mp4"


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = ask(msg)
    return res


#Creating GUI with tkinter
import tkinter
from tkinter import *


def send():
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    
    if "Weather" in msg:
        res = str(Weather())
        speak(res)
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        
    
    elif "your age" in msg:
        res = "i am 20 years old"
        print(res)
        speak(res)
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        flag = 1
        
    elif "how old" in msg:
        res = "i am 19 years old"
        print(res)
        speak(res)
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        flag = 1
    
    elif "birthday" in msg:
        res = "my birthday is on 21st april"
        print(res)
        speak(res)
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        flag = 1     
        
    elif "search" in msg:
        print('Searching Wikipedia...')
        res = msg.replace("search", "")
        res = wikipedia.summary(res, sentences=2)
        print(res)
        speak(res)
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
        
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        flag = 1

        
    elif msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')
        speak(res)
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)
        

    
    
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
 

    
    

window = Tk()
window.geometry("1200x600")
window.title('SANIHA')
window["bg"]="darkgreen"


bg = PhotoImage(file = "back screen.png")

label1 = Label( window, image = bg)
label1.place(x = 10, y = 10, height=580,width=1180, anchor=NW)




f1=Frame()
l1 = Label(window)



player = tkvideo("image.mp4", l1, loop = 1, size = (800,500))

f1.place(x=0,y=0)
l1.place(x=50, y=50, height=500, width=600, anchor=NW)
player.play()


ChatLog = Text(window, bd=10, bg="lightblue",  font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(window, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(window, text="Send", width=16,height=2,bg="lightgreen", 
                    activeforeground = "black",activebackground = "green",
                    command= send )

#Create the box to enter message
EntryBox = Text(window, bd=5, bg="white",width="40",height="2")
#EntryBox.bind("<Return>", send)


#Place all components on the screen
scrollbar.place(x=1130,y=50, height=430)
ChatLog.place(x=675,y=50, height=430, width=455)
EntryBox.place(x=675,y=505)
SendButton.place(x=1030,y=506)
# train = Button(window,text ='Train',command=train,width=10,bg="lightyellow")
# train.place(x=1356,y=757)




    
window.mainloop()