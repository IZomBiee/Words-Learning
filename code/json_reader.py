import json
import os

class JSONReader:
    def __init__(self, path:str) -> None:
        self.path = path
        self.data = []
    
    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def read(self) -> None:
        try:
            with open(self.path, encoding='utf-8', mode='r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            try:
                os.mkdir('files')
            except FileExistsError:
                pass
            self.write()

    def write(self) -> None:
        with open(self.path, encoding='utf-8', mode='w') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)