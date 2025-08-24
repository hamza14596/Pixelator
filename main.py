import pygame, sys, time, random, os

# --- Set working directory to the script's folder ---
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# --- Initialize Pygame ---
pygame.mixer.init()
pygame.init()

# --- Constants ---
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
    (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255),
    (255, 255, 0), (255, 165, 0), (255, 192, 203), (128, 0, 128), (165, 42, 42),
    (64, 224, 208), (128, 128, 128), (255, 20, 147), (0, 128, 128), (255, 105, 180),
    (0, 0, 139)
]

# --- Variables ---
zombie_timer = 0
zombie_interval = 500
selected_color = PALETTE_COLORS[0]

import sys, os

def resource_path(relative_path):
    """ Get absolute path to resource (for dev and for PyInstaller) """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# grid[row][col] stores the color of each cell
grid = [[(255, 255, 255) for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]


try:
    pygame.mixer.music.load(resource_path("Bonetrousle.mp3"))
except pygame.error:
    print("Warning: 'Bonetrousle.mp3' not found, background music will not play.")

try:
    explosion_sound = pygame.mixer.Sound(resource_path("deltarune-explosion.mp3"))
except pygame.error:
    print("Warning: 'deltarune-explosion.mp3' not found, exploding eraser will be silent.")
    explosion_sound = None

font = pygame.font.Font(None, 24)
prank_font = pygame.font.Font(None, 48)
prank_text = prank_font.render("Goodluck Tryna Draw Twin", True, (255, 0, 0))

prank_triggered = False
prank_start_time = None


blast_area = 2


#Functions
def draw_grid(surface):
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, grid[row][col], rect)

    # grid lines
    for r in range(GRID_ROWS+1):
        pygame.draw.line(surface, (220,220,220), (0, r*CELL_SIZE), (CANVAS_WIDTH, r*CELL_SIZE))
    for c in range(GRID_COLS+1):
        pygame.draw.line(surface, (220,220,220), (c*CELL_SIZE, 0), (c*CELL_SIZE, CANVAS_HEIGHT))

def draw_palette(surface):
    pygame.draw.rect(surface, (200,200,200), (CANVAS_WIDTH,0,PALETTE_WIDTH,WINDOW_HEIGHT))
    surface.blit(font.render("Palette", True, (0,0,0)), (CANVAS_WIDTH+10,10))

    button_size = 28
    padding = 8
    start_x = CANVAS_WIDTH+16
    start_y = 30
    per_row = 3

    for index, color in enumerate(PALETTE_COLORS):
        row = index // per_row
        col = index % per_row
        rect = pygame.Rect(start_x + col*(button_size+padding), start_y + row*(button_size+padding), button_size, button_size)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (0,0,0), rect, 2 if selected_color==color else 1)

    # helper text
    surface.blit(font.render("Left Click: Paint", True, (0,0,0)), (CANVAS_WIDTH+10, WINDOW_HEIGHT-70))
    surface.blit(font.render("Right Click: Erase", True, (0,0,0)), (CANVAS_WIDTH+10, WINDOW_HEIGHT-50))
    surface.blit(font.render("C: Clear  S: Save  R: Rainbow  E: Explode", True, (0,0,0)), (CANVAS_WIDTH+10, WINDOW_HEIGHT-30))

def get_cells_from_mouse(pos):
    mx, my = pos
    if mx >= CANVAS_WIDTH or mx < 0 or my < 0 or my >= CANVAS_HEIGHT:
        return None
    return my//CELL_SIZE, mx//CELL_SIZE

def handle_palette_click(pos):
    global selected_color
    button_size = 28
    padding = 8
    start_x = CANVAS_WIDTH+16
    start_y = 30
    per_row = 3
    mx, my = pos
    for i,color in  enumerate(PALETTE_COLORS):
        row = i//per_row
        col = i%per_row
        rect = pygame.Rect(start_x+col*(button_size+padding), start_y+row*(button_size+padding), button_size, button_size)
        if rect.collidepoint(mx,my):
            selected_color = color
            break

def clear_canvas():
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            grid[r][c]=(255,255,255)


def save_canvas():
    surface = pygame.Surface((CANVAS_WIDTH,CANVAS_HEIGHT))
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, grid[r][c], rect)
    filename=f"pixel_art_{int(time.time())}.png"
    pygame.image.save(surface, filename)
    print(f"Saved: {filename}")

