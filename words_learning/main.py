from vocabulary import Vocabulary
from statistic import Statistic
from windows import Windows
from text import Text
from settings_loader import SettingsLoader

if __name__ == '__main__':
    settings = SettingsLoader('files/settings.json')
    statistic = Statistic('files/statistic.csv', ['date', 'fail', 'success', 'load_times', 'time_in_learning', 'words_learned', 'words_added', 'words_deleted'])
    vocabulary = Vocabulary(statistic, 'files/words.json')
    windows = Windows(vocabulary, statistic)
    
    try:
        windows.choice()
    except KeyboardInterrupt:
        Text.print('Goodbye!')
        vocabulary.write()
        statistic.write()
        settings.write()