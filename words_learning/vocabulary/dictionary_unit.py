import difflib
import json
import utils
from .statistic import Statistic

class DictionaryUnit:
    def __init__(self):
        self.words = set()
        self.translations = set()
        self.fail_count = 0
        self.success_count = 0
        self.rating = 0
        self.create_time = utils.get_current_time()
        self.rating_chanse_dict = {
            0:100,
            1:80,
            2:50,
            3:30,
            4:10,
            5:1
        }

    def merge(self, dict_unit: 'DictionaryUnit') -> 'DictionaryUnit':
        self.add_words(*dict_unit.get_words())
        self.add_translations(*dict_unit.get_translations())
        self.add_rating(-2)
        self.fail_count += dict_unit.get_fail_count()
        self.success_count += dict_unit.get_success_count()
        self.change_create_time(utils.get_current_time())
        return self

    def add_words(self, *new_words:str) -> 'DictionaryUnit':
        for new_word in new_words:
            new_word = self.process_string(new_word)
            self.words.add(new_word)
        return self
    
    def add_translations(self, *new_translations:str) -> 'DictionaryUnit':
        for new_translation in new_translations:
            new_translation = self.process_string(new_translation)
            self.translations.add(new_translation)
        return self
    
    def change_create_time(self, time:str) -> None:
        self.create_time = time

    def on_fail(self) -> None:
        self.fail_count += 1
        Statistic().fail += 1
        self.add_rating(-2)

    def on_success(self) -> None:
        self.success_count += 1
        Statistic().success += 1
        self.add_rating(1) 
    
    def add_rating(self, a:int) -> int:
        self.rating += a
        if self.rating > 5:
            self.rating = 5
        elif self.rating < 0: 
            self.rating = 0
        return self.rating
        
    def load_from_json_string(self, json_string:str) -> 'DictionaryUnit':
        return self.load_from_dict(json.loads(json_string))

    def load_from_dict(self, data:dict) -> 'DictionaryUnit':
        self.words = set(data['words'])
        self.translations = set(data['translations'])
        self.fail_count = data['fail_count']
        self.success_count = data['success_count']
        self.rating = data['rating']
        self.create_time = data['create_time']
        return self

    def save_to_json_string(self) -> str:
        return json.dumps(self.save_to_dict(), ensure_ascii=False)

    def save_to_dict(self) -> dict:
        return {
            'words': list(self.words),
            'translations': list(self.translations),
            'fail_count': self.fail_count,
            'success_count' : self.success_count,
            'rating': self.rating,
            'create_time': self.create_time
        }

    def get_words(self) -> set[str]:
        return self.words
    
    def get_translations(self) -> set[str]:
        return self.translations
    
    def get_rating(self) -> int:
        return self.rating
    
    def get_chanse(self) -> int:
        return self.rating_chanse_dict[self.get_rating()]

    def get_rating_chanse(self):
        return self.rating_chanse_dict(self.get_rating())
    
    def get_fail_count(self) -> int:
        return self.fail_count

    def get_success_count(self) -> int:
        return self.success_count
    
    @staticmethod
    def process_string(string:str) -> str:
        return string.strip().capitalize()

    @staticmethod
    def compare(correct_word:str, check_word:str) -> list[dict]:
        result = []

        for correct_word_index, correct_word in enumerate(correct_word.split(' ')):
            for correct_char_index, correct_char in enumerate(correct_word):
                try:
                    check_char = check_word.split(' ')[correct_word_index][correct_char_index]
                except IndexError:
                    check_char = ' '

                if correct_char == check_char:
                    result.append({'char':correct_char, 'color':'green'})
                else:
                    result.append({'char':correct_char, 'color':'red'})
            result.append({'char':' ', 'color':'white'})
        return result

    @staticmethod
    def accuracy_precent(correct_word:str, check_word:str) -> float:
        return difflib.SequenceMatcher(None, correct_word, check_word).ratio() * 100

    def to_string(self) -> str:
        return f"{', '.join(self.words)} - {', '.join(self.translations)}"
    
    def __repr__(self):
        return f"DictionaryUnit({self.words=}; {self.translations=}; {self.fail_count=}; {self.success_count=}; {self.rating=})"