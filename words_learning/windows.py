import time
import random
import logging
import os

from vocabulary import Vocabulary
from statistic import Statistic
from text import Text

from learn import learn
class Windows:
    def __init__(self, vocabulary:Vocabulary, statistic:Statistic):
        self.vocabulary = vocabulary
        self.statistic = statistic
        Text.clear()
    
    def choice(self):
        while True:
            Text.clear()
            option = Text.menu([
                'Add words',
                'Add txt',
                'Delete words',
                'Change words',
                'Show statistics',
                'Learn'
            ])
            match option:
                case 1:
                    try:
                        while True:
                            self.add()
                    except KeyboardInterrupt:pass
                case 2:
                    try:
                        self.add_txt()
                    except KeyboardInterrupt:pass
                case 3:
                    try:
                        while True:
                            self.delete()
                    except KeyboardInterrupt:pass
                case 4:
                    try:
                        while True:
                            self.change()
                    except KeyboardInterrupt:pass
                case 5:
                    try:
                        self.vizualize()
                    except KeyboardInterrupt:pass
                case 6:
                    try:
                        self.learn()
                    except KeyboardInterrupt:pass

    def delete(self, index:int=None):
        logging.info(f'Delete word')
        Text.clear()
        if index == None:
            index = self.choice_word()

        Text.print(f'{self.vocabulary[index]['word']} | {self.vocabulary[index]['translation']}\n')
        option = Text.menu((
            'Yes',
            'No'
        ), phrase = 'Correct -> ')
        if option == 1:
            self.vocabulary.delete(index)

    def add_txt(self):
        logging.info(f'Add txt')
        Text.clear()
        words = []
        trans = []
        pattern = Text.menu([
            'Word - Translation [New line] Word - Translation'
        ], 'Pick a pattern -> ')
        Text.print('File need to be in desktop', color='yellow')
        file_name = Text.input('File name (words.txt)-> ').strip()
        try:
            with open(f'{os.path.join(os.path.expanduser('~'), 'Desktop')}\{file_name}', encoding='utf-8') as file:
                match pattern:
                    case 1:
                        for line in file:
                            line = line.split('-')
                            if len(line) >= 2:
                                words.append(Vocabulary.proccess_word(line[0]))
                                trans.append(Vocabulary.proccess_word(line[1]))
                            else:
                                return Text.input('Word dont have translation!', color='red')

        except FileNotFoundError:
            logging.error(f'File {file_name} not found!')
            Text.input(f'File {file_name} not found!', color='red')
            return

        Text.clear()   
        for word, tran in zip(words, trans):
            Text.print(f"{word:^{20}} - {tran:^{20}}")
        
        print('\n'*2)
        option = Text.menu((
            'Yes', 'No'
        ), phrase='Add? -> ')
        if option == 1:
            for word, tran in zip(words, trans):
                self.vocabulary.add(word, tran)

    def add(self):
        logging.info(f'Add word')
        Text.clear()
        Text.print('Nothing to add words', color='yellow')
        word = Vocabulary.proccess_word(Text.input('Write word        -> '))
        if word == '':raise KeyboardInterrupt
        translation = Vocabulary.proccess_word(Text.input('Write translation -> '))
        if translation == '':raise KeyboardInterrupt
        self.vocabulary.add(word, translation)

    
    def change(self, index:int=None):
        logging.info(f'Word change')
        Text.clear()
        if index == None:
            index = self.choice_word()
        Text.print(f'{self.vocabulary[index]['word']} - {self.vocabulary[index]['translation']}\n')
        Text.print(f'Nothing to exit', color='yellow')
        word = Vocabulary.proccess_word(Text.input('Write new word -> '))
        if word == '':raise KeyboardInterrupt
        translation = Vocabulary.proccess_word(Text.input('Write new translation -> '))
        if translation == '':raise KeyboardInterrupt
        Text.clear()
        Text.print(f'{self.vocabulary[index]['word']} - {self.vocabulary[index]['translation']} -> {word} - {translation}\n')
        option = Text.menu((
                    'Yes',
                    'No'
        ), phrase = 'Correct -> ')
        if option == 1:
            self.vocabulary.change(word, translation, index)

    def vizualize(self):
        self.statistic.vizualize()

    def learn(self):
        learn(self.vocabulary, self.statistic, self)

    def choice_word(self) -> int:
        return Text.menu([f"{i['word']:^{20}} - {i['translation']:^{20}}" for i in self.vocabulary[::1]])-1
