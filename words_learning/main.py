import logging
import os

from config import *
from text import Text
from windows import Windows

def main():
    Text.clear()
    logging.basicConfig(filename="last.log", level='DEBUG', filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s: %(message)s')
    logging.info("Start program")
    
    try:
        try:
            vocabulary = Windows.language_choice()
        except KeyboardInterrupt:
            exit()
        vocabulary.load()
        windows = Windows(vocabulary)
        while True:
            Text.clear()
            option = Text.menu((
                'Learn',
                'Add',
                'Add txt',
                'Delete',
                'Change',
                'List',
                'Statistic'
            ))
            match option:
                case -1:
                    raise KeyboardInterrupt
                case 1:
                    windows.learn()
                case 2:
                    windows.add()
                case 3:
                    windows.add_txt()
                case 4:
                    windows.delete()
                case 5:
                    windows.change()
                case 6:
                    windows.list()
                case 7:
                    windows.statistic()
    except KeyboardInterrupt:
        logging.info("Stop program")
        Text.clear()
        vocabulary.save()
    

if __name__ == '__main__':
    main()