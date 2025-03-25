import sys
import os

from termcolor import colored

class Text:
    def print(text:str='', color:str='white', end:str='\n'):    
        print(colored(text, color), end=end, flush=True)

    def input(text:str='', color:str='green'): 
        Text.print(text, color=color, end='')
        entry = input('')
        if entry == '':
            raise KeyboardInterrupt
        return entry
    
    def input_int(text:str='', color:str='green', limits:list[int]=(0, -1), exit_phrase:str='Nothing to exit'):
        if limits[1] == -1:
            limits[1] = float('inf')
        while True:
            Text.print(exit_phrase, color='yellow')
            index = Text.input(text, color)
            if index == '':
                raise KeyboardInterrupt
            try:
                index = int(index)
            except ValueError:
                Text.input('Write Number!', color='red')
                Text.clear(3)
                continue
            if index > limits[-1] or index < limits[0]:
                Text.input(f'Write number from {limits[0]} to {limits[1]}!', color='red')
                Text.clear(3)
                continue
            else:
                return index
    
    def input_bool(text:str='', color:str='green'):
        while True:
            user_input = Text.input(text + '(n/Y) -> ', color)
            if user_input == 'Y':
                return True
            elif user_input == 'n':
                return False
            else:
                Text.print('Write n or Y!', color='red')

                
    def clear(count:int=0):
        if count == 0:
            os.system('cls')
        else:
            for _ in range(count):
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")

    def menu(options:tuple[str], phrase:str='Option -> ', exit_phrase:str='Nothing to exit', return_index=True) -> int:
        while True:
            for index, option in enumerate(options):
                Text.print(f'{index+1:^{len(str(len(options)))+1}}-> {option}')
            try:
                user_option = Text.input_int(phrase, color='green', limits=(1, len(options)), exit_phrase=exit_phrase)
                if return_index:
                    return user_option
                else: return options[index]
            except ValueError:
                Text.input('Write number!', color='red')
            finally:
                Text.clear(len(options)+3)