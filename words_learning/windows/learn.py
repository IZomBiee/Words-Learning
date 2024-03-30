import logging
import time
import random

from text import Text
from config import *
from vocabulary import Vocabulary

def learn(vocabulary: Vocabulary):
    sum_time_start = time.time()
    running = True
    if len(vocabulary) == 0:
        Text.input('No Words!',color='red')
        return
    while running:
        for index, data in enumerate(vocabulary[::-1]):
            index = (len(vocabulary) - index)-1
            time_start = time.time()    
            Text.clear()
            try:
                change = (data['fail'] / data['success']) * CHANCE_MULT
                change += 0.001
            except ZeroDivisionError:
                change = 1
            
            if random.random() < change:
                Text.print(f'Fail:{data['fail']} Success:{data['success']} Change:{round(change, 2)} Time:{round(time.time()-sum_time_start)}s Index:{index}\n\n1 -> Exit', delay=0, color='green')
                Text.print(f"Translation -> ",delay=0, end='', color='green')
                Text.print(data['tran'],delay=0)
                option = Text.input('Write Word -> ', color='green')
                if option == '1':
                    running = False
                    break
                if option.title().strip() == data['word']:
                    Text.input('Success! ', color='green')
                    vocabulary[index]['success'] += 1
                    vocabulary.stats[-1]['success'] += 1
                else:
                    Text.input(f'Not Correct! Correct is {data['word']} ', color='red')   
                    vocabulary[index]['fail'] += 1
                    vocabulary.stats[-1]['fail'] += 1
                    break
            vocabulary.stats[-1]['time_in_learning'] += round(time.time()-time_start)
        


