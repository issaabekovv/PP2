import pygame
import sys
import os
from datetime import datetime
from tools import draw_shape, flood_fill

def main():
    pygame.init()
    screen = pygame.display.set_mode((900, 700))
    # В заголовке подсказки по основным кнопкам
    pygame.display.set_caption("Paint: P:Pencil, R:Rect, S:Square, T:RightTri, U:EquilatTri, D:Rhombus, Ctrl+S:Save")
    
    canvas = pygame.Surface((900, 700))
    canvas.fill((255, 255, 255))
    
    clock = pygame.time.Clock()
    
    # Системные шрифты
    font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 18)
    
    color = (0, 0, 0)
    mode = 'pencil'
    thickness = 2
    drawing = False
    start_pos = None
    last_pos = None
    
    text_input = ""
    text_pos = None
    typing = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()

                # --- 1. УМНОЕ СОХРАНЕНИЕ (Ctrl + S) ---
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    # Определяем папку, в которой лежит этот файл paint.py
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    # Формируем имя файла
                    filename = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    # Соединяем путь к папке и имя файла
                    full_path = os.path.join(current_dir, filename)
                    
                    pygame.image.save(canvas, full_path)
                    print(f"Файл успешно сохранен в папку проекта: {full_path}")
                    continue 

                # --- 2. ВВОД ТЕКСТА ---
                if typing:
                    if event.key == pygame.K_RETURN:
                        txt_surf = font.render(text_input, True, color)
                        canvas.blit(txt_surf, text_pos)
                        typing = False
                    elif event.key == pygame.K_ESCAPE:
                        typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                    continue

                # --- 3. ЦВЕТА (Клавиши 1, 2, 3, 0) ---
                if event.key == pygame.K_1: color = (255, 0, 0)
                if event.key == pygame.K_2: color = (0, 255, 0)
                if event.key == pygame.K_3: color = (0, 0, 255)
                if event.key == pygame.K_0: color = (0, 0, 0)

                # --- 4. ИНСТРУМЕНТЫ  ---
                if not (mods & pygame.KMOD_CTRL):
                    if event.key == pygame.K_p: mode = 'pencil'
                    if event.key == pygame.K_l: mode = 'line'
                    if event.key == pygame.K_g: mode = 'fill'
                    if event.key == pygame.K_w: mode = 'text'
                    if event.key == pygame.K_r: mode = 'rect'    
                    if event.key == pygame.K_s: mode = 'square'  
                    if event.key == pygame.K_c: mode = 'circle'
                    if event.key == pygame.K_e: mode = 'eraser'
                    if event.key == pygame.K_t: mode = 'right_tri'
                    if event.key == pygame.K_u: mode = 'equilat_tri'
                    if event.key == pygame.K_d: mode = 'rhombus'
                
                # --- 5. ТОЛЩИНА (F1, F2, F3) ---
                if event.key == pygame.K_F1: thickness = 2
                if event.key == pygame.K_F2: thickness = 5
                if event.key == pygame.K_F3: thickness = 10

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == 'fill':
                    flood_fill(canvas, event.pos, color)
                elif mode == 'text':
                    typing = True
                    text_pos = event.pos
                    text_input = ""
                else:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    draw_shape(canvas, mode, start_pos, event.pos, color, thickness)
                drawing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing and mode == 'pencil':
                    pygame.draw.line(canvas, color, last_pos, event.pos, thickness)
                    last_pos = event.pos
                elif drawing and mode == 'eraser':
                    pygame.draw.circle(canvas, (255, 255, 255), event.pos, 20)

        # Отрисовка на экране
        screen.blit(canvas, (0, 0))
        
        # Превью фигур
        if drawing and mode not in ['pencil', 'fill', 'text', 'eraser']:
            draw_shape(screen, mode, start_pos, mouse_pos, color, thickness, is_preview=True)
            
        # Текст во время печати
        if typing:
            temp_txt = font.render(text_input + "|", True, color)
            screen.blit(temp_txt, text_pos)

        # Верхняя информационная панель
        pygame.draw.rect(screen, (240, 240, 240), (0, 0, 900, 35))
        pygame.draw.line(screen, (180, 180, 180), (0, 35), (900, 35), 1)
        
        status_text = f"MODE: {mode.upper()}  |  SIZE: {thickness}  |  COLOR: {color}"
        ui_surf = small_font.render(status_text, True, (60, 60, 60))
        screen.blit(ui_surf, (15, 7))

        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    main()