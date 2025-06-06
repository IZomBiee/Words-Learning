import console
import vocabulary
import random
import time

def learn_page_loop():
    if len(vocabulary.Dictionary()) == 0:
        console.custom_input("No words in vocabulary! ", "red", False)
        return
    
    learning_start_time = time.time()
    while True:
        try:
            cycle_start_time = time.time()
            dictionary_unit = vocabulary.Dictionary().get_random_word()
            is_translation = 0.3 < random.random()

            try:
                correct_precent = (dictionary_unit.get_success_count() / (dictionary_unit.get_fail_count() + dictionary_unit.get_success_count())) * 100
                correct_precent = round(correct_precent)
            except ZeroDivisionError:
                correct_precent = '~'
            
            printed_words = dictionary_unit.get_words().copy()
            printed_translations = dictionary_unit.get_translations().copy()
            if is_translation:
                correct_word = random.choice(tuple(printed_translations))
                printed_translations.remove(correct_word)

            else:
                correct_word = random.choice(tuple(printed_words))
                printed_words.remove(correct_word)
            
            word_correction = False
            while True:
                console.clear()
                console.colored_print(f"Fail:{dictionary_unit.get_fail_count()} Success:{dictionary_unit.get_success_count()} Rating:{dictionary_unit.get_rating()} \
Precent:{correct_precent}% Time:{round(time.time()-learning_start_time)}s \
Position:{vocabulary.Dictionary().get_units().index(dictionary_unit)+1}/{len(vocabulary.Dictionary().get_units())}\n", 'green')
                
                console.colored_print("Nothing to exit", 'yellow')
                if is_translation:
                    if len(printed_words) > 1:
                        console.colored_print("Words -> ", 'green', end='')
                    else: console.colored_print("Word -> ", 'green', end='')
                    console.colored_print(', '.join(printed_words))

                    if len(printed_translations) > 1:
                        console.colored_print("Translations -> ", 'green', end='')
                    else: console.colored_print("Translation -> ", 'green', end='')
                    if len(printed_translations):
                        console.colored_print(', '.join(printed_translations), end=', ')
                else:
                    if len(printed_translations) > 1:
                        console.colored_print("Translation -> ", 'green', end='')
                    else: console.colored_print("Translation -> ", 'green', end='')
                    console.colored_print(', '.join(printed_translations))

                    if len(printed_words) > 1:
                        console.colored_print("Words -> ", 'green', end='')
                    else: console.colored_print("Word -> ", 'green', end='')
                    if len(printed_words):
                        console.colored_print(', '.join(printed_words), end=', ')

                entered_word = dictionary_unit.process_string(console.custom_input(""))
                accuracy_precent = dictionary_unit.accuracy_precent(correct_word, entered_word)
                if accuracy_precent == 100:
                    if not word_correction: dictionary_unit.on_success()
                    console.custom_input("All Correct! ", 'green', False)
                    break
                elif accuracy_precent > 70:
                    if not word_correction: dictionary_unit.on_success()
                    [console.colored_print(i['char'], i['color'], '') for i in dictionary_unit.compare(correct_word, entered_word)]
                    console.custom_input("\nAlmost Correct! ", 'yellow', False)
                    if not word_correction: break
                else:
                    if not word_correction:dictionary_unit.on_fail()
                    [console.colored_print(i['char'], i['color'], '') for i in dictionary_unit.compare(correct_word, entered_word)]
                    console.custom_input("\nNot Correct! ", 'red', False)
                    word_correction = True

            vocabulary.Statistic().time_in_learning += time.time()-cycle_start_time
            vocabulary.Statistic().words_learned = len(tuple(filter(lambda dict_unit: dict_unit.get_rating()>=4,
                                                              vocabulary.Dictionary().get_units())))
            vocabulary.Dictionary().save_units()
            vocabulary.Statistic().write()
            
        except KeyboardInterrupt:
            break