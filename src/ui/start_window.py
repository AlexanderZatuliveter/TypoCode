import inspect
import sys
from typing import List
from pygame import Rect
from pygame.event import Event
import pygame_gui
from pygame_gui.elements import UIButton, UISelectionList
from game_state import GameState
from pygame_gui import UIManager
import generators
from generators.generator_abc import GeneratorABC


class StartWindow:

    def __init__(self, game_state: GameState, manager: UIManager):
        self.__game_state = game_state
        self.__manager = manager

        self.__screen_width = 0
        self.__screen_height = 0

        self.__generators_list_items = self.__gens_list_items()
        self.__generator_names = list(self.__generators_list_items.keys())

        self.__selection_list = UISelectionList(
            relative_rect=Rect(200, 200, 1000, 600),
            item_list=self.__generator_names,
            manager=self.__manager,
            default_selection=self.__generator_names[0]
        )

        self.__start_button = UIButton(
            relative_rect=Rect(500, 900, 350, 100),
            text="Start",
            manager=self.__manager,
        )

        self.__exit_button = UIButton(
            relative_rect=Rect(500, 1100, 350, 100),
            text="Exit",
            manager=self.__manager
        )

        self.__objects_zip = list(zip(
            [self.__selection_list, self.__start_button, self.__exit_button],
            [0, 700, 850]
        ))

    def __set_object_pos(self, screen_width: int, screen_height: int,
                         object: UIButton | UISelectionList, y_offset: int):

        pos_x = screen_width // 2 - object.relative_rect.width // 2
        pos_y = screen_height // 2 - 475 + y_offset

        object.set_position((pos_x, pos_y))
        object.rebuild()

    def __update_positions(self):
        for object, y_offset in self.__objects_zip:
            self.__set_object_pos(self.__screen_width, self.__screen_height, object, y_offset)

    def update(self, events: List[Event], screen_width: int, screen_height: int):
        if self.__screen_height != screen_height or self.__screen_width != screen_width:
            self.__screen_height = screen_height
            self.__screen_width = screen_width
            self.__update_positions()

        for event in events:
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                selected_item = self.__selection_list.get_single_selection()
                if selected_item and selected_item in self.__generators_list_items:
                    self.__game_state.generator = self.__generators_list_items[selected_item]
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.__start_button:
                    self.__game_state.is_started = True
                if event.ui_element == self.__exit_button:
                    sys.exit()

    def __gens_list_items(self):
        item = {}
        for name, generator_cls in inspect.getmembers(generators):
            if inspect.isclass(generator_cls) and issubclass(generator_cls, GeneratorABC):
                gen = generator_cls()
                item[gen.display_name] = gen
        return item
