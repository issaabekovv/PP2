import pygame, sys
from pygame.locals import *
import random, time

# Инициализация Pygame
pygame.init()

# Константы игры
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0 

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# Шрифты для текста
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка фонового изображения
background = pygame.image.load("AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Racer Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        # Появляется над экраном в случайной позиции по горизонтали
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -100) 

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        # Если враг уехал вниз, возвращаем его наверх
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

# Extra task: Класс для монет
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        # Появляется в случайном месте выше игрока
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), -200)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.reset()

    def reset(self):
        self.rect.top = -50
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

# Создание объектов и групп
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins_group = pygame.sprite.Group()
coins_group.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 2000)

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.2      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона
    DISPLAYSURF.blit(background, (0,0))
    
    # Отображение счета врагов
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    # Extra task: Отображение счета монет в правом верхнем углу
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 110, 10))

    # Обновление позиций и отрисовка всех объектов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Extra task: Сбор монет
    if pygame.sprite.spritecollideany(P1, coins_group):
        COINS += 1
        C1.reset() # Перемещаем монету после сбора

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
          # Попытка проиграть звук, если файл существует
          try:
              pygame.mixer.Sound('crash.wav').play()
          except:
              pass
          
          time.sleep(0.5)
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          pygame.display.update()
          
          time.sleep(2)
          pygame.quit()
          sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)