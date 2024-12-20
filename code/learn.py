import time
import random
import logging
import os
import difflib

from vocabulary import Vocabulary
from statistic import Statistic
from text import Text
from dotenv import load_dotenv
load_dotenv()

rating_chance = {
    '0': 100., '1':70., '2':50., '3':30., '4':7., '5':0.3
}

def learn(vocabulary:Vocabulary, statistic:Statistic, windows):
    global_learning_time = time.time()
    if len(vocabulary) < 1:
        return Text.input('No words in vocabulary!', color='red')
    
    while True:
        word_learning_mode = 1 if int(os.getenv('word_mode_chance')) > random.randint(0, 100) else 0
        contest_mode = 1 if int(os.getenv('contest_mode_chance')) > random.uniform(0, 100) \
        and min(map(lambda x: int(x['rating']), vocabulary)) >= 3 else 0
        correct_words = 0
        uncorrect_words = 0

        cycle_learning_time = time.time()
        for index, data in enumerate(vocabulary[::-1]):
            word_learning_time = time.time()
            index = len(vocabulary) - index - 1

            if int(data['rating']) < 0: data['rating'] = '0'
            elif int(data['rating']) > 5: data['rating'] = '5'
            word_chance = rating_chance[data['rating']]

            if word_chance < random.uniform(0, 100) and not contest_mode:
                continue
            synonyms = []
            for word in vocabulary[::-1]:
                if word is data:pass 
                elif word_learning_mode:
                    if word['translation'] == data['translation']:
                        synonyms.append(word['word'])
                else: 
                    if word['word'] == data['word']:
                        synonyms.append(word['translation'])
            try:
                correct_ansawer_percents = (int(data['success'])/(int(data['success'])+int(data['fail'])))*100
            except ZeroDivisionError: correct_ansawer_percents = 100

            Text.clear()
            logging.info(f'Learn')
            if contest_mode:Text.print('Contest!', color='yellow')
            if int(data['fail'])+int(data['success']) <= 0:Text.print('New word!', color='yellow')
            Text.print(f"Fail:{data['fail']} Success:{data['success']} Rating:{data['rating']}/5 \
Correct:{round(correct_ansawer_percents)}% Time:{round(time.time()-global_learning_time)}s Position:{index+1}\n", color='green')
                
            Text.print('Nothing to exit', color='yellow')
            if len(synonyms):
                Text.print(f"Don't write {', '.join(synonyms)}!", color='red')
            if word_learning_mode:
                Text.print(f"Translation       -> ", end='', color='green')
                Text.print(f"{data['translation']} ", end='')
                if data['description'] != "":
                    Text.print(f"({data['description']})")
                else:print()
                user_word = Vocabulary.proccess_word(Text.input('Write Translation -> ', color='green'))
            else:
                Text.print(f"Word              -> ", end='', color='green')
                Text.print(f"{data['word']} ", end='')
                if data['description'] != "":
                    Text.print(f"({data['description']})")
                else:print()
                user_word = Vocabulary.proccess_word(Text.input('Write Translation -> ', color='green'))
            if user_word == '':raise KeyboardInterrupt

            if word_learning_mode:
                checked_word = Vocabulary.check_word(data['word'], user_word)
            else:
                checked_word = Vocabulary.check_word(data['translation'], user_word)

            print()
            if ((checked_word['correct'] < int(os.getenv('word_almost_correct_threshold')) and word_learning_mode) or
            (checked_word['correct'] < int(os.getenv('translation_almost_correct_threshold')) and not word_learning_mode)):
                statistic.add('fail', 1)
                vocabulary.add_statistic(index, 'fail', 1)
                vocabulary.add_statistic(index, 'rating', -1)
                uncorrect_words += 1
                Text.print('Not correct!', color='red')
                Text.print('Correct is ', color='green', end='')
                for char in checked_word['word']:
                    Text.print(char['char'], color=char['color'], end='')
            else:
                if checked_word['correct'] == 100:
                    statistic.add('success', 1)
                    vocabulary.add_statistic(index, 'success', 1)
                    vocabulary.add_statistic(index, 'rating', 1)
                    correct_words += 1
                    Text.print('Correct! ', color='green', end='')
                else:
                    Text.print('Almost correct!', color='yellow')
                    Text.print('Correct is ', color='green', end='')
                    for char in checked_word['word']:
                        Text.print(char['char'], color=char['color'], end='')
            try:
                print()
                option = Text.menu(('Change',
                                    'Delete',
                                    'Exit'), exit_phrase='Nothing to next word')
            except KeyboardInterrupt:pass
            else:
                match option:
                    case 3:
                        logging.debug('Exit')
                        raise KeyboardInterrupt
                    case 2:
                        logging.debug('Delete')
                        try:
                            windows.delete(index)
                            break
                        except KeyboardInterrupt:break
                    case 1:
                        logging.debug('Change')
                        try:
                            windows.change(index)
                            break
                        except KeyboardInterrupt:break

            statistic.add('time_in_learning', int(time.time()-word_learning_time))
            if (((checked_word['correct'] <= int(os.getenv('word_almost_correct_threshold'))) and word_learning_mode) or (
                (checked_word['correct'] <= int(os.getenv('translation_almost_correct_threshold'))) and not word_learning_mode
                )) and not contest_mode:break
                
        Text.clear()
        if contest_mode:
            Text.print('Summery of contest:', color='green')
            Text.print(f'\tWords count:{correct_words+uncorrect_words}')
            Text.print(f'\tFail words:{uncorrect_words}')
            Text.print(f'\tCorrect words:{correct_words}')
            Text.print(f'\tCorrect procent:{round((correct_words/(uncorrect_words+correct_words))*100)}%')
            Text.print(f'\tTime: {round(time.time()-cycle_learning_time)}s')
            statistic.replace('words_learned', correct_words)
            Text.input("Continue? -> ")
