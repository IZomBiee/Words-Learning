import difflib

from datetime import datetime
from json_reader import JSONReader
from statistic import Statistic
from text import Text

class Vocabulary(JSONReader):
    def __init__(self, statistic:Statistic, path:str) -> None:
        super().__init__(path)
        self.statistic = statistic
        self.read()

    def add(self, word:str, translation:str, date:str=None,
            fail:int=0, success:int=0, rating:int=0) -> None:
        word = Vocabulary.proccess_word(word)
        translation = Vocabulary.proccess_word(translation)
        if date == None: date = str(datetime.now().date())
        for data in self.data:
            if any(map(lambda x: x==word,data['words'])):
                Vocabulary.display_word(data)
                Text.print("↓↓↓")
                data['translations'].append(translation)
                Vocabulary.display_word(data)
                if Text.menu(("Yes", "No"), phrase="Correct? -> ") == 2:
                    return data['translations'].pop(-1)
                data['rating'] = 0
                return self.statistic.add('words_added', 1)
                
            elif any(map(lambda x: x==translation,data['translations'])):
                Vocabulary.display_word(data)
                Text.print("↓↓↓")
                data['words'].append(word)
                Vocabulary.display_word(data)
                if Text.menu(("Yes", "No"), phrase="Correct? -> ") == 2:
                    return data['words'].pop(-1)
                return self.statistic.add('words_added', 1)
                
        self.data.append({
            'words':[word], 'translations':[translation],
            'date':date, 'fail':fail, 'success':success,
            'rating':rating
            })

    def delete(self, index:int):
        Vocabulary.display_word(self.data[index])
        if len(self.data[index]['translations'])+len(self.data[index]['words']) <= 2:
            self.data.pop(index)
            self.statistic.add('words_deleted', 1)
        elif Text.menu(('Words','Translations'), phrase="What need to delete? -> ") == 1:
            self.data[index]['words'].pop(Text.menu(self.data[index]['words'],
                                                    phrase='Choose the word to delete -> ')-1)
            self.statistic.add('words_deleted', 1)
        else:
            self.data[index]['translations'].pop(Text.menu(self.data[index]['translations'],
                                        phrase='Choose the translation to delete -> ')-1)
            self.statistic.add('words_deleted', 1)

    def change(self, word:str, translation:str, index:int) -> None:
        self.data[index]['word'] = word
        self.data[index]['translation'] = translation
        self.write()

    def add_statistic(self, index:int, key:str, count:int):
        self[index][key] = str(int(self[index][key]) + count)
        self.write()
    
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

    @staticmethod
    def display_word(data: dict):
        Text.print(', '.join(data['words']), end=" ")
        Text.print('= ', end='')
        Text.print(', '.join(data['translations']), end=" ")
        Text.print()
    
    def choice_word(self) -> int:
        return Text.menu([f"{', '.join(i['words']):^{20}} - {', '.join(i['translations']):^{20}}" for i in self[::1]], phrase='Choose the word -> ')-1