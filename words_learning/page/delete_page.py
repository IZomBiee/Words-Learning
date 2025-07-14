import console
from vocabulary import Dictionary, DictionaryUnit

def delete_page_loop():
    if len(Dictionary()) == 0:
        console.custom_input("No words in vocabulary! ", "red", False)
        return
    
    while True:
        try:
            console.clear()

            try:
                option = console.menu(['Search in list', 'Search by word', 'Search by translation'], "How to find word? ")
            except KeyboardInterrupt:
                break
            
            try:
                match option:
                    case 1:
                        choosen_word_unit = console.choose_word()
                    case 2:
                        while True:
                            choosen_word_unit = Dictionary().has_words(console.custom_input("Write a word -> "))
                            if choosen_word_unit is None:
                                console.custom_input("Can't find word! ", 'red', False)
                                console.clear(2)
                            else:
                                break
                    case 3:
                        while True:
                            choosen_word_unit = Dictionary().has_translations(console.custom_input("Write a translation -> "))
                            if choosen_word_unit is None:
                                console.custom_input("Can't find translation! ", 'red', False)
                                console.clear(2)
                            else:
                                break
                        
                console.colored_print(choosen_word_unit.to_string())
                if console.custom_input_bool('Delete this word? '):
                    Dictionary().delete(choosen_word_unit)
            except KeyboardInterrupt:continue

        except KeyboardInterrupt:
            break