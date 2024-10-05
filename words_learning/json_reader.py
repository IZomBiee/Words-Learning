import logging
import json
import os

class JSONReader:
    def __init__(self, path:str) -> None:
        logging.info(f'JSONReader init {path}')
        self.path = path
        self.data = []
    
    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def read(self):
        logging.debug(f'Read JSON {self.path}')
        try:
            with open(self.path, encoding='utf-8', mode='r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            logging.error(f"Can't read {self.path}. Creating new...")
            try:
                os.mkdir('files')
            except FileExistsError:
                self.write()

    def write(self):
        logging.debug(f'Write JSON {self.path}')
        with open(self.path, encoding='utf-8', mode='w') as file:
            json.dump(self.data, file, indent=4)