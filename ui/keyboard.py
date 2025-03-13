
import pygame
from pygame.event import Event
from pygame.key import ScancodeWrapper
from generators.keyboard_lang import KeyboardLanguage
from random import randint


class Keyboard:

    KEY_SIZE = 40.0
    KEY_SPACING = 6.0
    FONT_SIZE = 24.0
    LINE_KEYS_COUNT = 15
    SIZE = 0.7  # 70% of the screen

    def __init__(self, language: KeyboardLanguage):
        self.__x = 0
        self.__y = 0
        self.__keys = {}
        self.__highlighted_key = None
        self.__screen_height = -1
        self.__screen_width = -1
        self.__language = language
        self.__is_upper_case = False

        self.__eng_layout_uppercase = [
            [("~", 1), ("!", 1), ("@", 1), ("#", 1), ("$", 1), ("%", 1), ("^", 1),
             ("&", 1), ("*", 1), ("(", 1), (")", 1), ("_", 1), ("+", 1), ("<--", 2)],

            [("Tab", 1.5), ("Q", 1), ("W", 1), ("E", 1), ("R", 1), ("T", 1), ("Y", 1),
             ("U", 1), ("I", 1), ("O", 1), ("P", 1), ("{", 1), ("}", 1), ("|", 1.5)],

            [("CAPS", 1.8), ("A", 1), ("S", 1), ("D", 1), ("F", 1), ("G", 1),
             ("H", 1), ("J", 1), ("K", 1), ("L", 1), (":", 1), ('"', 1), ("ENTER", 2.35)],

            [("SHIFT", 2.30), ("Z", 1), ("X", 1), ("C", 1), ("V", 1), ("B", 1),
             ("N", 1), ("M", 1), ("<", 1), (">", 1), ("?", 1), ("Shift", 3.0)],

            [("CTRL", 1.25), ("Win", 1.25), ("ALT", 1.25), ("Space", 7.15),
             ("Alt", 1.25), ("Fn", 1.25), ("Menu", 1.25), ("Ctrl", 1.25)]
        ]

        self.__eng_layout_lowercase = [
            [("~", 1), ("1", 1), ("2", 1), ("3", 1), ("4", 1), ("5", 1), ("6", 1),
             ("7", 1), ("8", 1), ("9", 1), ("0", 1), ("-", 1), ("=", 1), ("<--", 2)],

            [("Tab", 1.5), ("q", 1), ("w", 1), ("e", 1), ("r", 1), ("t", 1), ("y", 1),
             ("u", 1), ("i", 1), ("o", 1), ("p", 1), ("[", 1), ("]", 1), ("\\", 1.5)],

            [("CAPS", 1.8), ("a", 1), ("s", 1), ("d", 1), ("f", 1), ("g", 1),
             ("h", 1), ("j", 1), ("k", 1), ("l", 1), (";", 1), ("'", 1), ("ENTER", 2.35)],

            [("SHIFT", 2.30), ("z", 1), ("x", 1), ("c", 1), ("v", 1), ("b", 1),
             ("n", 1), ("m", 1), (",", 1), (".", 1), ("/", 1), ("Shift", 3.0)],

            [("CTRL", 1.25), ("Win", 1.25), ("ALT", 1.25), ("Space", 7.15),
             ("Alt", 1.25), ("Fn", 1.25), ("Menu", 1.25), ("Ctrl", 1.25)]
        ]

        self.__rus_layout = [
            [("~", 1), ("1", 1), ("2", 1), ("3", 1), ("4", 1), ("5", 1), ("6", 1),
             ("7", 1), ("8", 1), ("9", 1), ("0", 1), ("-", 1), ("=", 1), ("<--", 2)],

            [("Tab", 1.5), ("Й", 1), ("Ц", 1), ("У", 1), ("К", 1), ("Е", 1), ("Н", 1),
             ("Г", 1), ("Ш", 1), ("Щ", 1), ("З", 1), ("Х", 1), ("Ъ", 1), ("\\", 1.5)],

            [("CAPS", 1.8), ("Ф", 1), ("Ы", 1), ("В", 1), ("А", 1), ("П", 1),
             ("Р", 1), ("О", 1), ("Л", 1), ("Д", 1), ("Ж", 1), ("Э", 1), ("ENTER", 2.35)],

            [("SHIFT", 2.30), ("Я", 1), ("Ч", 1), ("С", 1), ("М", 1), ("И", 1),
             ("Т", 1), ("Ь", 1), ("Б", 1), ("Ю", 1), ("/", 1), ("Shift", 3.0)],

            [("CTRL", 1.25), ("Win", 1.25), ("ALT", 1.25), ("Space", 7.15),
             ("Alt", 1.25), ("Fn", 1.25), ("Menu", 1.25), ("Ctrl", 1.25)]
        ]

        # self.__set_scale(1.0)

    def __create_keys(self):

        y_offset = self.__y

        if self.__language == KeyboardLanguage.ENGLISH:
            self.__create_keys_from_layout(
                y_offset,
                self.__eng_layout_uppercase if self.__is_upper_case else self.__eng_layout_lowercase
            )
        elif self.__language == KeyboardLanguage.RUSSIAN:
            self.__create_keys_from_layout(y_offset, self.__rus_layout)

    def _switch_layout(self, keys: ScancodeWrapper):
        # Detect if shift has been pressed or released
        shift_pressed = keys[pygame.K_LSHIFT]

        # Only change case if the state is different
        if shift_pressed and not self.__is_upper_case:
            self.__is_upper_case = True
            self.__create_keys()  # Recreate keys with uppercase layout
            print('upper')

        elif not shift_pressed and self.__is_upper_case:
            self.__is_upper_case = False
            self.__create_keys()  # Recreate keys with lowercase layout
            print('lower')
        # print('.....')

    def __create_keys_from_layout(self, y_offset, layout):
        print('call __create_keys_from_layout')
        self.__keys = {}
        for row in layout:
            x_offset = self.__x
            for key, width in row:
                self.__keys[key] = pygame.Rect(x_offset, y_offset, self.__key_size * width, self.__key_size)
                x_offset += self.__key_size * width + self.__spacing
            y_offset += self.__key_size + self.__spacing

    def update(self, screen_height: int, screen_width: int, keys: ScancodeWrapper):
        if self.__screen_height != screen_height or self.__screen_width != screen_width:
            self.__screen_height = screen_height
            self.__screen_width = screen_width
            scale_w = (screen_width * Keyboard.SIZE / Keyboard.LINE_KEYS_COUNT) / \
                (Keyboard.KEY_SIZE + Keyboard.KEY_SPACING)
            self.__set_scale(scale_w)
        self._switch_layout(keys)

    def __set_scale(self, scale: float):
        self.__scale = scale
        self.__x = self.__screen_width / 2 - (Keyboard.LINE_KEYS_COUNT / 2.0 + 1) * Keyboard.KEY_SIZE * self.__scale
        self.__y = self.__screen_height / 2.5 + Keyboard.KEY_SIZE * self.__scale
        self.__key_size = Keyboard.KEY_SIZE * scale
        self.__spacing = Keyboard.KEY_SPACING * scale
        self.__font = pygame.font.Font(None, int(Keyboard.FONT_SIZE * scale))
        self.__create_keys()

    def highlight_key(self, key: str):
        if key in self.__keys:
            self.__highlighted_key = key
        if key == " ":
            self.__highlighted_key = "Space"

    def draw(self, screen: pygame.Surface):
        for key, rect in self.__keys.items():
            bg_color = (30, 30, 30) if key != self.__highlighted_key else (35, 56, 35)
            pygame.draw.rect(screen, bg_color, rect, border_radius=5)
            text = self.__font.render(key, True, (200, 200, 200))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
