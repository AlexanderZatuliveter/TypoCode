from generators.generator_abc import GeneratorABC
from generators.keyboard_lang import KeyboardLanguage


class EnglishGenerator(GeneratorABC):

    @property
    def display_name(self): return "English"

    keyboard_lang = KeyboardLanguage.ENGLISH

    _words = []

    def __init__(self) -> None:
        with open("src/_content/dictionaries/english.txt", "r", encoding="utf-8") as f:
            self._words = f.read().split()
