
from abc import ABC, abstractmethod
from generators.typing_level import TypingLevel
from typing_errors import TypingErrors
import random

from generators.keyboard_lang import KeyboardLanguage


class GeneratorABC(ABC):

    @property
    @abstractmethod
    def display_name(self):
        pass

    keyboard_lang = KeyboardLanguage.ENGLISH

    _words = []

    _level_symbols = [
        set('asdfghjkl '),  # level 0
        set('asdfghjkl qwertyuiop'),  # level 1
        set('asdfghjkl qwertyuiop zxcvbnm'),  # level 2
        set('asdfghjkl qwertyuiop zxcvbnm ASDFGHJKL QWERTYUIOP ZXCVBNM .,'),  # level 3
        set('asdfghjkl qwertyuiop zxcvbnm ASDFGHJKL QWERTYUIOP ZXCVBNM 1234567890 .,'),  # level 4
        set('asdfghjkl qwertyuiop zxcvbnm ASDFGHJKL QWERTYUIOP ZXCVBNM 1234567890 `~!@#$%^&*()-_=+[]{}\\|;:",<.>/?' + "'")  # level 5
    ]

    def get_text(self, length: int, errors: TypingErrors, typing_level: int) -> str:
        text = ''
        while True:
            total_len = len(text)
            if total_len >= length:
                break

            max_word_len = length - total_len - 1

            word_type = random.random()
            error_words = errors.get_error_words()
            error_letters = errors.get_error_letters()

            if max_word_len == 0:
                word = self._get_random_word(words=self._words, max_length=1, typing_level=typing_level)
                text += word
                continue
            elif word_type < 0.1 and typing_level >= TypingLevel.NUMBERS_4.value:
                word = self._get_random_number(max_word_len)
            elif word_type < 0.5 and len(error_words) > 0:
                word = self._get_random_word(words=error_words, max_length=max_word_len, typing_level=typing_level)
                if not word:
                    continue
                errors.del_word(word)
            elif word_type < 0.75 and len(error_letters) > 0:
                rand_letter = random.choice(error_letters)
                word = self._get_random_word_with_letter(
                    words=self._words, max_length=max_word_len, letter=rand_letter, typing_level=typing_level
                )
                if not word:
                    continue
                errors.del_letter(rand_letter)
            else:
                word = self._get_random_word(words=self._words, max_length=max_word_len, typing_level=typing_level)

            text += ' ' + word
            text = text.lstrip()

        return text

    def _get_random_word(self, words: list[str], max_length: int, typing_level: int):
        level_words = self.__get_level_words(words, typing_level)
        right_words = list(filter(lambda w: len(w) <= max_length, level_words))
        if len(right_words) == 0:
            return ''
        return random.choice(list(right_words))

    def _get_random_word_with_letter(self, words: list[str], max_length: int, letter: str, typing_level: int):
        level_words = self.__get_level_words(words, typing_level)
        right_words = list(
            filter(
                lambda w: len(w) <= max_length and letter in w,
                level_words
            )
        )
        if len(right_words) == 0:
            return None
        return random.choice(right_words)

    def _get_random_number(self, max_length: int) -> str:
        if max_length > 5:
            max_length = 5
        max_length = random.randint(1, max_length)
        return str(random.randint(0, 10 ** max_length - 1))

    def __get_level_words(self, words: list[str], typing_level: int):
        return (
            word for word in words
            if set(word).issubset(self._level_symbols[typing_level])
        )
