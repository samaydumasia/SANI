# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 02:40:02 2022

@author: samay
"""

import os
import openai

os.environ['OPENAI_KEY'] = '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'


openai.api_key = os.environ['OPENAI_KEY']


completion = openai.Completion()

start_chat_log = '''Human: Hello, who are you?
AI: I am doing great. How can I help you today?
'''

def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=10)
    answer = response.choices[0].text.strip()
    return answer


if __name__ == '__main__':
    print(ask('hi'))