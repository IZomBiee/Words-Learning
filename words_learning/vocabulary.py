import logging
import difflib

from datetime import datetime
from csv_reader import CSVReader
from statistic import Statistic
from text import Text

class Vocabulary(CSVReader):
    def __init__(self, statistic:Statistic, path:str, keys:list) -> None:
        super().__init__(path, keys)
        self.statistic = statistic
        self.read()

    def add(self, word:str, translation:str) -> None:
        logging.info(f'Add word {word} - {translation}')
        
        for index, data in enumerate(self.data):
            if data['word'] == word:
                Text.input(f'The word {word} is already in the vocabulary! This word will be reseted!', color='red')
                self.data[index]['success'] = 0
                self.data[index]['fail'] = 0
                return
            elif data['translation'] == translation:
                Text.print(f'''\nThe word {word} with translation {translation} is already in the vocabulary!
Please, change translation! The word will not be added!\n''', color='red')
                Text.print(f'{word} - {translation}\n{self.data[index]['word']} - {self.data[index]['translation']}\n', color='white')
                Text.input(f'Continue? ', color='green')
                return
            
        self.data.append({
            'word':word, 'translation':translation,
            'date':str(datetime.now().date()), 'fail':0, 'success':0
            })
        self.statistic.add('words_added', 1)
        self.write()

    def delete(self, index:int) -> None:
        logging.info(f'Delete word {self[index]['word']} - {self[index]['translation']} on index {index}')
        self.data.pop(index)
        self.statistic.add('words_deleted', 1)
        self.write()
    
    def change(self, word:str, tranlation:str, index:int) -> None:
        logging.info(f'Change word {self.data[index]['word']} - {self.data[index]['translation']}\
                     to {word} - {tranlation}')
        self.data[index]['word'] = word
        self.data[index]['translation'] = tranlation
        self.write()
    
    def add_statistic(self, index:int, key:str, count:int):
        self[index][key] = int(self[index][key]) + count
        self.write()
        self.statistic.replace('words_learned', self.words_learned())

    def words_learned(self):
        elem = 0
        for data in self:
            try:
                if (int(data['success'])/(int(data['success'])+int(data['fail'])))*100 > 70:
                    elem += 1
            except ZeroDivisionError:pass
        return elem
      
    @staticmethod
    def proccess_word(word:str) -> str:
        return word.strip().capitalize()

    @staticmethod
    def check_word(correct_word:str, check_word:str) -> list[dict]:
        correct_procentage = difflib.SequenceMatcher(None, correct_word.replace(' ', ''), check_word.replace(' ', '')).ratio()*100
        result = {'correct':correct_procentage, 'word':[]}
        if correct_procentage == 100:
            result['word'] = [{'char':i, 'color':'green'} for i in correct_word]
        else:
            for correct_word_index, correct_word in enumerate(correct_word.split(' ')):
                for correct_char_index, correct_char in enumerate(correct_word):
                    try:
                        check_char = check_word.split(' ')[correct_word_index][correct_char_index]
                    except IndexError:
                        check_char = ' '

                    if correct_char == check_char:
                        result['word'].append({'char':correct_char, 'color':'green'})
                    else:
                        result['word'].append({'char':correct_char, 'color':'red'})
                result['word'].append({'char':' ', 'color':'white'})
        return result
