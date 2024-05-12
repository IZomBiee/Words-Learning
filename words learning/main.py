import logging
import os

from vocabulary import Vocabulary
from statistic import Statistic
from windows import Windows
from text import Text

from dotenv import load_dotenv
load_dotenv()

if __name__ == '__main__':
    logging.basicConfig(filename="last.log", level='DEBUG', filemode='w', encoding='utf-8',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s: %(message)s')
    logging.info("Start program")

    statistic = Statistic('files/statistic.csv', ['date', 'fail', 'success', 'load_times', 'time_in_learning', 'words_learned', 'words_added', 'words_deleted'])
    vocabulary = Vocabulary(statistic, 'files/words.csv', ['word', 'translation', 'date', 'fail', 'success'])
    windows = Windows(vocabulary, statistic)
    
    try:
        windows.choice()
    except KeyboardInterrupt:
        logging.info('Goodbye!')
        Text.print('Goodbye!')