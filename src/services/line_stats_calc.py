import pygame
from common.time_provider import TimeProvider
from services.line_stats import LineStats
from pygame.typing import RectLike


class LineStatsCalc:
    FONT_SIZE = 50

    def __init__(self, time_provider: TimeProvider):
        self.__success_count = 0
        self.__error_count = 0
        self.__time_provider = time_provider
        self.__start_time_utc = None
        self.__end_time_utc = None
        self.__scale = 1.0
        self.__screen_height = 0
        self.__screen_width = 0

    def is_stopped(self):
        return self.__end_time_utc

    def start(self):
        self.__start_time_utc = self.__time_provider.get_utc_time()
        self.__success_count = 0
        self.__error_count = 0
        self.__end_time_utc = None
        self.__intervals = []
        self.__pref_key_press_time = self.__start_time_utc

    def stop(self):
        self.__end_time_utc = self.__time_provider.get_utc_time()

    def symbol_typed(self, is_error: bool):

        if not self.__start_time_utc:
            raise Exception(f"Please call {LineStatsCalc.__name__}.{LineStatsCalc.start.__name__}() first.")

        if is_error:
            self.__error_count += 1
        else:
            self.__success_count += 1
            key_press_time = self.__time_provider.get_utc_time()
            self.__intervals.append((key_press_time - self.__pref_key_press_time).total_seconds())
            self.__pref_key_press_time = key_press_time

    def get_stats(self) -> LineStats:
        end_time = self.__end_time_utc if self.__end_time_utc else self.__time_provider.get_utc_time()
        start_time = self.__start_time_utc if self.__start_time_utc else end_time
        duration_minutes: float = (end_time - start_time).total_seconds() / 60.0

        # Идеальный интервал
        mean_interval = sum(self.__intervals) / len(self.__intervals)

        # Вычисляем отклонение от идеального интервала для каждого интервала
        deviations = [abs(interval - mean_interval) / mean_interval for interval in self.__intervals]

        # Рассчитываем среднее отклонение
        avg_deviation = sum(deviations) / len(deviations)

        # Ритм в процентах (меньше отклонение - выше процент)
        rhythm_percentage = (1 - avg_deviation) * 100

        if duration_minutes == 0:
            speed_symbols_per_minute = 0
        else:
            speed_symbols_per_minute: float = self.__success_count / duration_minutes

        return LineStats(
            error_count=self.__error_count,
            speed_symbols_per_minute=speed_symbols_per_minute,
            rhythm_percentage=rhythm_percentage
        )

    def update(self, screen_height: int, screen_width: int):
        if self.__screen_height != screen_height or self.__screen_width != screen_width:
            self.__screen_height = screen_height
            self.__screen_width = screen_width

            scale_w = screen_width / 1920.0
            scale_h = screen_height / 1080.0
            self.__scale = min(scale_w, scale_h)

            self.__font = pygame.font.Font(None, int(self.FONT_SIZE * self.__scale))

    def draw(self, screen: pygame.Surface):
        if not self.is_stopped():
            return

        stats = self.get_stats()
        window_width = 400 * self.__scale
        diff_x = int(screen.get_width() - window_width)

        line_rect = pygame.Rect(
            diff_x,
            100 * self.__scale,
            window_width,
            self.FONT_SIZE * 1.5 * 2 * self.__scale
        )

        pygame.draw.rect(screen, (0, 0, 0), line_rect)

        self.__draw_text(screen, (diff_x, line_rect.y), f'Speed: {int(stats.speed_symbols_per_minute)}')
        self.__draw_text(screen, (diff_x, line_rect.y + self.FONT_SIZE * 1.5 *
                         self.__scale), f'Errors: {int(stats.error_count)}')
        self.__draw_text(screen, (diff_x, line_rect.y + 2 * self.FONT_SIZE * 1.5 *
                                  self.__scale), f'Rythm: {int(stats.rhythm_percentage)}')

    def __draw_text(self, screen: pygame.Surface, pos: RectLike, text: str):
        speed_text = self.__font.render(text, True, (200, 200, 200))
        screen.blit(speed_text, pos)
