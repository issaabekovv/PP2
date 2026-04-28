import pygame
import random
import sys
from db import Database
from config import load_settings, save_settings
from game import GameLogic, FOOD, POISON, POWERUP
import json
import os


# Инициализация Pygame и глобальных объектов
pygame.init()
db = Database()
settings = load_settings()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake TSIS 4")
font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

# Константы цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_RED = (100, 0, 0) # Ядовитая еда
GREEN = (0, 255, 0)    # Обычная еда
BLUE = (0, 0, 255)     # Бонусы
YELLOW = (255, 215, 0)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, 'settings.json')

DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],
    "grid_overlay": True,
    "sound": True
}

def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)

def input_username():
    """Экран ввода имени пользователя с клавиатуры"""
    username = ""
    while True:
        screen.fill((30, 30, 30))
        prompt = font.render("Enter Username:", True, WHITE)
        txt = font.render(username + "_", True, YELLOW)
        screen.blit(prompt, (WIDTH//2 - 70, HEIGHT//2 - 40))
        screen.blit(txt, (WIDTH//2 - 50, HEIGHT//2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(username) > 0:
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 15 and event.unicode.isalnum():
                        username += event.unicode

def show_leaderboard():
    """Экран таблицы лидеров (Топ-10)"""
    records = db.get_top_10()
    running = True
    while running:
        screen.fill(BLACK)
        title = font.render("TOP 10 LEADERBOARD", True, YELLOW)
        screen.blit(title, (200, 20))
        
        y = 70
        for i, (name, score, lvl, date) in enumerate(records):
            txt = font.render(f"{i+1}. {name}: {score} pts (Lvl {lvl})", True, WHITE)
            screen.blit(txt, (100, y))
            y += 30
            
        btn = font.render("Press ESC to Back", True, (150, 150, 150))
        screen.blit(btn, (220, 350))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

def show_settings():
    """Экран настроек: переключение сетки и выбор цвета змейки"""
    global settings
    running = True
    while running:
        screen.fill((20, 20, 20))
        title = font.render("SETTINGS", True, YELLOW)
        grid_status = "ON" if settings.get('grid_overlay') else "OFF"
        grid_txt = font.render(f"1. Grid Overlay: {grid_status}", True, WHITE)
        color_txt = font.render(f"2. Snake Color: {settings.get('snake_color')}", True, WHITE)
        hint_txt = font.render("Press ESC to Save & Back", True, (150, 150, 150))

        screen.blit(title, (250, 50))
        screen.blit(grid_txt, (180, 150))
        screen.blit(color_txt, (180, 200))
        screen.blit(hint_txt, (180, 350))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_settings(settings) # Сохранение в settings.json
                    running = False
                if event.key == pygame.K_1:
                    settings['grid_overlay'] = not settings['grid_overlay']
                if event.key == pygame.K_2:
                    # Циклический выбор цвета
                    colors = [[0, 255, 0], [255, 255, 255], [0, 255, 255], [255, 165, 0]]
                    current_color = settings.get('snake_color', [0, 255, 0])
                    idx = colors.index(current_color) if current_color in colors else 0
                    settings['snake_color'] = colors[(idx + 1) % len(colors)]

def run_game(player_id, best_score):
    """Основной игровой процесс"""
    logic = GameLogic(settings)
    snake_list = [[300, 200]]
    direction = "RIGHT"
    change_to = direction
    length = 3
    score = 0
    level = 1
    base_speed = 10
    current_speed = base_speed
    
    food_pos = logic.spawn_food(snake_list)
    poison_pos = logic.spawn_food(snake_list)
    powerup = None # [x, y, type, expire_time]
    
    powerup_timer = 0
    shield_active = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN': change_to = 'UP'
                if event.key == pygame.K_DOWN and direction != 'UP': change_to = 'DOWN'
                if event.key == pygame.K_LEFT and direction != 'RIGHT': change_to = 'LEFT'
                if event.key == pygame.K_RIGHT and direction != 'LEFT': change_to = 'RIGHT'
        
        direction = change_to
        head = list(snake_list[-1])
        if direction == 'UP': head[1] -= 20
        elif direction == 'DOWN': head[1] += 20
        elif direction == 'LEFT': head[0] -= 20
        elif direction == 'RIGHT': head[0] += 20

        # Столкновения со стенами, собой или препятствиями
        collision = (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or 
                     head in logic.obstacles or head in snake_list[:-1])
        
        if collision:
            if shield_active:
                shield_active = False # Эффект бонуса Shield
            else:
                running = False 

        snake_list.append(head)
        if len(snake_list) > length:
            del snake_list[0]

        # Логика еды
        if head == food_pos:
            score += 1
            length += 1
            food_pos = logic.spawn_food(snake_list)
            if score % 3 == 0:
                level += 1
                base_speed += 2
                logic.generate_obstacles(level, snake_list) # Генерация препятствий
        
        # Логика ядовитой еды
        if head == poison_pos:
            length -= 2
            poison_pos = logic.spawn_food(snake_list)
            if length < 1: running = False
        
        # Логика бонусов (Power-ups)
        ticks = pygame.time.get_ticks()
        if not powerup and random.randint(1, 150) == 1:
            p_pos = logic.spawn_food(snake_list)
            p_type = random.choice(["speed", "slow", "shield"])
            powerup = [p_pos[0], p_pos[1], p_type, ticks + 8000] # Исчезает через 8 сек

        if powerup:
            if ticks > powerup[3]:
                powerup = None
            elif head == [powerup[0], powerup[1]]:
                if powerup[2] == "speed": current_speed = base_speed + 7
                elif powerup[2] == "slow": current_speed = max(5, base_speed - 5)
                elif powerup[2] == "shield": shield_active = True
                powerup_timer = ticks + 5000 # Длится 5 сек
                powerup = None

        if ticks > powerup_timer:
            current_speed = base_speed

        # --- ОТРИСОВКА ---
        screen.fill(BLACK)
        if settings.get("grid_overlay"): # Сетка из настроек
            for x in range(0, WIDTH, 20): pygame.draw.line(screen, (30,30,30), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, 20): pygame.draw.line(screen, (30,30,30), (0, y), (WIDTH, y))

        logic.draw_obstacles(screen)
        pygame.draw.rect(screen, GREEN, [food_pos[0], food_pos[1], 20, 20])
        pygame.draw.rect(screen, DARK_RED, [poison_pos[0], poison_pos[1], 20, 20])
        
        if powerup:
            pygame.draw.rect(screen, BLUE, [powerup[0], powerup[1], 20, 20])

        for pos in snake_list:
            color = settings.get("snake_color", [0, 255, 0])
            if shield_active: color = (100, 200, 255) # Цвет при активном щите
            pygame.draw.rect(screen, color, [pos[0], pos[1], 20, 20])

        score_txt = font.render(f"Score: {score}  Lvl: {level}  PB: {best_score}", True, WHITE)
        screen.blit(score_txt, (10, 10))
        
        pygame.display.flip()
        clock.tick(current_speed)

    db.save_session(player_id, score, level) # Сохранение в БД
    show_game_over(score, level)

def show_game_over(score, level):
    """Экран Game Over"""
    while True:
        screen.fill((50, 0, 0))
        txt = font.render(f"GAME OVER! Score: {score} Lvl: {level}", True, WHITE)
        hint = font.render("Press R to Restart or M for Menu", True, YELLOW)
        screen.blit(txt, (180, 150))
        screen.blit(hint, (150, 200))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return 
                if event.key == pygame.K_m: main()
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

def main():
    """Главное меню игры"""
    username = input_username()
    player_id = db.get_or_create_player(username) #
    
    while True:
        best_score = db.get_personal_best(player_id)
        screen.fill((20, 20, 20))
        title = font.render(f"Welcome, {username}!", True, GREEN)
        play_btn = font.render("1. Play Game", True, WHITE)
        lead_btn = font.render("2. Leaderboard", True, WHITE)
        sett_btn = font.render("3. Settings", True, WHITE)
        quit_btn = font.render("4. Quit", True, WHITE)
        
        screen.blit(title, (220, 50))
        screen.blit(play_btn, (240, 130))
        screen.blit(lead_btn, (240, 180))
        screen.blit(sett_btn, (240, 230))
        screen.blit(quit_btn, (240, 280))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: run_game(player_id, best_score)
                if event.key == pygame.K_2: show_leaderboard()
                if event.key == pygame.K_3: show_settings()
                if event.key == pygame.K_4: pygame.quit(); sys.exit()

if __name__ == "__main__":
    main()