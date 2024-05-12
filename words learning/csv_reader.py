import logging
import csv
import datetime
import os

class CSVReader:
    def __init__(self, path:str, keys:list) -> None:
        logging.info(f'CSVReader init {path}, {keys}')
        self.path = path
        self.keys = keys
        self.data = []
    
    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)

    def get_modification_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(os.path.getmtime(self.path)).date()

    def read(self):
        logging.debug(f'Read CSV {self.path}')
        try:
            with open(self.path, encoding='utf-8', mode='r') as file:
                reader = csv.DictReader(file, lineterminator='\n', delimiter=',')
                self.data = []
                for row in reader:
                    self.data.append(row)
        except FileNotFoundError:
            logging.error(f"Can't read {self.path}. Creating new...")
            try:
                os.mkdir('files')
            except FileExistsError:
                self.write()

    def write(self):
        logging.debug(f'Write CSV {self.path}')
        with open(self.path, encoding='utf-8', mode='w') as file:
            writer = csv.DictWriter(file, lineterminator='\n', delimiter=',',
                                    fieldnames=self.keys)
            writer.writeheader()
            writer.writerows(self.data)

if __name__ == '__main__':
    a = CSVReader('files/words.csv', ['word', 'translation', 'date', 'fail', 'success'])
    a.read()
    print(a.get_modification_date())