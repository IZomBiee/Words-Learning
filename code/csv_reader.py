import csv
import datetime
import os

class CSVReader:
    def __init__(self, path:str, keys:list) -> None:
        self.path = path
        self.keys = keys
        self.data = []
    
    def __getitem__(self, index):
        try:
            return int(self.data[index])
        except ValueError:
            return self.data[index]

    def __len__(self):
        return len(self.data)

    def get_modification_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(os.path.getmtime(self.path)).date()

    def read(self) -> None:
        try:
            with open(self.path, encoding='utf-8', mode='r') as file:
                reader = csv.DictReader(file, lineterminator='\n', delimiter=',')
                self.data = []
                for row in reader:
                    self.data.append(row)
        except FileNotFoundError:
            try:
                os.mkdir('files')
            except FileExistsError:
                pass
            self.write()

    def write(self) -> None:
        with open(self.path, encoding='utf-8', mode='w') as file:
            writer = csv.DictWriter(file, lineterminator='\n', delimiter=',',
                                    fieldnames=self.keys)
            writer.writeheader()
            writer.writerows(self.data)