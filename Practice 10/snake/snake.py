import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Константы экрана и цветов
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# Настройка дисплея
dis = pygame.display.set_caption('Snake Game: Levels and Speed')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_score(score, level):
    """Отображает текущий счет и уровень на экране"""
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    screen.blit(value, [10, 10])

def generate_food(snake_list):
    """Генерирует позицию еды, которая не совпадает с телом змейки"""
    while True:
        foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        # Проверка: не попала ли еда на сегмент змейки
        if [foodx, foody] not in snake_list:
            return foodx, foody

def gameLoop():
    game_over = False
    game_close = False

    # Начальные координаты змейки
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1

    # Начальные параметры прогрессии
    score = 0
    level = 1
    snake_speed = 10 
    
    foodx, foody = generate_food(snake_List)

    while not game_over:

        while game_close == True:
            screen.fill(BLACK)
            msg = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, RED)
            screen.blit(msg, [WIDTH / 6, HEIGHT / 3])
            display_score(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        #ПРОВЕРКА СТОЛКНОВЕНИЯ СО СТЕНАМИ
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        
        # Рисуем еду
        pygame.draw.rect(screen, GREEN, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Столкновение с самим собой
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Рисуем змейку
        for x in snake_List:
            pygame.draw.rect(screen, WHITE, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

        # Отображаем UI
        display_score(score, level)
        pygame.display.update()

        # --- 2. ЛОГИКА ПОЕДАНИЯ И УРОВНЕЙ ---
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List) # Безопасная генерация
            Length_of_snake += 1
            score += 1
            
            # --- 3. ПЕРЕХОД НА НОВЫЙ УРОВЕНЬ ---
            # Повышаем уровень каждые 3 очка
            if score % 3 == 0:
                level += 1
                snake_speed += 2 # Увеличиваем скорость

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()