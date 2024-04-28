import sys
import logging
import os

from termcolor import colored

class Text:
    def print(text:str='', color:str='white', end:str='\n'):    
        print(colored(text, color), end=end, flush=True)

    def input(text:str='', color:str='green'): 
        Text.print(text, color=color, end='')
        entry = input('')
        return entry
    
    def input_int(text:str='', color:str='green', limits:list[int]=(0, -1)):
        if limits[1] == -1:
            limits[1] = float('inf')
        while True:
            Text.print('Nothing to exit', color='yellow')
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
            if index > limits[-1] or index < limits[0]:
                logging.info(f'Number {index} out of limits!')
                Text.input(f'Write number from {limits[0]} to {limits[1]}!', color='red')
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
        while True:
            for index, option in enumerate(options):
                Text.print(f'{index+1:^{len(str(len(options)))+1}}-> {option}')
            Text.print('')
            try:
                user_option = Text.input_int(phrase, color='green', limits=(1, len(options)))
                return user_option
            except ValueError:
                Text.input('Write number!', color='red')
            finally:
                Text.clear(len(options)+3)