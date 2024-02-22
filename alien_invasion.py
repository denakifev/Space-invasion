#!/usr/bin/env python3
import sys 
from time import sleep
import pygame 
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_starts import GameStats
from button import Button
from scoreboard import ScoreBoard

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        
        #Создание экземпляра для хранения игровой статистики и панели результатов
        self.stats = GameStats(self)
        self.scoreboard = ScoreBoard(self)

        #Создание игровых объектов
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #Создание кнопки play
        self.button = Button(self, 'Play')

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            
    def _check_events(self):
        """Обрабатывает нажатия клавиш и событий мыши"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._write_record()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)
    
    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._write_record()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.start_game()

    def _check_keyup_events(self, event):
        """"Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создает новый снаряд и добавляет его в self.bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets:
            if self.stats.game_active:
                bullet.draw_bullet()
        self.aliens.draw(self.screen)

        #Вывод информации о счете
        self.scoreboard.show_score()

        #Кнопка Play отображается в том случае, если игра неактивна
        if not self.stats.game_active:
            self.button.draw_button()
        
        #Отображение последнего прорисованного кадра 
        pygame.display.flip()

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        #Обновление позиций снарядов
        self.bullets.update()

        #Удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _create_fleet(self):
        """Создание флота вторжения"""
        #Создание пришельцев и вычисление количества пришельцев в ряду
        #Интервал между соседними пришельцами равен ширине пришельца
        new_alien = Alien(self)
        alien_width, alien_height = new_alien.rect.size
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = available_space_x // (2 * alien_width)
        # Определяет количество рядов, помещающихся на экране 
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - ship_height - 3 * alien_height
        number_rows = available_space_y // (2 * alien_height)

        #Создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._creat_alien(alien_number, row_number)
                
    def _creat_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду """
        new_alien = Alien(self)
        alien_width, alien_height = new_alien.rect.size
        new_alien.x = alien_width + 2 * alien_width * alien_number
        new_alien.rect.x = new_alien.x
        new_alien.y = alien_height + 2 * alien_height * row_number
        new_alien.rect.y = new_alien.y
        self.aliens.add(new_alien)
        
    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте"""
        self._check_fleet_edges()
        self.aliens.update()

        #Проверка коллизии пришелец-корабль или достижения пришельцем конца экрана
        if pygame.sprite.spritecollideany(self.ship, self.aliens) or self._check_aliens_bottom():
            self._ship_heat()

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана """
        for alien in self.aliens:
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота """
        for alien in self.aliens:
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collision(self):
        """Обработка коллизий снарядов с пришельцами"""
        #При обнаружении попадания удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score() 
            self.scoreboard.check_record()
        
        if not self.aliens:
            #Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed() 

            #Увеличение уровня
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _ship_heat(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ship_left > 0:
            #Уменьшает ship_left и обновляет панель счета
            self.stats.ship_left -= 1
            self.scoreboard.prep_ships()

            #Очистка списков пришельцев и снарядов
            self.bullets.empty()
            self.aliens.empty()

            #Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            #Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            #Указатель мыши должен появиться
            pygame.mouse.set_visible(True)
        
    def _check_aliens_bottom(self):
        """Проверяет добрались ли пришельцы до конца экрана"""
        return any(alien.rect.bottom >= self.ship.screen_rect.bottom for alien in self.aliens)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        if self.button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.start_game()

    def start_game(self):
        """Запускает новую игру"""
        #Сброс игровой статистики
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()

        #Сброс скорости при начале новой игры
        self.settings.initialize_dynamic_settings()
        
        #Очистка списков пришельцев и снарядов
        self.bullets.empty()
        self.aliens.empty()
        
        #Создание нового флота и размещение корабля в центре
        self._create_fleet()
        self.ship.center_ship()
        
        #Указатель мыши скрывается 
        pygame.mouse.set_visible(False)

    def _write_record(self):
        """Записывает рекорд игрока в файл"""
        with open('record.txt', 'w') as f:
            f.write(str(self.stats.record))

if __name__ == '__main__':
    #Создание экземпляра и запуск игры 
    ai = AlienInvasion()
    ai.run_game()