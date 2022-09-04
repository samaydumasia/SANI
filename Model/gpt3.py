# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 16:23:55 2022

@author: samay
"""

import os
import openai

openai.api_key = os.getenv('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')


def gpt3(prompt, engine='davinci', response_length=64,
         temperature=0.7, top_p=1, frequency_penalty=0, presence_penalty=0,
         start_text='', restart_text='', stop_seq=[]):
    response = openai.Completion.create(
        prompt=prompt + start_text,
        engine=engine,
        max_tokens=response_length,
        temperature=temperature,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop_seq,
    )
    answer = response.choices[0]['text']
    new_prompt = prompt + start_text + answer + restart_text
    return answer, new_prompt



