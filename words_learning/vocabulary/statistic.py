import csv
import os
from words_learning import utils

@utils.singleton
class Statistic:
    def __init__(self):
        self.saving_path = "statistic.csv"
        self.data: list[dict] = []
        self.read()
        if len(self.data) == 0 or self[-1]['date'] != utils.get_current_date():
            if not len(self.data):
                words_learned = 0
            else: words_learned = self.data[-1]['words_learned']
            self.data.append({
                'date':utils.get_current_date(),
                'fail':0,
                'success':0,
                'load_times':0,
                'time_in_learning':0,
                'words_learned': words_learned,
                'words_added':0,
                'words_deleted':0,
                              })
        self.load_times += 1
        
    @property
    def date(self) -> str:
        return self[-1]['date']
    
    @date.setter
    def date(self, value: str):
        self[-1]['date'] = value
        self.write()
    
    @property
    def fail(self) -> int:
        return int(self[-1]['fail'])
    
    @fail.setter
    def fail(self, value: int):
        self[-1]['fail'] = str(value)
        self.write()
    
    @property
    def success(self) -> int:
        return int(self[-1]['success'])
    
    @success.setter
    def success(self, value: int):
        self[-1]['success'] = str(value)
        self.write()
    
    @property
    def load_times(self) -> int:
        return int(self[-1]['load_times'])
    
    @load_times.setter
    def load_times(self, value: int):
        self[-1]['load_times'] = str(value)
        self.write()
    
    @property
    def time_in_learning(self) -> int:
        return float(self[-1]['time_in_learning'])
    
    @time_in_learning.setter
    def time_in_learning(self, value: int):
        self[-1]['time_in_learning'] = str(value)
        self.write()
    
    @property
    def words_learned(self) -> int:
        return int(self[-1]['words_learned'])
    
    @words_learned.setter
    def words_learned(self, value: int):
        self[-1]['words_learned'] = str(value)
        self.write()
    
    @property
    def words_added(self) -> int:
        return int(self[-1]['words_added'])
    
    @words_added.setter
    def words_added(self, value: int):
        self[-1]['words_added'] = str(value)
        self.write()
    
    @property
    def words_deleted(self) -> int:
        return int(self[-1]['words_deleted'])
    
    @words_deleted.setter
    def words_deleted(self, value: int):
        self[-1]['words_deleted'] = str(value)
        self.write()

    def read(self):
        try:
            with open(self.saving_path, encoding='utf-8', mode='r') as file:
                reader = csv.DictReader(file, lineterminator='\n', delimiter=',')
                self.data = []
                for row in reader:
                    self.data.append(row)
        except FileNotFoundError:
            try:
                os.mkdir('files')
            except FileExistsError:
                pass

    def write(self):
        with open(self.saving_path, encoding='utf-8', mode='w') as file:
            writer = csv.DictWriter(file, lineterminator='\n', delimiter=',', fieldnames=self[-1].keys())
            writer.writeheader()
            writer.writerows(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __len__(self):
        return len(self.data)