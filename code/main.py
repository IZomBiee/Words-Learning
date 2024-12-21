from vocabulary import Vocabulary
from statistic import Statistic
from windows import Windows
from text import Text
from settings_loader import SettingsLoader
# import json

if __name__ == '__main__':
    settings = SettingsLoader('files/settings.json')
    statistic = Statistic('files/statistic.csv', ['date', 'fail', 'success', 'load_times', 'time_in_learning', 'words_learned', 'words_added', 'words_deleted'])
    vocabulary = Vocabulary(statistic, 'files/words.json')
    windows = Windows(vocabulary, statistic)
    
    try:
        # with open('files/words.csv', 'r', encoding='utf-8') as file:
        #     file.readline()
        #     while True:
        #         line = file.readline()
        #         if line == '':
        #             break
        #         data = line.replace('\n', '').split(',')
        #         elem = data
        #         vocabulary.add(elem[0], elem[1], elem[3], elem[4], elem[5])
            
        windows.choice()
    except KeyboardInterrupt:
        Text.print('Goodbye!')
        vocabulary.write()
        statistic.write()
        settings.write()