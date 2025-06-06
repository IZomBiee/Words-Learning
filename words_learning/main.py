import page

from vocabulary import Dictionary, Statistic

try:
    Statistic()
    Dictionary().load_units()
    page.start_page_loop()
except KeyboardInterrupt:...
finally:
    print("Goodbye!")



