import pygame, sys, time

pygame.mixer.init()
pygame.init()
import random

CELL_SIZE = 16
GRID_COLS = 42
GRID_ROWS = 34
CANVAS_WIDTH = GRID_COLS * CELL_SIZE
CANVAS_HEIGHT = GRID_ROWS * CELL_SIZE
PALETTE_WIDTH = 140

WINDOW_WIDTH = CANVAS_WIDTH + PALETTE_WIDTH
WINDOW_HEIGHT = CANVAS_HEIGHT

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pixelator")

clock = pygame.time.Clock()

PALETTE_COLORS = [
    (0, 0, 0),       # black
    (255, 255, 255), # white
    (255, 0, 0),     # red
    (0, 255, 0),     # green
    (0, 0, 255),     # blue
    (255, 255, 0),   # yellow
    (255, 165, 0),   # orange
    (255, 192, 203), # pink
    (128, 0, 128),   # purple
    (165, 42, 42),   # brown
    (64, 224, 208),  # turquoise
    (128, 128, 128), # gray
    (255, 20, 147),  # deep pink
    (0, 128, 128),   # teal
    (255, 105, 180), # hot pink
    (0, 0, 139)      # dark blue
]

selected_color = PALETTE_COLORS[0]
font = pygame.font.Font(None, 24)

# grid[row][col] stores the color of each cell
grid = [[(255, 255, 255) for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

pygame.mixer.music.load("Bonetrousle.mp3")
def draw_grid(surface):
    # fill cells
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, grid[row][col], rect)

    # grid lines – horizontal
    for r in range(GRID_ROWS + 1):
        y = r * CELL_SIZE
        pygame.draw.line(surface, (220, 220, 220), (0, y), (CANVAS_WIDTH, y), 1)

    # grid lines – vertical
    for c in range(GRID_COLS + 1):
        x = c * CELL_SIZE  
        pygame.draw.line(surface, (220, 220, 220), (x, 0), (x, CANVAS_HEIGHT), 1)

def draw_palette(surface):
    palette_rect = pygame.Rect(CANVAS_WIDTH, 0, PALETTE_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(surface, (200, 200, 200), palette_rect)

    title = font.render("Palette", True, (0, 0, 0))
    surface.blit(title, (CANVAS_WIDTH + 10, 10))

    button_size = 28
    padding = 8
    start_x = CANVAS_WIDTH + 16
    start_y = 30
    per_row = 3

    # draw color buttons
    for index, color in enumerate(PALETTE_COLORS):
        row = index // per_row
        col = index % per_row
        x = start_x + col * (button_size + padding)
        y = start_y + row * (button_size + padding)
        rect = pygame.Rect(x, y, button_size, button_size)

        pygame.draw.rect(surface, color, rect)

        border_color = (0, 0, 0)
        border_width = 2 if selected_color == color else 1
        pygame.draw.rect(surface, border_color, rect, border_width)

    # helper text (moved OUT of the loop so it doesn't draw 16 times)
    helper1 = font.render("Left Click: Paint", True, (0, 0, 0))
    helper2 = font.render("Right Click: Erase", True, (0, 0, 0))
    helper3 = font.render("C: Clear   S: Save", True, (0, 0, 0))
    surface.blit(helper1, (CANVAS_WIDTH + 10, WINDOW_HEIGHT - 70))
    surface.blit(helper2, (CANVAS_WIDTH + 10, WINDOW_HEIGHT - 50))
    surface.blit(helper3, (CANVAS_WIDTH + 10, WINDOW_HEIGHT - 30))

def get_cells_from_mouse(pos):
    mx, my = pos
    if mx < 0 or mx >= CANVAS_WIDTH:
        return None
    if my < 0 or my >= WINDOW_HEIGHT:
        return None
    col = mx // CELL_SIZE
    row = my // CELL_SIZE
    return row, col

def handle_palette_click(pos):
    global selected_color
    button_size = 28
    padding = 8
    start_x = CANVAS_WIDTH + 16
    start_y = 30
    per_row = 3

    mx, my = pos
    for i, color in enumerate(PALETTE_COLORS):
        row = i // per_row
        col = i % per_row
        x = start_x + col * (button_size + padding)
        y = start_y + row * (button_size + padding)
        rect = pygame.Rect(x, y, button_size, button_size)
        if rect.collidepoint(mx, my):
            selected_color = color
            break

def clear_canvas():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            grid[row][col] = (255, 255, 255)

def save_canvas():
    surface = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, grid[row][col], rect)

    filename = f"pixel_art_{int(time.time())}.png"
    pygame.image.save(surface, filename)
    print(f"Canvas saved as {filename}")

prank_font = pygame.font.Font(None, 48)
prank_text = prank_font.render("Goodluck Tryna Draw Twin", True, (255, 0, 0))

prank_triggered = False
prank_start_time = None



rainbow_mode = True
#Main Loop

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not prank_triggered:
                pygame.mixer.music.play(-1)  # loop forever
                prank_triggered = True
                prank_start_time = pygame.time.get_ticks()

            mx, my = event.pos
            if mx >= CANVAS_WIDTH:
                # clicked in palette area
                handle_palette_click(event.pos)
            else:
                # clicked on canvas
                cell = get_cells_from_mouse(event.pos)
                if cell is not None:
                    row, col = cell
                    if event.button == 1:  # left click = paint
                        if rainbow_mode:
                            grid[row][col] = random.choice(PALETTE_COLORS)
                        else:
                            grid[row][col] = selected_color
                    elif event.button == 3:  # right click = erase
                        grid[row][col] = (255, 255, 255)

        elif event.type == pygame.MOUSEMOTION:
            # smooth painting while dragging
            if event.buttons[0]:  # left held
                cell = get_cells_from_mouse(event.pos)
                if cell is not None:
                    r, c = cell
                    if rainbow_mode:
                        grid[r][c] = random.choice(PALETTE_COLORS)
                    else:
                        grid[r][c] = selected_color
            elif event.buttons[2]:  # right held (erase)
                cell = get_cells_from_mouse(event.pos)
                if cell is not None:
                    r, c = cell
                    grid[r][c] = (255, 255, 255)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                clear_canvas()
            elif event.key == pygame.K_s:
                save_canvas()
            elif event.key == pygame.K_r:  # toggle rainbow mode
                rainbow_mode = not rainbow_mode
                print("🌈 Rainbow mode:", rainbow_mode)

    # --- drawing ---
    screen.fill((255, 255, 255))
    draw_grid(screen)
    draw_palette(screen)

    # prank text fade
    if prank_triggered:
        elapsed = (pygame.time.get_ticks() - prank_start_time) / 1000  # seconds
        fade_duration = 5
        if elapsed < fade_duration:
            alpha = max(0, 255 - int((elapsed / fade_duration) * 255))
            text_surface = prank_text.copy()
            text_surface.set_alpha(alpha)
            text_rect = text_surface.get_rect(midtop=(CANVAS_WIDTH // 2, 20))
            screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
