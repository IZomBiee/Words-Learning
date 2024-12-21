import json
import os

from json_reader import JSONReader

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class SettingsLoader(JSONReader):
    def __init__(self, settings_file_path:str):
        super().__init__(settings_file_path)
        self.read()
    
    def read(self) -> None:
        try:
            with open(self.path, encoding='utf-8', mode='r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            try:
                os.mkdir('files')
            except FileExistsError:
                pass
            self.data = {
                'word_in_learning_chance':50,
                'learning_chance_table':{'0': 100., '1':70., '2':50., '3':30., '4':7., '5':0.3},
                'contest_mode_chance':1,
                "word_almost_correct_threshold": 70,
                "translation_almost_correct_threshold": 60
            }
            self.write()