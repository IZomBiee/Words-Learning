import page

from vocabulary import Dictionary, Statistic

Statistic()
Dictionary().load_units()
try:
    page.start_page_loop()
except KeyboardInterrupt:
    Dictionary().save_units()
    Statistic().write()
    


