from .output import *

from vocabulary.dictionary_unit import DictionaryUnit
from vocabulary.dictionary import Dictionary

def display_word(word_unit: DictionaryUnit) -> None:
    colored_print(', '.join(word_unit.get_words()), end=" ")
    colored_print('- ', end='')
    colored_print(', '.join(word_unit.get_translations()), end=" ")
    colored_print()

def input_words() -> list[str]:
    colored_print('Nothing to exit', color='yellow')
    colored_print('Seperate by ,', color='yellow')
    words = custom_input('Write words -> ').split(',')
    return [DictionaryUnit.process_string(word) for word in words]

def input_translations() -> list[str]:
    colored_print('Nothing to exit', color='yellow')
    colored_print('Seperate by ,', color='yellow')
    translations = custom_input('Write translations -> ').split(',')
    return [DictionaryUnit.process_string(translation) for translation in translations]

def input_word_unit() -> DictionaryUnit:
    words = input_words()
    translations = input_translations()
    return DictionaryUnit().add_words(*words).add_translations(*translations)

def compare_word_units(word_unit1: DictionaryUnit, word_unit2: DictionaryUnit, splitting: str = '\n↓↓↓\n') -> None:
    colored_print(', '.join(word_unit1.get_words()), 'white', ' - ')
    colored_print(', '.join(word_unit1.get_translations()), 'white', end='')
    colored_print(splitting, end='')
    colored_print(', '.join(word_unit2.get_words()), 'white', ' - ')
    colored_print(', '.join(word_unit2.get_translations()), 'white')


def choose_word() -> DictionaryUnit:
    return Dictionary()[menu([word_unit.to_string()
                 for word_unit in Dictionary()], phrase='Choose the word -> ')-1]

def menu(options:tuple[str, ...], phrase:str='Option -> ', exit_phrase:str='Nothing to exit', return_index=True) -> int:
    while True:
        for index, option in enumerate(options):
            colored_print(f'{index+1:^{len(str(len(options)))+1}}-> {option}')
        try:
            user_option = input_int(phrase, color='green', limits=(1, len(options)), exit_phrase=exit_phrase)
            if return_index:
                return user_option
            else: return options[index]
        except ValueError:
            custom_input('Write number!', color='red')
        finally:
            clear(len(options)+2)

def custom_input(text:str='', color:str='green', raise_interrupt = True): 
    colored_print(text, color=color, end='')
    entry = input('')
    if entry == '' and raise_interrupt:
        raise KeyboardInterrupt
    return entry

def input_int(text:str='', color:str='green', limits:list[int, int]=(0, -1), exit_phrase:str='Nothing to exit'):
    if limits[1] == -1:
        limits[1] = float('inf')
    while True:
        colored_print(exit_phrase, color='yellow')
        index = custom_input(text, color)
        if index == '':
            raise KeyboardInterrupt
        try:
            index = int(index)
        except ValueError:
            custom_input('Write Number!', color='red')
            clear(3)
            continue
        if index > limits[-1] or index < limits[0]:
            custom_input(f'Write number from {limits[0]} to {limits[1]}!', color='red')
            clear(3)
            continue
        else:
            return index

def custom_input_bool(text:str='', color:str='green'):
    while True:
        user_custom_input = custom_input(text + '(n/Y) -> ', color)
        if user_custom_input == 'Y':
            return True
        elif user_custom_input == 'n':
            return False
        else:
            colored_print('Write n or Y!', color='red')
