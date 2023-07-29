import random

import pygame

width = 800
height = 900

O = [['.....',
      '.00..',
      '.00..',
      '.....',
      '.....']]

I = [['.....',
      '.0...',
      '.0...',
      '.0...',
      '.0...'],
      ['.....',
      '.0000',
      '.....',
      '.....'
      '.....']]

S = [['.....',
      '..00.',
      '.00..',
      '.....',
      '.....'],
      ['.0...',
      '.00..',
      '..0..'
      '.....'
      '......']]

Z = [['.....',
      '.00..',
      '..00.',
      '.....',
      '.....'],
     ['.....',
      '...0.',
      '..00.',
      '..0..'
      '.....']]

L = [['.....',
      '.0...',
      '.0...',
      '.00..',
      '.....'],
     ['.....',
      '.000.',
      '.0...',
      '.....',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '...0.',
      '...0.',
      '..00.',
      '......']]

J = [['.....',
      '...0.',
      '...0.',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.0...',
      '.000.'],
     ['.....',
      '.00..',
      '.0...',
      '.0...',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....']]

T = [['.....',
      '.000.',
      '..0..',
      '.....',
      '.....'],
     ['.....',
      '...0.',
      '..00.',
      '...0.',
      '.....',],
     ['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '.0...',
      '.00..',
      '.0...'
      '.....']]


shapes =[S,I,J,Z,O,L,T]
shape_colors = [(0,255,0), (255,0,0), (0,255,255), (255, 255,0), (255,165,0), (0,0,255), (128,0,128)]
pygame.font.init()

class piece(object):
    def __init__(self,x,y,shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0



def draw_next_shape(window):
    font = pygame.font.SysFont("consolas", 30, bold=False)
    label = font.render("Next Shape", 1, (255,255,255))
    window.blit(label, (350, 400))

def draw_text_middle(window):
    font = pygame.font.SysFont("consolas", 30, bold=False)
    label = font.render("Ready", 1, (255,255,255))
    window.blit(label, (350, 400))

def create_grid(locked_positions  = {}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j,i)]

    return grid

def get_piece():
    return piece(5,0,random.choice(shapes))

blocksize =30
rocksize = 15


def draw_grid(window, grid):


    for i in range(len(grid)):
        pygame.draw.line(window,
                         (255,255,255),
                         (250,100 + i * blocksize),
                         (550,100 + i * blocksize))


        for j in range(len(grid[i])):
            pygame.draw.line(window,
                         (255,255,255),
                         (250 + j * blocksize,100),
                         (250 + j * blocksize,700))

def draw_shape(piece):

    shape = piece.shape

    rotation = piece.rotation

    format = shape[rotation % len(shape)]

    positions = []


    for i in range(len(format)):
        row  = list(format[i])

        for j in range(len(row)):
            if(row[j] == "0"):
                pygame.draw.rect(window,
                                piece.color,
                               (530 + j* blocksize,
                                300 + i * blocksize),
                                 blocksize,
                                 blocksize),

                positions.append((piece.x +j, piece.y + i))
    for i , pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions

def valid_space(shape,grid):
    accepted_pos = []
    for i in range(20):
        subList = []
    for j in range(20):
        if grid[i][j] - (0,0,0):
          subList.append((j,i))

    for sub in subList:
       accepted_pos.append(sub)

    formatted = draw_shape(shape)
     for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False




def draw_window(window, grid):
    window.fill((0,0,42))
    font = pygame.font.SysFont("consolas", 20, bold=False)
    label = font.render("Tetris", 1, (255, 255, 255))
    window.blit(label, (365, 25))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                window,
                grid[i][j],
                (220 + j * blocksize,
                 100 + i * blocksize,
                 blocksize,
                 blocksize)

            )



    pygame.draw.rect(window,
                 (128,128,128),
                 (250,100,300,600),
                 5)
    draw_grid(window, grid)

def main(window):
    locked_position = {}
    grid = create_grid(locked_position)
    current_shape = get_piece()
    next_shape = get_piece()

    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0


    run = True
    while (run):
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/ 1000 > 5:
            level_time = 0

        if level_time > 0.12:
            level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_shape.y += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.K_DOWN:
                if event.type == pygame.K_DOWN:
                    current_shape.y += 1
                if event.key == pygame.K_UP:
                    current_shape.rotation += 1
                if event.key == pygame.K_LEFT:
                    current_shape.x -= 1
                if event.key == pygame.K_RIGHT:
                    current_shape.x += 1
                    if not(valid_space(current_shape, grid)):
                        current_shape.x -= 1
        current_piece_position = draw_shape(current_shape)
        for i in range(len(current_piece_position)):
            x, y = current_piece_position[i]
            if y >= 0:
                grid[y][x] = current_shape.color
        draw_window(window, grid)
        draw_next_shape(window,next_shape)
        pygame.display.update()


def main_menu(window):

    run = True
    while(run):
        window.fill((0, 0, 42))
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