import logging
from datetime import datetime

from vocabulary import Vocabulary
from text import Text
from config import *

def delete(vocabulary:Vocabulary) -> None:
    while True:
        logging.info("Delete words")
        Text.clear()
        Text.print(vocabulary.draw(keys=['word', 'tran']), delay=0)
        Text.print('Nothing to Exit', color='green', delay=0)
        index = Text.input('Nr. of Word to Delete -> ', color='green')
        if index == '':
            break
        
        try:
            index = int(index)
        except ValueError:
            logging.info(f'{index} is not number')
            Text.input('Write Number!', color='red')
            continue
        if index >= len(vocabulary) or -len(vocabulary) > index:
            logging.info(f'{index} is out of bounds')
            Text.input('Out of Bounds!', color='red')
            continue
                
        vocabulary.delete(index)