import logging
import os

from text import Text
from vocabulary import Vocabulary
from config import *

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
        option = Text.menu(['Add New Language']+languages)
        match option:
            case -1:
                exit()
            
            case 1:
                logging.info('Create new language')
                Text.print('Write Nothing To Exit',delay=0, color='green')
                language_name = Text.input('Write Language Name -> ', color='green')
                if '/' in language_name or '\\' in language_name:
                    logging.info(f"Language name contain / or \\ {language_name}")
                    Text.input("Name can't contain / or \\ ", color='red')
                    continue
                elif language_name == '':
                    continue

                os.mkdir(f'{LANGUAGES_PATH}\\{language_name}')
                logging.info("New language folder created")
            case _:
                data = Vocabulary(languages[option-2])
                return data
        
        
        