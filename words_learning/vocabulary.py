import json
import logging
import datetime

from config import *
from text import Text

class Vocabulary():
    def __init__(self, lang_folder_name:str) -> None:
        logging.info(f"Words init {lang_folder_name}")
        self.lang_folder_name = lang_folder_name
        self.lang_folder_path = f'{LANGUAGES_PATH}\\{self.lang_folder_name}'
        self.lang_folder_words = f'{self.lang_folder_path}\\words.json'
        self.lang_folder_stats = f'{self.lang_folder_path}\\stats.json'
        self.data = []
        self.stats = []
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __len__(self):
        return len(self.data)
    
    def load(self):
        logging.info(f'Try to load {self.lang_folder_words}')
        for i in range(2):
            try:
                with open(self.lang_folder_words, 'r', encoding='utf-8') as file:
                    self.data = json.load(file)
                logging.info('Words loading complite successfuly!')
                break
            except FileNotFoundError:
                logging.warning('File not found! Create new...')
                with open(self.lang_folder_words, 'w', encoding='utf-8') as file:
                    json.dump(self.data, file)

        logging.info(f'Try to load {self.lang_folder_stats}')
        for i in range(2):
            try:
                with open(self.lang_folder_stats, 'r') as file:
                    self.stats = json.load(file)
                logging.info('Stats loading complite successfuly!')
                break
            except FileNotFoundError:
                logging.warning('File not found! Create new...')
                with open(self.lang_folder_stats, 'w') as file:
                    json.dump(self.data, file)

        if len(self.stats) == 0 or self.stats[-1]['date'] != str(datetime.datetime.now().date()):
            self.stats.append({
                'date':str(datetime.datetime.now().date()),
                'fail':0,
                'success':0,
                'time_in_learning':0,
                'word_added':0,
                'word_deleted':0,
                'load_times':0
            })
        self.stats[-1]['load_times'] += 1

    def save(self):
        logging.info(f'Try to save {self.lang_folder_words}...')
        with open(self.lang_folder_words, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4)
        logging.info(f'Words successfuly saved!')
        logging.info(f'Try to save {self.lang_folder_stats}...')
        with open(self.lang_folder_stats, 'w', encoding='utf-8') as file:
            json.dump(self.stats, file, indent=4)

        logging.info(f'Stats successfuly saved!')

    def append(self, words:list[str], trans:list[str]) -> None:
        logging.info(f"Appending {words}")
        words, trans = self.process_data(words, trans)
        
        for word, tran in zip(words, trans):
            self.data.append({
                'word': word,
                'tran': tran,
                'time': str(datetime.datetime.now().date()),
                'fail': 0,
                'success': 0
            })
        self.stats[-1]['word_added'] += len(words)
        
    def delete(self, index):
        logging.info('Delete Word')
        self.stats[-1]['word_deleted'] += 1
        self.data.pop(index)

    def draw(self, indexs:tuple[int]=None, keys:tuple[str]=None):
        logging.info("Draw words")

        if indexs == None:
            indexs = range(len(self.data))
        if keys == None:
            keys = self.data[0].keys()

        sizes = [len(key) for key in keys]
        for i in indexs:
            for j, key in enumerate(keys):
                if sizes[j] < len(str(self.data[i][key])): sizes[j] = len(self.data[i][key])

        text = f'|{'Nr.':^{len(str(len(self.data)))}}|{'word':^{sizes[0]}}|{'tran':^{sizes[1]}}|\n'
        for i in indexs:
            text += f'|{i:^{3 if len(str(len(self.data))) < 3 else len(str(len(self.data)))}}|'
            for j, key in enumerate(keys):
                text += f'{self.data[i][key]:^{sizes[j]}}|'
            text += f'\n'
        return text
    
    @staticmethod
    def draw_date(words:list[str], trans:list[str]) -> str:
        logging.info("Draw words")

        sizes = [len(key) for key in ('word', 'tran')]
        sizes.insert(0, 3 if len(str(len(words))) < 3 else len(str(len(words))))
        for word, tran in zip(words, trans):
            if len(word) > sizes[1]: sizes[1] = len(word)
            if len(tran) > sizes[2]: sizes[2] = len(tran)


        text = f"|{'Nr.':^{sizes[0]}}|{'word':^{sizes[1]}}|{'tran':^{sizes[2]}}|\n"
        for index, (word, tran) in enumerate(zip(words, trans)):
            text += f'|{index:^{sizes[0]}}|{word:^{sizes[1]}}|{tran:^{sizes[2]}}|\n'
        return text

    @staticmethod
    def process_data(words:list[str], trans:list[str]) -> tuple[str, str]:
        processed_words = []
        processed_trans = []
        for word, tran in zip(words, trans):
            processed_words.append(word.replace('\n', '').strip().title())
            processed_trans.append(tran.replace('\n', '').strip().title())
        return (processed_words, processed_trans)
