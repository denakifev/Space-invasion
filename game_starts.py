class GameStats:
    """Отслеживание статистики для игры Alien Invasion"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

        #Рекорд не должен сбрасываться
        self.read_record()

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры """
        self.ship_left = self.settings.ship_limit 
        self.score = 0
        self.level = 1

    def read_record(self):
        """Считывает текущий рекорд игрока"""
        with open('record.txt') as f:
            self.record = int(f.read().strip())