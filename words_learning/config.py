import os

# Logging
OUTPUT_LOGS = False
DEBUG_LEVEL = 'DEBUG'
FORMAT='%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s: %(message)s'

# Dirs
CURRENT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LANGUAGES_PATH = f'{CURRENT_DIR}\\languages'
DESKTOP_PATH = os.path.expanduser("~/Desktop")

# Learning
CHANCE_MULT = 0.7