def explode_erase(row,col):
    if explosion_sound:
        explosion_sound.play()
    for dr in range(-blast_area, blast_area+1):
        for dc in range(-blast_area, blast_area+1):
            rr, cc = row+dr, col+dc
            if 0<=rr<GRID_ROWS and 0<=cc<GRID_COLS:
                grid[rr][cc]=(255,255,255)



    
    new_grid = [row[:] for row in grid]  
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if grid[r][c] == (0, 255, 0):
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        if grid[rr][cc] == (255, 255, 255) and random.random() < 0.01:
                            new_grid[rr][cc] = (0, 255, 0)
    
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            grid[r][c] = new_grid[r][c]


    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            grid[r][c] = new_grid[r][c]



#Variables
zombie_timer = 0
zombie_interval = 500
selected_color = PALETTE_COLORS[0]

drawing = False
draw_start_time = None
rainbow_mode = False
rainbow_start_time = None
zombie_mode = False
exploding_eraser = True 

# grid[row][col] stores the color of each cell
grid = [[(255, 255, 255) for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

#Functions
def spread_zombies():
    new_grid = [row[:] for row in grid]

    # turn some already drawn pixels green
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if grid[r][c] != (255, 255, 255) and random.random() < 0.05:
                new_grid[r][c] = (0, 255, 0)

    # spread green to neighbors
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if grid[r][c] == (0, 255, 0):
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < GRID_ROWS and 0 <= cc < GRID_COLS:
                        if grid[rr][cc] == (255, 255, 255) and random.random() < 0.02:
                            new_grid[rr][cc] = (0, 255, 0)

    # update grid
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            grid[r][c] = new_grid[r][c]


#Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not prank_triggered:
                prank_triggered = True
                prank_start_time = pygame.time.get_ticks()

            mx, my = event.pos
            if mx >= CANVAS_WIDTH:
                handle_palette_click(event.pos)
            else:
                cell = get_cells_from_mouse(event.pos)
                if cell:
                    row, col = cell
                    if event.button == 1:  # left click draw
                        if draw_start_time is None:   #start timer on first draw
                            draw_start_time = time.time()
                        grid[row][col] = random.choice(PALETTE_COLORS) if rainbow_mode else selected_color
                    elif event.button == 3:  # right click erase
                        if exploding_eraser:
                            explode_erase(row, col)  # explosion only on click
                        else:
                            grid[row][col] = (255, 255, 255)

        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # left drag drawing
                cell = get_cells_from_mouse(event.pos)
                if cell:
                    r, c = cell
                    grid[r][c] = random.choice(PALETTE_COLORS) if rainbow_mode else selected_color
            elif event.buttons[2] and not exploding_eraser:  
                # right drag erase, but only normal erase (not exploding)
                cell = get_cells_from_mouse(event.pos)
                if cell:
                    r, c = cell
                    grid[r][c] = (255, 255, 255)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                clear_canvas()
            elif event.key == pygame.K_s:
                save_canvas()
            elif event.key == pygame.K_r:
                rainbow_mode = not rainbow_mode
            elif event.key == pygame.K_e:
                exploding_eraser = not exploding_eraser

    screen.fill((255, 255, 255))
    draw_grid(screen)
    draw_palette(screen)


    # Timed Modes
    fade_duration = 5
    if draw_start_time:
        elapsed = time.time() - draw_start_time
        if elapsed > 8 and not rainbow_mode:
            rainbow_mode = True
            rainbow_start_time = pygame.time.get_ticks()
            pygame.mixer.music.play(-1)
            print("🌈 Rainbow Mode Activated!")
        if elapsed > 15 and not zombie_mode:
            zombie_mode = True
            print("🧟 Zombie Mode Activated!")

    #Zombie Spread (only if mode active)
    if zombie_mode:
        current_time = pygame.time.get_ticks()
        if current_time - zombie_timer > zombie_interval:
            spread_zombies()
            zombie_timer = current_time

    #Drawing
    screen.fill((255, 255, 255))
    draw_grid(screen)
    draw_palette(screen)

    #Rainbow message
    if rainbow_mode and rainbow_start_time:
        elapsed = (pygame.time.get_ticks() - rainbow_start_time) / 1000
        fade_duration = 5
        if elapsed < fade_duration:
            alpha = max(0, 255 - int((elapsed/fade_duration) * 255))
            text_surface = prank_text.copy()
            text_surface.set_alpha(alpha)
            text_rect = text_surface.get_rect(midtop=(CANVAS_WIDTH//2, 20))
            screen.blit(text_surface, text_rect)




    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
