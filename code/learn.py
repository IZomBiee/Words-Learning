import time
import random

from vocabulary import Vocabulary
from statistic import Statistic
from text import Text
from settings_loader import SettingsLoader

def learn(vocabulary:Vocabulary, statistic:Statistic):
    global_learning_time = time.time()
    if len(vocabulary) < 1:
        return Text.input('No words in vocabulary!', color='red')
    
    while True:
        contest_mode = 1 if SettingsLoader()['contest_mode_chance'] > random.uniform(0, 100) \
        and min(map(lambda x: int(x['rating']), vocabulary)) >= 3 else 0
        contest_correct_words = 0
        contest_uncorrect_words = 0
        avaible_indexes = list(range(0, len(vocabulary)))

        cycle_learning_time = time.time()
        for _ in range(0, len(vocabulary)):
            break_cycle = False
            word_learning_mode = 1 if SettingsLoader()['word_in_learning_chance'] > random.randint(0, 100) else 0
            index = random.choice(avaible_indexes)
            avaible_indexes.pop(avaible_indexes.index(index))
            data = vocabulary[index]
            word_learning_time = time.time()
            try:
                word_chance = SettingsLoader()['learning_chance_table'][str(data['rating'])]
            except KeyError:
                word_chance = 100 
            if word_chance < random.uniform(0, 100) and not contest_mode:
                continue

            try:
                correct_ansawer_percents = (int(data['success'])/(int(data['success'])+int(data['fail'])))*100
            except ZeroDivisionError: correct_ansawer_percents = 100

            while True:
                break_loop = False
                Text.clear()
                if contest_mode:Text.print('Contest!', color='yellow')
                if int(data['fail'])+int(data['success']) <= 0:Text.print('New word!', color='yellow')
                Text.print(f"Fail:{data['fail']} Success:{data['success']} Rating:{data['rating']}/5 \
Correct:{round(correct_ansawer_percents)}% Time:{round(time.time()-global_learning_time)}s Position:{index+1}\n", color='green')
                Text.print('Nothing to exit', color='yellow')
                if word_learning_mode:
                    Text.print(f"Translation       -> ", end='', color='green')
                    Text.print(f"{', '.join(data['translations'])}", end='')
                    print()
                    correct_words = data['words'].copy() 
                    other_words = ', '.join([
                        correct_words.pop(correct_words.index(random.choice(correct_words))) for _ in range(len(correct_words)-1)
                        ])
                    Text.print(f'Write Translation -> ', end='', color='green')
                    if other_words != '':
                        Text.print(f'{other_words}, ', end='')
                    user_word = Vocabulary.proccess_word(Text.input('', color='green'))
                    correct_word = correct_words[0]
                else:
                    Text.print(f"Word              -> ", end='', color='green')
                    Text.print(f"{', '.join(data['words'])}", end='')
                    print()
                    correct_words = data['translations'].copy() 
                    other_words = ', '.join([
                        correct_words.pop(correct_words.index(random.choice(correct_words))) for _ in range(len(correct_words)-1)
                        ])
                    Text.print(f'Write Word        -> ', end='', color='green')
                    if other_words != '':
                        Text.print(f'{other_words}, ', end='')
                    user_word = Vocabulary.proccess_word(Text.input('', color='green'))
                    correct_word = correct_words[0]

                print()
                checked_word = Vocabulary.check_word(correct_word, user_word)
                if ((checked_word['correct'] < SettingsLoader()['word_almost_correct_threshold']) and word_learning_mode) or \
                (checked_word['correct'] < SettingsLoader()['translation_almost_correct_threshold'] and not word_learning_mode):
                    statistic.add('fail', 1)
                    vocabulary.add_statistic(index, 'fail', 1)
                    vocabulary.add_statistic(index, 'rating', -2)
                    contest_uncorrect_words += 1
                    Text.print('Not correct!', color='red')
                    Text.print('Correct is ', color='green', end='')
                    for char in checked_word['word']:
                        Text.print(char['char'], color=char['color'], end='')
                    break_cycle = True
                else:
                    if checked_word['correct'] == 100:
                        statistic.add('success', 1)
                        vocabulary.add_statistic(index, 'success', 1)
                        vocabulary.add_statistic(index, 'rating', 1)
                        contest_correct_words += 1
                        Text.print('Correct! ', color='green', end='')
                        break_loop = True
                    else:
                        statistic.add('success', 1)
                        vocabulary.add_statistic(index, 'success', 1)
                        vocabulary.add_statistic(index, 'rating', 1)
                        Text.print('Almost correct!', color='yellow')
                        Text.print('Correct is ', color='green', end='')
                        for char in checked_word['word']:
                            Text.print(char['char'], color=char['color'], end='')
                        break_loop = True
                        
                input()
        
                if int(data['rating']) < 0: data['rating'] = 0
                elif int(data['rating']) > 5: data['rating'] = 5

                statistic.add('time_in_learning', int(time.time()-word_learning_time))
                if break_loop:
                    break
            if break_cycle:
                break
                
        Text.clear()
        if contest_mode:
            Text.print('Summery of contest:', color='green')
            Text.print(f'\tWords count:{contest_correct_words+contest_uncorrect_words}')
            Text.print(f'\tFail words:{contest_uncorrect_words}')
            Text.print(f'\tCorrect words:{contest_correct_words}')
            Text.print(f'\tCorrect procent:{round((contest_correct_words/(contest_uncorrect_words+contest_correct_words))*100)}%')
            Text.print(f'\tTime: {round(time.time()-cycle_learning_time)}s')
            statistic.replace('words_learned', contest_correct_words)
            Text.input("Continue? -> ")
