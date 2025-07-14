import vocabulary
import page

import console

def start_page_loop():
    while True:
        console.clear()
        option = console.menu([
            'Add words',
            'Change words',
            'Delete words',
            'Show statistics',
            'Learn',
        ])

        match option:
            case 1:
                page.add_page_loop()
            case 2:
                page.change_page_loop()
            case 3:
                page.delete_page_loop()
            case 4:
                page.statistic_page_loop()
            case 5:
                page.learn_page_loop()
                