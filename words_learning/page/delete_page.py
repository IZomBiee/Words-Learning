import console
import vocabulary

def delete_page_loop():
    if len(vocabulary.Dictionary()) == 0:
        console.custom_input("No words in vocabulary! ", "red", False)
        return
    
    while True:
        try:
            console.clear()

            match console.menu(['Search in list', 'Search by word', 'Search by translation'], "How to find word? "):
                case 1:
                    choosen_word_unit = console.choose_word()
                case 2:
                    choosen_word_unit = vocabulary.Dictionary().has_words(console.custom_input("Write a word -> "))
                    if choosen_word_unit is None:
                        console.custom_input("Can't find word! ", 'red')
                        continue
                case 3:
                    choosen_word_unit = vocabulary.Dictionary().has_translations(console.custom_input("Write a translation -> "))
                    if choosen_word_unit is None:
                        console.custom_input("Can't find translation! ", 'red')
                        continue
                    
            console.colored_print(choosen_word_unit.to_string())
            if console.custom_input_bool('Delete? '):
                vocabulary.Dictionary().delete(choosen_word_unit)
        except KeyboardInterrupt:
            break