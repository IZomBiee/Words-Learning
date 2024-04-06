import sys
import logging
import os

from time import sleep
from termcolor import colored

class Text:
    def print(text:str='', color:str='white', delay:int=1, end:str='\n'):    
        for char in text:
            print(colored(char, color), end='', flush=True)
            if char != ' ':
                sleep(0.1 / len(text))   
        print(end=end)
        sleep(delay)

    def input(text:str='', color:str='green', end:str='\n'):  
        for char in text:
            print(colored(char, color), end='', flush=True)
            sleep(0.1 / len(text))  
        return input('')
    
    def input_int(text:str='', color:str='green', range:list[int]=(0, -1)):
        if range[1] == -1:
            range[1] = float('inf')
        while True:
            Text.print("Nothing to exit", color='yellow', delay=0)
            index = Text.input(text, color)
            if index == '':
                raise KeyboardInterrupt
            try:
                index = int(index)
            except ValueError:
                logging.info(f'{index} is not number')
                Text.input('Write Number!', color='red')
                Text.clear(3)
                continue
            if index > range[-1] or index < range[0]:
                logging.info(f'Number {index} out of range!')
                Text.input(f'Write number from {range[0]} to {range[1]}!', color='red')
                Text.clear(3)
                continue
            else:
                return index
                
    def clear(count:int=0):
        if count == 0:
            os.system('cls')
        else:
            for _ in range(count):
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")

    def menu(options:tuple[str], phrase:str='Option -> ') -> int:
        '''Return option number'''
        logging.info(f"Making menu {options}")
        while True:
            for index, option in enumerate(options):
                Text.print(f'{index+1} -> {option}', delay=0)
            try:
                Text.print("Nothing To Exit", color='yellow', delay=0)
                user_option = Text.input(phrase, color='green')
                if user_option == '':
                    Text.clear(len(options)+2)
                    return -1
                user_option = int(user_option)
                if user_option < 1 or user_option > len(options):
                    logging.warning(f'{user_option=} out of range')
                    Text.input('Not correct variant ', color='red')
                    continue
                logging.info(f"Return {user_option}")
                return user_option
            except ValueError:
                Text.input('Write number!', color='red')
                logging.warning(f'{user_option=} is not int')
            finally:
                Text.clear(len(options)+3)
    
    def multimenu(options:tuple[str], phrase:str='Option -> ') -> int:
        '''Return option number'''
        logging.info(f"Making multimenu {options=}")
        while True:
            for index, option in enumerate(options):
                Text.print(f'{index+1} -> {option}', delay=0)
           
            Text.print("Nothing To Exit", color='yellow', delay=0)
            Text.print("Separate by ,", color='yellow', delay=0)
            user_option = Text.input(phrase, color='green')
            if user_option == '':
                Text.clear(len(options)+3)
                return -1
            
            user_options = user_option.replace(' ', '').split(',')
            try:
                user_options = [int(i) for i in user_options]
            except ValueError:
                logging.warning(f'{user_option=} is not int')
                Text.input('Write number!', color='red')
                Text.clear(len(options)+4)
                continue

            for user_option in user_options:
                if user_option < 1 or user_option > len(options):
                    logging.warning(f'{user_option=} out of range')
                    Text.input('Not correct variant ', color='red')
                    Text.clear(len(options)+4)
                    continue
            
            logging.info(f"Return {user_options}")
            return user_options


if __name__ == '__main__':
    print(Text.multimenu(['a', 'b', 'c']))