import logging
import time
import random

from text import Text
from config import *
from vocabulary import Vocabulary
from matplotlib import pyplot as plt

class Windows:
    def __init__(self, vocabulary:Vocabulary) -> None:
        self.vocabulary = vocabulary

    @staticmethod
    def language_choice() -> Vocabulary:
        while True:
            logging.info('Language choice start')
            Text.clear()
            try:
                languages = os.listdir(LANGUAGES_PATH)
            except FileNotFoundError:
                logging.warning("No language folder! Create new...")
                os.mkdir(LANGUAGES_PATH)
                logging.info("Folder succesful create!")
                languages = os.listdir(LANGUAGES_PATH)
            option = Text.menu(['Add New Language', 'Delete Language']+languages)
            match option:
                case -1:
                    raise KeyboardInterrupt
                
                case 1:
                    logging.info('Create new language')
                    Text.print('Nothing To Exit',delay=0, color='yellow')
                    language_name = Text.input('Write Language Name -> ', color='green')
                    if '/' in language_name or '\\' in language_name:
                        logging.info(f"Language name contain / or \\ {language_name}")
                        Text.input("Name can't contain / or \\ ", color='red')
                        continue
                    elif language_name == '':
                        continue

                    os.mkdir(f'{LANGUAGES_PATH}\\{language_name}')
                    logging.info("New language folder created")
                case 2:
                    logging.info('Delete language')
                    options = Text.multimenu(languages)
                    for option in options:
                        os.rmdir(f'{LANGUAGES_PATH}\\{languages[option-1]}')
                        logging.info(f'Dir {LANGUAGES_PATH}\\{languages[option-1]} removed!')
                case _:
                    data = Vocabulary(languages[option-3])
                    return data
        
    def list(self) -> None:
        logging.info("Show words")
        Text.print(self.vocabulary.draw(keys=('word', 'tran')), delay=0)
        Text.input('Continue? -> ', color='green')
        Text.clear()

    def delete(self) -> None:
        while True:
            logging.info("Delete words")
            Text.clear()
            Text.print(self.vocabulary.draw(keys=['word', 'tran']), delay=0)
            try:
                self.vocabulary.delete(Text.input_int('Write Nr. of word to delete -> ', range=[0, len(self.vocabulary)]))
            except KeyboardInterrupt:
                return

    def add_txt(self) -> None:
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
                Text.print('Create File With Words in Desktop',delay=0, color='yellow')
                Text.print('Nothing to Exit',delay=0, color='yellow')
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

                words, trans = self.vocabulary.process_data(words, trans)
                while True:
                    Text.clear()
                    Text.print(self.vocabulary.draw_date(words, trans), delay=0)
                    option = Text.menu((
                        'Yes',
                        'No'
                    ), phrase='Correct? -> ')
                    if option == -1:break
                    elif option == 1:
                        self.vocabulary.append(words, trans)
                        return
                    elif option == 2:
                        while True:
                            Text.clear()
                            Text.print(self.vocabulary.draw_date(words, trans),delay=0)
                            try:
                                index = Text.input_int('Write Nr. of the Wrong Word -> ', color='green', range=[0, len(words)])
                            except KeyboardInterrupt:
                                break
                                    
                            words.pop(index)
                            trans.pop(index)

    def add(self) -> None:
        while True:
            Text.clear()
            logging.info("Add Words")

            Text.print("Write nothing to exit\nSplit words by ,", delay=0, color='yellow')
            words = Text.input('Write word -> ',
                                color='green').split(',')
            if words[0] == '':break
            trans = Text.input('Write translation -> ',
                                color='green').split(',')
            if trans[0] == '':break


            while True:
                Text.clear()
                Text.print(self.vocabulary.draw_date(words, trans),delay=0)


                option = Text.menu((
                    'Yes',
                    'No'
                ), phrase='Correct? -> ')
                Text.clear()
                if option == -1:break
                elif option == 1:
                    self.vocabulary.append(words, trans)
                    return
                elif option == 2:
                    while True:
                        Text.clear()
                        Text.print(self.vocabulary.draw_date(words, trans),delay=0)
                        try:
                            index = Text.input_int('Write Nr. of the Wrong Word -> ', color='green', range=[0, len(words)])
                        except KeyboardInterrupt:
                            break
                        else:            
                            words.pop(index)
                            trans.pop(index)
    
    def change(self) -> None:
         while True:
            logging.info("Change words")

            try:
                while True:
                    Text.clear()
                    Text.print(self.vocabulary.draw(keys=['word', 'tran']), delay=0)
                    index = Text.input_int('Write Nr. of word to change -> ', range=[0, len(self.vocabulary)])
                    Text.clear()
                    Text.print(f"| {index} | {self.vocabulary[index]['word']} | {self.vocabulary[index]['tran']} |\n", delay=0)

                    Text.print('Nothing to exit', color='yellow', delay=0)
                    word = Text.input('Write new word -> ').title().strip()
                    if word == '':
                        raise KeyboardInterrupt
                    tran = Text.input('Write new translation -> ').title().strip()
                    if tran == '':
                        raise KeyboardInterrupt
                    
                    while True:
                        Text.clear()
                        Text.print(f"| {index} | {word} | {tran} |", delay=0)
                        option = Text.menu((
                            'Yes',
                            'Change word',
                            'Change translation'
                        ), 'Correct? -> ')
                        match option:
                            case -1:
                                raise KeyboardInterrupt
                            case 1:
                                self.vocabulary.change(index, word, tran)
                                break
                            case 2:
                                Text.print('Nothing to exit', color='yellow', delay=0)
                                word = Text.input('Write new word -> ').title().strip()
                                if word == '':
                                    raise KeyboardInterrupt
                            case 3:
                                Text.print('Nothing to exit', color='yellow', delay=0)
                                tran = Text.input('Write new translation -> ').title().strip()
                                if tran == '':
                                    raise KeyboardInterrupt 

            except KeyboardInterrupt:
                return

    def learn(self):
        sum_time_start = time.time()
        running = True
        if len(self.vocabulary) == 0:
            Text.input('No Words!',color='red')
            return
        while running:
            for index, data in enumerate(self.vocabulary[::-1]):
                if running == False:
                    break
                index = (len(self.vocabulary) - index)-1
                time_start = time.time()    
                try:
                    change = (data['fail'] / data['success']) * CHANCE_MULT
                    change += 0.001
                except ZeroDivisionError:
                    change = 1
                
                if random.random() < change:
                    Text.clear()
                    Text.print(f'Fail:{data['fail']} Success:{data['success']} Change:{round(change, 2)} Time:{round(time.time()-sum_time_start)}s Index:{index}\n', delay=0, color='green')
                    Text.print('1 -> Exit', color='yellow', delay=0)
                    Text.print(f"Translation -> ",delay=0, end='', color='green')
                    Text.print(data['tran'],delay=0)
                    option = Text.input('Write Word -> ', color='green')
                    if option == '1':
                        running = False
                        break
                    if option.title().strip() == data['word']:
                        Text.input('Success! ', color='green')
                        self.vocabulary[index]['success'] += 1
                        self.vocabulary.stats[-1]['success'] += 1
                    else:
                        Text.input(f'Not Correct! Correct is {data['word']} ', color='red')   
                        self.vocabulary[index]['fail'] += 1
                        self.vocabulary.stats[-1]['fail'] += 1
                        break
                    
                self.vocabulary.stats[-1]['time_in_learning'] += round(time.time()-time_start)
                
    def statistic(self):
        plt.title("All statistic of all time")
        plt.xlabel("Dates")
        plt.ylabel("Count")
        plt.plot([i['date'] for i in self.vocabulary.stats], [i['time_in_learning']//60 for i in self.vocabulary.stats], marker='.')
        plt.plot([i['date'] for i in self.vocabulary.stats], [i['word_added'] for i in self.vocabulary.stats], marker='.')
        plt.plot([i['date'] for i in self.vocabulary.stats], [i['word_deleted'] for i in self.vocabulary.stats], marker='.')
        plt.plot([i['date'] for i in self.vocabulary.stats], [i['load_times'] for i in self.vocabulary.stats], marker='.')
        plt.plot([i['date'] for i in self.vocabulary.stats], [i['fail'] for i in self.vocabulary.stats], marker='.')
        plt.plot([i['date'] for i in self.vocabulary.stats], [i['success'] for i in self.vocabulary.stats], marker='.')
        plt.legend(['Time in learning(M)', 'Words added', 'Words deleted', 'Load times', 'Fail count', 'Success count'])
        plt.show()