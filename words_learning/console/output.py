import sys
import os

from termcolor import colored

def colored_print(text:str='', color:str='white', end:str='\n'):    
    print(colored(text, color), end=end, flush=True)
            
def clear(count:int=0):
    if count == 0:
        os.system('cls')
    else:
        for _ in range(count):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

