import vocabulary
import console
import logging

def add_page_loop():
    while True:
        logging.info("Adding page cycle start")
        try:
            console.clear()

            entered_word_unit = console.input_word_unit()

            logging.debug("Finding word unit with same word")
            merging_word_unit = vocabulary.Dictionary().has_words(*entered_word_unit.get_words())
            if merging_word_unit is not None:
                logging.debug("Merging word")
                if all(map(lambda translation: translation in entered_word_unit.get_translations(),merging_word_unit.get_translations())):
                    console.custom_input("There is the same word already!", 'red', False)
                else:
                    console.compare_word_units(entered_word_unit, vocabulary.DictionaryUnit().merge(entered_word_unit).merge(merging_word_unit))

                    if console.custom_input_bool("Merge? "):
                        merging_word_unit.merge(entered_word_unit)
            else:
                logging.debug("Finding word unit with same translation")
                merging_word_unit = vocabulary.Dictionary().has_translations(*entered_word_unit.get_translations())
                if merging_word_unit is not None:
                    logging.debug("Merging translation")
                    console.compare_word_units(entered_word_unit, vocabulary.DictionaryUnit().merge(entered_word_unit).merge(merging_word_unit))

                    match console.menu(['Merge', 'Create seperate', 'Cancel']):
                        case 1:
                            merging_word_unit.merge(entered_word_unit)
                        case 2:
                            vocabulary.Dictionary().add_unit(entered_word_unit)
                        case _:
                            continue
                else:
                    vocabulary.Dictionary().add_unit(entered_word_unit)
        except KeyboardInterrupt:break