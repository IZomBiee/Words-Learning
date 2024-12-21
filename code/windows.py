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
                'Delete words',
                'Show statistics',
                'Learn',
            ])
            match option:
                case 1:
                    try:
                        while True:
                            self.add()
                    except KeyboardInterrupt:pass
                case 2:
                    try:
                        while True:
                            self.vocabulary.delete(self.vocabulary.choice_word())
                    except KeyboardInterrupt:pass
                case 3:
                    try:
                        self.vizualize()
                    except KeyboardInterrupt:pass
                case 4:
                    try:
                        self.learn()
                    except KeyboardInterrupt:pass

    def add(self):
        Text.clear()
        Text.print('Nothing to exit', color='yellow')
        word = Text.input('Write word        -> ')
        translations = Text.input('Write translations and separate using , -> ').split(',')
        for translation in translations:
            self.vocabulary.add(word, translation)

    def vizualize(self):
        self.statistic.vizualize()

    def learn(self):
        learn(self.vocabulary, self.statistic)

    def reset(self):
        Text.print('Are you sure to reset ALL words? Write Bye to delete', color='red')
        if Text.input('Word -> ') == 'Bye':
            for data in self.vocabulary:
                data['word'] = data['word']
                data['translation'] = data['translation']
                data['date'] = data['date']
                data['fail'] = 0
                data['success'] = 0
                data['rating'] = 0
            self.vocabulary.write()
        else: raise KeyboardInterrupt

    
