from words_learning import utils
import json
import random

from .statistic import Statistic
from .dictionary_unit import DictionaryUnit

@utils.singleton
class Dictionary():
    def __init__(self) -> None:
        self.saving_path = "dictionary.json"
        self.units: list[DictionaryUnit] = []
    
    def get_units(self) -> list[DictionaryUnit]:
        return self.units

    def delete(self, unit:DictionaryUnit) -> DictionaryUnit:
        Statistic().words_deleted += 1
        deleted_unit = self.units.pop(self.units.index(unit))
        self.save_units()
        return deleted_unit

    def has_translations(self, *translations:str) -> DictionaryUnit | None:
        for translation in translations:
            translation = DictionaryUnit.process_string(translation)

            for unit in self.units:
                if translation in unit.get_translations():
                    return unit

        return None

    def has_words(self, *words:str) -> DictionaryUnit | None:
        for word in words:
            word = DictionaryUnit.process_string(word)
            for unit in self.units:
                if word in unit.get_words():
                    return unit

        return None

    def add_unit(self, unit: DictionaryUnit) -> DictionaryUnit:
        self.units.append(unit)
        Statistic().words_added += 1
        self.save_units()
        return unit
    
    def create_unit(self, words:tuple[str, ...], translations:tuple[str]) -> DictionaryUnit:
        return self.add_unit(DictionaryUnit().add_words(words).add_translations(translations))
    
    def save_units(self) -> None:
        with open(self.saving_path, 'w', encoding='utf-8') as file:
            json.dump(list(map(lambda unit: unit.save_to_dict(), self.units)), file,
                      ensure_ascii=False, indent=2)
    
    def get_random_word(self) -> DictionaryUnit:
        while True:
            dictionary_unit: DictionaryUnit = random.choice(self[::1])
            if dictionary_unit.get_chanse() > random.random()*100:
                return dictionary_unit
    
    def load_units(self) -> None:
        try:
            with open(self.saving_path, 'r', encoding='utf-8') as file:
                try:
                    self.units = [DictionaryUnit().load_from_dict(dict_unit) for dict_unit in json.load(file)]
                except json.decoder.JSONDecodeError:
                    pass
        except FileNotFoundError:
            pass

    def __repr__(self) -> str:
        return " ".join([str(i) for i in self.units])

    def __getitem__(self, index:int) -> DictionaryUnit:
        return self.units[index]
    
    def __len__(self) -> int:
        return len(self.units)