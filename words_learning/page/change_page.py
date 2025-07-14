import console
from vocabulary import Dictionary, DictionaryUnit

def change_page_loop():
    if len(Dictionary()) == 0:
        console.custom_input("No words in vocabulary! ", "red", False)
        return
    
    while True:
        try:
            console.clear()

            match console.menu(['Search in list', 'Search by word', 'Search by translation'], "How to find word? "):
                case 1:
                    choosen_word_unit = console.choose_word()
                case 2:
                    choosen_word_unit = Dictionary().has_words(console.custom_input("Write a word -> "))
                    if choosen_word_unit is None:
                        console.custom_input("Can't find word! ", 'red')
                        continue
                case 3:
                    choosen_word_unit = Dictionary().has_translations(console.custom_input("Write a translation -> "))
                    if choosen_word_unit is None:
                        console.custom_input("Can't find translation! ", 'red')
                        continue
            
            while True:
                try:
                    new_word_unit = DictionaryUnit()
                    console.colored_print(choosen_word_unit.to_string())
                    match console.menu(['Change word', 'Change translation', 'Both'], 'What to do? -> '):
                        case 1:
                            new_words = console.input_words()
                            new_word_unit.add_words(*new_words)
                            new_word_unit.add_translations(*choosen_word_unit.get_translations())
                        case 2:
                            new_translations = console.input_translations()
                            new_word_unit.add_words(*choosen_word_unit.get_words())
                            new_word_unit.add_translations(*new_translations)
                        case _:
                            new_word_unit = console.input_word_unit()
                    
                    new_word_unit.rating = choosen_word_unit.get_rating()
                    new_word_unit.add_rating(-2)

                    print(new_word_unit.to_string())
                    if console.custom_input_bool("Is it correct? "):
                        Dictionary().delete(choosen_word_unit)
                        Dictionary().add_unit(new_word_unit)
                        break  

                except KeyboardInterrupt:
                    break

        except KeyboardInterrupt:
            break