import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Paint - R:Rect, C:Circle, P:Pen, E:Eraser, 1-3:Colors")
    
    canvas = pygame.Surface((800, 600))
    canvas.fill((255, 255, 255)) # Белый фон
    
    clock = pygame.time.Clock()
    
    # Настройки
    color = (0, 0, 0)      # Черный
    thickness = 5          
    mode = 'pen'           # Начальный режим
    
    drawing = False
    start_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            # ГОРЯЧИЕ КЛАВИШИ
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: mode = 'rect'    # R - Прямоугольник
                if event.key == pygame.K_c: mode = 'circle'  # C - Круг
                if event.key == pygame.K_p: mode = 'pen'     # P - Карандаш
                if event.key == pygame.K_e: mode = 'eraser'  # E - Ластик
                if event.key == pygame.K_BACKSPACE: canvas.fill((255, 255, 255)) # Стереть всё
                
                # Цвета: 1-Красный, 2-Зеленый, 3-Синий, 0-Черный
                if event.key == pygame.K_1: color = (255, 0, 0)
                if event.key == pygame.K_2: color = (0, 255, 0)
                if event.key == pygame.K_3: color = (0, 0, 255)
                if event.key == pygame.K_0: color = (0, 0, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                if mode == 'pen':
                    pygame.draw.circle(canvas, color, event.pos, thickness)

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    if mode == 'rect':
                        draw_rect(canvas, start_pos, event.pos, color)
                    elif mode == 'circle':
                        draw_circle(canvas, start_pos, event.pos, color)
                drawing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == 'pen':
                        pygame.draw.circle(canvas, color, event.pos, thickness)
                    elif mode == 'eraser':
                        pygame.draw.circle(canvas, (255, 255, 255), event.pos, 20)

        # Отрисовка
        screen.blit(canvas, (0, 0)) # Рисуем накопленное на холсте
        
        # Предпросмотр
        if drawing:
            curr_pos = pygame.mouse.get_pos()
            if mode == 'rect':
                draw_rect(screen, start_pos, curr_pos, color, preview=True)
            elif mode == 'circle':
                draw_circle(screen, start_pos, curr_pos, color, preview=True)

        pygame.display.flip()
        clock.tick(60)

def draw_rect(surf, start, end, color, preview=False):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    if w > 0 and h > 0:
        pygame.draw.rect(surf, color, (x, y, w, h), 1 if preview else 0)

def draw_circle(surf, start, end, color, preview=False):
    rad = int(math.hypot(end[0]-start[0], end[1]-start[1]))
    if rad > 0:
        pygame.draw.circle(surf, color, start, rad, 1 if preview else 0)

if __name__ == "__main__":
    main()