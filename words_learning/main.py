import logging
import os

from config import *
from text import Text
from windows import add, delete, language_choice, learn, list, add_txt

def main():
    Text.clear()
    logging.basicConfig(filename="last.log", level=DEBUG_LEVEL, filemode='w',
                        format=FORMAT)
    logging.info("Start program")
    try:
        vocabulary = language_choice.language_choice()
        vocabulary.load()
    except KeyboardInterrupt:
        return

    try:         
        while True:
            Text.clear()
            option = Text.menu((
                'Learn Words',
                'List Words',
                'Add Words',
                'Add TXT',
                'Delete Words'
            ))
            match option:
                case -1:
                    raise KeyboardInterrupt
                case 1:
                    learn.learn(vocabulary)
                case 2:
                    list.list(vocabulary)
                case 3:
                    add.add(vocabulary)
                case 4:
                    add_txt.add_txt(vocabulary)
                case 5:
                    delete.delete(vocabulary)
                    
    except KeyboardInterrupt:
        logging.info("Stop program")
        Text.clear()
        vocabulary.save()
    

if __name__ == '__main__':
    main()