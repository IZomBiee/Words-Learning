import logging

from datetime import datetime
from csv_reader import CSVReader
from matplotlib import pyplot as plt

class Statistic(CSVReader):
    def __init__(self, path: str, keys: list) -> None:
        super().__init__(path, keys)
        self.read()
        if len(self.data) == 0 or self.data[-1].get('date') != str(datetime.now().date()):
            self.data.append({
                'date':str(datetime.now().date()),
                'fail':0,
                'success':0,
                'load_times':0,
                'time_in_learning':0,
                'words_learned':0,
                'words_added':0,
                'words_deleted':0,
                              })
        self.add('load_times', 1)
    

    def __getitem__(self, index):
        return self.data[index]

    def vizualize(self):
        plt.title("All statistic of all time")
        plt.xlabel("Dates")
        plt.ylabel("Count")
        plt.plot([i['date'] for i in self], [int(i['time_in_learning'])/60 for i in self], marker='.')
        plt.plot([i['date'] for i in self], [int(i['words_added']) for i in self], marker='.')
        plt.plot([i['date'] for i in self], [int(i['words_learned']) for i in self], marker='.')
        plt.plot([i['date'] for i in self], [int(i['words_deleted']) for i in self], marker='.')
        plt.plot([i['date'] for i in self], [int(i['load_times']) for i in self], marker='.')
        plt.plot([i['date'] for i in self], [int(i['fail']) for i in self], marker='.')
        plt.plot([i['date'] for i in self], [int(i['success']) for i in self], marker='.')
        plt.legend(['Time in learning(M)', 'Words added', 'Words learned', 'Words deleted', 'Load times', 'Fail count', 'Success count'])
        plt.show()

    def add(self, key:str, count:int) -> None:
        logging.debug(f'Add {count} statistic to {key}')
        self[-1][key] = int(self[-1][key]) + count 
        self.write()

    def replace(self, key:str, count:int) -> None:
        logging.debug(f'Replace statistic in {key} with {count}')
        self[-1][key] = count 
        self.write()