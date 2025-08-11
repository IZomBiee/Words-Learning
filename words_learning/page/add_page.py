from ..vocabulary import DictionaryUnit, Dictionary
from .. import console

def add_page_loop():
    while True:
        try:
            console.clear()

            entered_word_unit = console.input_word_unit()

            merging_word_unit = Dictionary().has_words(*entered_word_unit.get_words())
            if merging_word_unit is not None:
                console.clear()
                try:
                    index = list(map(lambda translation: translation in entered_word_unit.get_translations(), merging_word_unit.get_translations())).index(True)
                    print(merging_word_unit.to_string())
                    console.colored_print("\nThe same word with same translations is already in vocabulary!", 'red')
                    if console.custom_input_bool("Would you like to reset it rating? "):
                        Dictionary()[index].add_rating(-5)

                except ValueError:
                    console.colored_print("There is the same word already!\n", 'red')
                    print(entered_word_unit.to_string(), end=' | ')
                    console.compare_word_units(merging_word_unit, DictionaryUnit().merge(entered_word_unit).merge(merging_word_unit))

                    if console.custom_input_bool("Would you like to merge? "):
                        merging_word_unit.merge(entered_word_unit)
            else:
                console.clear()
                merging_word_unit = Dictionary().has_translations(*entered_word_unit.get_translations())
                if merging_word_unit is not None:
                    console.colored_print("There is the same translation already!", 'red')
                    print(merging_word_unit.to_string(), end=' | ')
                    console.compare_word_units(entered_word_unit, DictionaryUnit().merge(entered_word_unit).merge(merging_word_unit))
                    print()
                    match console.menu(['Merge', 'Create seperate', 'Cancel']):
                        case 1:
                            merging_word_unit.merge(entered_word_unit)
                        case 2:
                            Dictionary().add_unit(entered_word_unit)
                        case _:
                            continue
                else:
                    console.clear()
                    print(entered_word_unit.to_string())
                    if console.custom_input_bool("Correct? "):
                        Dictionary().add_unit(entered_word_unit)

        except KeyboardInterrupt:break