import logging

from text import Text
from vocabulary import Vocabulary

def list(vocabulary: Vocabulary) -> None:
    logging.info("Show words")
    Text.print(vocabulary.draw(keys=('word', 'tran')), delay=0)
    Text.input('Continue? -> ', color='green')
    Text.clear()
