# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 14:49:27 2022

@author: samay
"""

from textblob import TextBlob
print(TextBlob('The experience was bad as hell').sentiment.polarity)
