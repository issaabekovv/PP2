import pygame
import random
import time

# Константы для типов объектов
FOOD = "food"
POISON = "poison"
POWERUP = "powerup"

class GameLogic:
    def __init__(self, settings):
        self.settings = settings
        self.obstacles = []
        self.powerup_active = None
        self.powerup_end_time = 0
        self.has_shield = False

    def generate_obstacles(self, level, snake_list):
        self.obstacles = []
        if level >= 3:
            # Генерируем 5-10 блоков, следя, чтобы они не зажали змейку
            for _ in range(level * 2):
                while True:
                    obs = [random.randrange(0, 600, 20), random.randrange(0, 400, 20)]
                    # Проверка: не на змейке и не вплотную к голове
                    if obs not in snake_list:
                        self.obstacles.append(obs)
                        break

    def spawn_food(self, snake_list, type=FOOD):
        while True:
            pos = [random.randrange(0, 600, 20), random.randrange(0, 400, 20)]
            if pos not in snake_list and pos not in self.obstacles:
                return pos
            
    # Добавь эти методы в класс GameLogic в файле game.py
    def spawn_powerup(self, snake_list):
        """Создает случайный бонус на 8 секунд"""
        types = ["speed", "slow", "shield"]
        pos = self.spawn_food(snake_list) # Используем ту же логику спавна
        p_type = random.choice(types)
        # Возвращаем: [x, y, тип, время_исчезновения]
        return [pos[0], pos[1], p_type, pygame.time.get_ticks() + 8000]

    def draw_grid(self, screen):
        """Рисует сетку, если она включена в настройках"""
        for x in range(0, 600, 20):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 400))
        for y in range(0, 400, 20):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))
            
    # В отрисовке внутри game.py
    def draw_obstacles(self, screen):
        for obs in self.obstacles:
            pygame.draw.rect(screen, (100, 100, 100), [obs[0], obs[1], 20, 20])