import time
import random
import logging
import os
import math

from vocabulary import Vocabulary
from statistic import Statistic
from text import Text
from dotenv import load_dotenv
load_dotenv()

def learn(vocabulary:Vocabulary, statistic:Statistic, windows):
    global_learning_time = time.time()
    if len(vocabulary) < 1:
        return Text.input('No words in vocabulary!', color='red')
    while True:
        mode = 1 if random.randint(0, 100) > int(os.getenv('translation_mode_change')) else 0

        logging.info(f'Learn {mode=}')
        for index, data in enumerate(vocabulary[::-1]):
            index = len(vocabulary) - index - 1
            learning_time = time.time()
            try:
                success_procentage = (int(data['success'])/(int(data['success'])+int(data['fail'])+1))*100
            except ZeroDivisionError:
                success_procentage = 0
            if success_procentage*float(os.getenv('learn_change_mult')) < random.randint(0, 100) or 1 == random.randint(0, int(os.getenv("random_word_change"))):
                logging.debug(f'Word is {data['word']} - {data['translation']}')
                Text.clear()
                Text.print(f'Fail:{data['fail']} Success:{data['success']} Correct:{round(success_procentage)}% Time:{round(time.time()-global_learning_time)}s\
 Position:{index+1}\n', color='green')
                Text.print('1 - Exit', color='yellow')
                Text.print('2 - Delete word', color='yellow')
                Text.print('3 - Change word', color='yellow')
                
                if mode:
                    Text.print(f"Word              -> ", end='', color='green')
                    Text.print(data['word'])
                    word = Vocabulary.proccess_word(Text.input('Write Translation -> ', color='green'))
                else:
                    Text.print(f"Translation -> ", end='', color='green')
                    Text.print(data['translation'])
                    word = Vocabulary.proccess_word(Text.input('Write Word  -> ', color='green'))

                match word:
                    case '1':
                        logging.debug('Exit')
                        raise KeyboardInterrupt
                    case '2':
                        logging.debug('Delete')
                        try:
                            windows.delete(index)
                            break
                        except KeyboardInterrupt:break
                    case '3':
                        logging.debug('Change')
                        try:
                            windows.change(index)
                            break
                        except KeyboardInterrupt:break
                    case _:
                        if mode:
                            correct = Vocabulary.check_word(data['translation'], word)
                        else:
                            correct = Vocabulary.check_word(data['word'], word)
                        logging.debug(f'Word correct procentage is {correct['correct']}')
                        print()
                        if correct['correct'] >= 100:
                            statistic.add('success', 1)
                            vocabulary.add_statistic(index, 'success', 1)
                            Text.print('Correct! ', color='green', end='')
                        elif correct['correct'] > int(os.getenv('almost_correct_threshold')):
                            statistic.add('success', 1)
                            vocabulary.add_statistic(index, 'success', 1)
                            Text.print('Almost correct!', color='yellow')
                            Text.print('Correct is ', color='green', end='')
                            for char in correct['word']:
                                Text.print(char['char'], color=char['color'], end='')
                        else:
                            statistic.add('fail', 1)
                            vocabulary.add_statistic(index, 'fail', 1)
                            Text.print('Not correct!', color='red')
                            Text.print('Correct is ', color='green', end='')
                            for char in correct['word']:
                                Text.print(char['char'], color=char['color'], end='')
                            
                        option = Text.input('\nOption -> ', color='green')
                        match option:
                            case '1':
                                logging.debug('Exit')
                                raise KeyboardInterrupt
                            case '2':
                                logging.debug('Delete')
                                try:
                                    windows.delete(index)
                                    break
                                except KeyboardInterrupt:break
                            case '3':
                                logging.debug('Change')
                                try:
                                    windows.change(index)
                                    break
                                except KeyboardInterrupt:break
                        if correct['correct'] <= int(os.getenv('almost_correct_threshold')):break
                            
                statistic.add('time_in_learning', int(time.time()-learning_time))
