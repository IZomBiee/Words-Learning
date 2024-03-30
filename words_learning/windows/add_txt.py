import logging
from datetime import datetime

from vocabulary import Vocabulary
from text import Text
from config import *

def add_txt(vocabulary: Vocabulary) -> None:
    while True:
        Text.clear()
        logging.info("Add words by txt")

        patern = Text.menu((
            'Word-Translation[New Line]Word-Translation',
            'Word, Word...[New Line]Translation, Translation...'
        ), 'Pick a Pattern -> ')
        if patern == -1:
            return
        while True:
            Text.clear()
            Text.print('Create File With Words in Desktop',delay=0, color='green')
            Text.print('Nothing to Exit',delay=0, color='green')
            file_name = Text.input('Write file name (name.txt) -> ', color='green')
            if file_name == '':
                break
            
            words = []
            trans = []
            path = f'{DESKTOP_PATH}\\{file_name}'
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    match patern:
                        case 1:
                            for line in file:
                                line = line.split('-')
                                words.append(line[0])
                                trans.append(line[1])
                        case 2:
                            for index, line in enumerate(file):
                                if index == 0:
                                    words = (line.split(','))
                                else:
                                    trans = (line.split(','))
            except FileNotFoundError:
                Text.input('Cant Read File!', color='red')    
                continue    
            
            if len(words) != len(trans):
                Text.print("Amount of Words Is Not the Same! Please Check Words Before!", color='red', delay=0)

            words, trans = vocabulary.process_data(words, trans)
            while True:
                Text.clear()
                Text.print(vocabulary.draw_date(words, trans), delay=0)
                option = Text.menu((
                    'Yes',
                    'No'
                ), phrase='Correct? -> ')
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
                            logging.info(f'{index} is not number')
                            Text.input('Write Number!', color='red')
                            continue
                        if index >= len(words):
                            logging.info(f'{index} is out of bounds')
                            Text.input('Out of Bounds!', color='red')
                            continue
                                
                        words.pop(index)
                        trans.pop(index)