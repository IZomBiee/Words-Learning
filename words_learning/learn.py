import time
import random
import logging

from vocabulary import Vocabulary
from statistic import Statistic
from text import Text

def learn(vocabulary:Vocabulary, statistic:Statistic, windows):
    global_learning_time = time.time()
    while True:
        mode = random.randint(0, 100)
        logging.info(f'Learn {mode=}')
        for index, data in enumerate(vocabulary[::-1]):
            index = len(vocabulary) - index - 1
            learning_time = time.time()
            try:
                success_procentage = (int(data['success'])/(int(data['success'])+int(data['fail'])))*100
            except ZeroDivisionError:
                success_procentage = 0
            if success_procentage*1.1 < random.randint(0, 100) or 1 == random.randint(0, 1000):
                logging.debug(f'Word is {data['word']} - {data['translation']}')
                Text.clear()
                Text.print(f'Fail:{data['fail']} Success:{data['success']} Correct:{round(success_procentage)}% Time:{round(time.time()-global_learning_time)}s\
 Position:{index+1}\n', color='green')
                Text.print('1 - Exit', color='yellow')
                Text.print('2 - Delete word', color='yellow')
                Text.print('3 - Change word', color='yellow')
                
                if mode > 90:
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
                        if mode < 80:
                            correct = Vocabulary.check_word(data['word'], word)
                        else:
                            correct = Vocabulary.check_word(data['translation'], word)
                            correct['correct'] += 20
                        logging.debug(f'Word correct_procentage is {correct['correct']}')
                        print()
                        if correct['correct'] >= 100:
                            statistic.add('success', 1)
                            vocabulary.add_statistic(index, 'success', 1)
                            Text.print('Correct! ', color='green')
                        elif correct['correct'] > 80:
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
                            Text.input('', color='green')
                            break
                        Text.input('', color='green')
                            
                statistic.add('time_in_learning', int(time.time()-learning_time))
            
               
