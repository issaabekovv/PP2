import pygame
import math
import sys 

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint Pro: S-Square, T-Right Tri, U-Equilat Tri, D-Rhombus")
    
    # Холст для сохранения рисунков
    canvas = pygame.Surface((800, 600))
    canvas.fill((255, 255, 255))
    
    clock = pygame.time.Clock()
    color = (0, 0, 0)
    mode = 'pen' 
    drawing = False
    start_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Выбор режимов фигур
                if event.key == pygame.K_s: mode = 'square'
                if event.key == pygame.K_t: mode = 'right_tri'
                if event.key == pygame.K_u: mode = 'equilat_tri'
                if event.key == pygame.K_d: mode = 'rhombus'
                
                # Стандартные режимы
                if event.key == pygame.K_p: mode = 'pen'
                if event.key == pygame.K_r: mode = 'rect'
                if event.key == pygame.K_c: mode = 'circle'
                if event.key == pygame.K_e: mode = 'eraser'
                
                # Выбор цвета (1-3)
                if event.key == pygame.K_1: color = (255, 0, 0)
                if event.key == pygame.K_2: color = (0, 255, 0)
                if event.key == pygame.K_3: color = (0, 0, 255)

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                if mode == 'pen':
                    pygame.draw.circle(canvas, color, event.pos, 5)

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    # Окончательное рисование фигуры на холсте
                    draw_shape(canvas, mode, start_pos, event.pos, color)
                drawing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == 'pen':
                        pygame.draw.circle(canvas, color, event.pos, 5)
                    elif mode == 'eraser':
                        # Ластик рисует белым цветом
                        pygame.draw.circle(canvas, (255, 255, 255), event.pos, 20)

        # Отображаем содержимое холста
        screen.blit(canvas, (0, 0))
        
        # Отрисовка превью (контура) пока кнопка мыши зажата
        if drawing and mode not in ['pen', 'eraser']:
            draw_shape(screen, mode, start_pos, pygame.mouse.get_pos(), color, is_preview=True)

        pygame.display.flip()
        clock.tick(60)

def draw_shape(surface, mode, start, end, color, is_preview=False):
    """Функция для расчета координат и рисования геометрических фигур"""
    x1, y1 = start
    x2, y2 = end
    # Если превью — рисуем только контур (толщина 1), если финал — закрашиваем (толщина 0)
    width = 1 if is_preview else 0 

    if mode == 'rect':
        pygame.draw.rect(surface, color, (min(x1, x2), min(y1, y2), abs(x1-x2), abs(y1-y2)), width)
    
    elif mode == 'square':
        # Квадрат
        side = max(abs(x1-x2), abs(y1-y2))
        rect_x = x1 if x2 > x1 else x1 - side
        rect_y = y1 if y2 > y1 else y1 - side
        pygame.draw.rect(surface, color, (rect_x, rect_y, side, side), width)

    elif mode == 'circle':
        # Радиус через гипотенузу
        rad = int(math.hypot(x2-x1, y2-y1))
        pygame.draw.circle(surface, color, start, rad, width)

    elif mode == 'right_tri':
        # Прямоугольный треугольник 
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, width)

    elif mode == 'equilat_tri':
        # Равносторонний треугольник 
        h = (x2 - x1) * math.sqrt(3) / 2
        points = [(x1, y2), (x2, y2), ((x1 + x2) / 2, y2 - h)]
        pygame.draw.polygon(surface, color, points, width)

    elif mode == 'rhombus':
        # Ромб 
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
        pygame.draw.polygon(surface, color, points, width)

if __name__ == "__main__":
    main()