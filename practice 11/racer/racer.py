import pygame, sys
from pygame.locals import *
import random, time

# Инициализация Pygame
pygame.init()

# Настройки экрана и FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# Константы игры
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5        # Начальная скорость
SCORE = 0        # Пропущенные враги
COINS = 0        # Общий счет монет
N = 5            # Каждые N монет скорость врага увеличивается

# Шрифты
font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 60)
game_over_text = font_big.render("Game Over", True, BLACK)

# Загрузка фона
background = pygame.image.load("AnimatedStreet.png")
DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Racer - Practice 11")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100) 

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = -100
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# ОБНОВЛЕННЫЙ КЛАСС COIN: Случайный выбор между двумя типами монет
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Заранее подгружаем оба изображения для оптимизации
        self.image_small = pygame.image.load("coin.png")   # 24x24
        self.image_red = pygame.image.load("coin1.png")    # 35x35
        self.rect = self.image_small.get_rect()
        self.reset()

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.reset()

    def reset(self):
        # Случайно выбираем тип монеты: 0 - обычная (вес 1), 1 - красная (вес 3)
        # Шанс на красную монету можно сделать меньше, например random.randint(0, 3)
        coin_type = random.randint(0, 1) 
        
        if coin_type == 1:
            self.image = self.image_red
            self.weight = 3
        else:
            self.image = self.image_small
            self.weight = 1
            
        self.rect = self.image.get_rect()
        self.rect.top = -50
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группировка
enemies = pygame.sprite.Group()
enemies.add(E1)
coins_group = pygame.sprite.Group()
coins_group.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    
    # Отрисовка статистики
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_scores = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    DISPLAYSURF.blit(coin_scores, (SCREEN_WIDTH - 110, 10))

    # Движение
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Сбор монет с разным весом и логикой ускорения
    if pygame.sprite.collide_rect(P1, C1):
        old_coins = COINS
        COINS += C1.weight # Прибавляем вес текущей монеты (1 или 3)
        
        # Если количество собранных монет достигло порога N, увеличиваем скорость врага
        if COINS // N > old_coins // N:
            SPEED += 1 
            
        C1.reset()

    # Столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        try:
            pygame.mixer.Sound('crash.wav').play()
        except:
            pass
        
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (30,250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)