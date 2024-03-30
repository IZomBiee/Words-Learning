import logging
from datetime import datetime

from vocabulary import Vocabulary
from text import Text
from config import *

def add(vocabulary: Vocabulary) -> None:
    while True:
        Text.clear()
        logging.info("Add Words")

        Text.print("Write nothing to exit\nSplit words by ,", delay=0, color='green')
        words = Text.input('Write word -> ',
                            color='green').split(',')
        if words[0] == '':break
        trans = Text.input('Write translation -> ',
                            color='green').split(',')
        if trans[0] == '':break


        while True:
            Text.clear()
            Text.print(vocabulary.draw_date(words, trans),delay=0)


            option = Text.menu((
                'Yes',
                'No'
            ), phrase='Correct? -> ')
            Text.clear()
            if option == -1:break
            elif option == 1:
                vocabulary.append(words, trans)
                return
            elif option == 2:
                while True:
                    Text.clear()
                    Text.print(vocabulary.draw_date(words, trans),delay=0)

                    Text.print('Nothing to exit',color='green', delay=0)
                    index = Text.input('Write Nr. of the Wrong Word -> ', color='green')
                    if index == '':
                        break
                    try:
                        index = int(index)
                    except ValueError:
                        Text.input('Write Number!', color='red')
                        continue
                    
                    words.pop(index)
                    trans.pop(index)
            