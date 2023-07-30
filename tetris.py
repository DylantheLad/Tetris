import random

import pygame

width = 800
height = 900
blockSize = 30

O = [['.....',
      '.00..',
      '.00..',
      '.....',
      '.....']]

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
L = [['....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
shapes = [S, I ,Z, L, O ,J , T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


pygame.font.init()

def draw_text_middle(window):
    font = pygame.font.SysFont("comicsans", 30, bold=True) 
    label = font.render("ready", 1, (255, 255, 255)) # font
    window.blit(label, (280,300 ))

def create_grid(locked_positions = {}):
    #Create 2D list filled with 5 , row = 100, col=10
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)] # matrix with 10 columns and 20 rows
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c

    return grid

def get_piece():
    return Piece(5, 0, random.choice(shapes))

def draw_grid(window, grid):

    for i in range(len(grid)): # 20 times
        pygame.draw.line(window,
                         (128, 128, 128), #color (RGB)
                         (200, 100 + i * blockSize),
                         # ending position (x,y)
                         (500, 100 + i * blockSize)
                         )
        for j in range(len(grid[i])):
            pygame.draw.line(window,
                             (128, 128, 128),  # color (RGB)
                             (200 + j * blockSize, 100 ),
                             # ending position (x,y)
                             (200 + j * blockSize, 700)
                             )

def draw_shape(piece):

    shape = piece.shape

  
    rotation = piece.rotation

    format = shape[rotation % len(shape)]

    positions = []
    #['.....', '.....', '..00.', '.00..', '.....']
    for i in range(len(format)):
        row = list(format[i])

        for j in range(len(row)):
            if( row[j] == "0"):
                positions.append((piece.x + j, piece.y + i))

    for i , pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def draw_window(window, grid):
    window.fill((0,0,42))
    font = pygame.font.SysFont("consolas", 30, bold=True)  
    label = font.render("Tetris", 1, (255, 255, 255))  # TODO: set color of the font
    window.blit(label, (350, 50))


    for i in range(len(grid)): #row
        for j in range(len(grid[i])): #column
 
            pygame.draw.rect(
                window,
                grid[i][j],
                (200 + j * blockSize,
                 100 + i * blockSize,
                 blockSize,
                 blockSize),
                0
            )

    pygame.draw.rect(window,
                     (128, 128, 128),
                     (200, 100,300, 600),
                      5) 
    draw_grid(window, grid)

def draw_next_shape(window, piece):

    font = pygame.font.SysFont("comicsans", 30, bold=True)  
    label = font.render("Next Shape", 1, (255, 255, 255))  

    shape = piece.shape
    rotation = piece.rotation
    format = shape[rotation % len(shape)]
    for i in range(len(format)):
        row = list(format[i])

        for j in range(len(row)):
            if( row[j] == "0"):
                pygame.draw.rect(window, piece.color, (540 + j * blockSize, 370 + i * blockSize, blockSize, blockSize), 0)
                

    window.blit(label, (550, 350))



def main(window):
    locked_positions = {}
    grid = create_grid(locked_positions)
    current_shape = get_piece()
    next_shape = get_piece()

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0

    run = True
    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_shape.y += 1

            if not valid_space(current_shape, grid) and current_shape.y > 0:
                current_shape.y -= 1
                for pos in draw_shape(current_shape):
                    x, y = pos
                    if y > -1:
                        locked_positions[pos] = current_shape.color
                current_shape = next_shape
                next_shape = get_piece()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    current_shape.y += 1
                    if not valid_space(current_shape, grid):
                        current_shape.y -= 1
                if event.key == pygame.K_UP:
                    current_shape.rotation += 1
                    if not valid_space(current_shape, grid):
                        current_shape.rotation -= 1
                if event.key == pygame.K_LEFT:
                    current_shape.x -= 1
                    if not valid_space(current_shape, grid):
                        current_shape.x += 1
                if event.key == pygame.K_RIGHT:
                    current_shape.x += 1
                    if not valid_space(current_shape, grid):
                        current_shape.x -= 1

        current_piece_position = draw_shape(current_shape)
        for i in range(len(current_piece_position)):
            x, y = current_piece_position[i]
            if 0 <= y <= 19:
                grid[y][x] = current_shape.color

        draw_window(window, grid)
        draw_next_shape(window, next_shape)
        pygame.display.update()

def valid_space(shape, grid):
    accepted_pos = []

    for j in range(10):
        subList = []
        for i in range(20):
            if grid[i][j] == (0, 0, 0):
                subList.append((j, i))

        for sub in subList:
            accepted_pos.append(sub)

    formatted = draw_shape(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False

    return True
        
def main_menu(window):
    run = True
    while(run):
        window.fill((0,0,0))
        draw_text_middle(window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(window)
    pygame.display.quit()



window = pygame.display.set_mode((width, height))
pygame.display.set_caption("tetris")
main_menu(window)

