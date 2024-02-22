import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
    """Класс для вывода игровой информации"""

    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчеста очков"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        #Настройки шрифта для вывода счета
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        #Подготовка исходных изображений
        self.prep_score()
        self.prep_record()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        #Вывод счета в правой верхней части экрана 
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20 

    def show_score(self):
        """Выводит очки , уровень и количество кораблей на экран"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.record_image, self.record_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)


    def prep_record(self):
        """Преобразует текущий рекорд к графическое изображение"""
        rounded_record = round(self.stats.record, -1)
        record_str = "{:,}".format(rounded_record)
        self.record_image = self.font.render(
            record_str, True, self.text_color, self.settings.bg_color
        )

        #Выравнивание рекорда по центру верхней стороны экрана 
        self.record_rect = self.record_image.get_rect()
        self.record_rect.center = self.screen_rect.center
        self.record_rect.top = self.screen_rect.top

    def check_record(self):
        """Проверяет, появился ли новый рекорд"""
        if self.stats.score > self.stats.record:
            self.stats.record = self.stats.score
            self.prep_record()

    def prep_level(self):
        """ Преобразует уровень в графическое изображение"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
        )

        #Уровень выводится под текущим счетом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_ships(self):
        """Сообщает количество оставшихся кораблей"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

