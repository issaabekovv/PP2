import pygame
import random
import time

# Инициализация
pygame.init()

# Константы
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)      # Цвет для "тяжелой" еды
GREEN = (0, 255, 0)      # Цвет для обычной еды
YELLOW = (255, 255, 102)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake: Food Weights & Timers')
clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift", 25)

def display_ui(score, level):
    """Отображает счет и уровень"""
    value = font_style.render(f"Score: {score}  Level: {level}", True, YELLOW)
    screen.blit(value, [10, 10])

def generate_new_food(snake_list):
    """
    Создает новую еду с весом и таймером.
    Вес влияет на количество очков и размер хвоста.
    """
    foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    
    # 1. Задаем вес еды (случайно от 1 до 3)
    weight = random.randint(1, 3)
    
    # 2. Задаем время жизни еды в секундах (например, от 5 до 10 сек)
    timer = time.time() + random.randint(5, 10)
    
    # Цвет зависит от веса: 1 - зеленый, 3 - красный
    color = GREEN if weight == 1 else RED
    
    return [foodx, foody, weight, timer, color]

def gameLoop():
    game_over = False
    game_close = False

    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1
    score = 0
    level = 1
    snake_speed = 10

    # Генерируем первую еду
    # Структура: [x, y, weight, expiration_time, color]
    current_food = generate_new_food(snake_List)

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            msg = font_style.render("Game Over! Press C-Play Again or Q-Quit", True, RED)
            screen.blit(msg, [WIDTH / 6, HEIGHT / 3])
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
                    x1_change, y1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change, y1_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change, x1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change, x1_change = BLOCK_SIZE, 0

        # СТОЛКНОВЕНИЕ СО СТЕНАМИ
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)

        # ПРОВЕРКА ТАЙМЕРА ЕДЫ
        # Если текущее время больше, чем время "смерти" еды — генерируем новую
        if time.time() > current_food[3]:
            current_food = generate_new_food(snake_List)

        # Рисуем еду
        pygame.draw.rect(screen, current_food[4], [current_food[0], current_food[1], BLOCK_SIZE, BLOCK_SIZE])

        # Логика движения змейки
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for segment in snake_List:
            pygame.draw.rect(screen, WHITE, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

        display_ui(score, level)
        pygame.display.update()

        # ПРОВЕРКА ПОЕДАНИЯ ЕДЫ
        if x1 == current_food[0] and y1 == current_food[1]:
            # Прибавляем очки и длину хвоста согласно весу еды
            weight_eaten = current_food[2]
            score += weight_eaten
            Length_of_snake += weight_eaten
            
            # Повышаем уровень каждые 5 очков
            if score // 5 >= level:
                level += 1
                snake_speed += 2
            
            # Сразу создаем новую еду
            current_food = generate_new_food(snake_List)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()