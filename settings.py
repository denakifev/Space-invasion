class Settings:
    '''Класс для хранения всех настроек игры'''
    def __init__(self):
        """Инициализирует статистические настройки игры"""
        #Параметры экрана
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230) #Белый цвет 
        
        #Настройки корабля 
        self.ship_limit = 3

        #Настройки снаряда 
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (230, 0, 0) #Красный цвет снаряда 
        self.bullets_allowed = 5

        #Настройки пришельцов 
        self.fleet_drop_speed = 10
        
        #Темп ускорения игры
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

        #Темп роста стоимости пришельцев
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        """Инициализирует настойки изменяющиеся в ходе игры"""
        self.ship_speed = 1
        self.bullet_speed = 1.5
        self.alien_speed = 1
        
        #Подсчет очков
        self.alien_points = 50

        # fleet_direction = 1 обозначает движение вправо; а -1 влево
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает скорость игры и стоимось пришельца"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)