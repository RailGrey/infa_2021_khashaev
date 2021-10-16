import pygame
from pygame.draw import *
from random import randint
pygame.init()

print('Hello! Please enter your name:')
name = input()

FPS = 20
screen = pygame.display.set_mode((1200, 800))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

rect(screen, (255, 255, 255), (50, 50, 1100, 700))

score = 0
check = [6, 6]
x = [0, 0]
y = [0, 0]
r = [0, 0]
vx = [0, 0]
vy = [0, 0]
color = [RED, RED]
maxtime = [10, 10]


def new_ball(a): 
    '''Create a ball 
    x, y coordinates of a ball
    r - radius of a ball
    vx, vy - speed of a ball
    color - colour of a ball
    maxtime - lifetime of a ball'''
    global x, y, r, vx, vy, color, maxtime
    x[a] = randint(150, 1050)
    y[a] = randint(150, 650)
    r[a] = randint(10, 100)
    vx[a] = randint(-5, 5) 
    vy[a] = randint(-5, 5) 
    color[a] = COLORS[randint(0, 5)]
    maxtime[a] = randint(10, 50)
    circle(screen, color[a], (x[a], y[a]), r[a])
    
def move_ball(a):
    global x, y, r, color, vx, vy, maxtime
    if x[a] <= 50 + r[a] or x[a] >= 1150 - r[a]:
        vx[a] = -vx[a]
    if y[a] <= 50 + r[a] or y[a] >= 750 - r[a]:
        vy[a] = -vy[a]
    x[a] = x[a] + vx[a]
    y[a] = y[a] + vy[a]
    circle(screen, color[a], (x[a], y[a]), r[a])
    
x2 = [0, 0]
y2 = [0, 0]
r2 = [0, 0]
vx2 = [0, 0]
vy2 = [0, 0]
color2 = [RED, RED]
maxtime2 = [10, 10]
curent_time = [0, 0]
time_of_motion = [5, 5]
check2 = [6, 6]
time = [0, 0]

    
def new_square(a): 
    '''Create a square
    x2, y2 - coordinates of a square
    r2 - half of lenth of side of square
    vx2, vy2 - speed of a square
    color2 - colour of a square
    maxtime2 - lifetime of a square'''
    global x2, y2, r2, vx2, vy2, color2, maxtime2
    x2[a] = randint(150, 1050)
    y2[a] = randint(150, 650)
    r2[a] = randint(20, 40)
    vx2[a] = randint(-10, 10) 
    vy2[a] = randint(-10, 10) 
    color2[a] = COLORS[randint(0, 5)]
    maxtime2[a] = randint(10, 50)
    time_of_motion[a] = randint(5, 10)
    curent_time[a] = 0
    rect(screen, color2[a], (x2[a], y2[a], r2[a] * 2, r2[a] * 2))
    

def move_square(a):
    global x2, y2, r2, color2, vx2, vy2, maxtime2
    if curent_time[a] >= time_of_motion[a]:
        time_of_motion[a] = randint(5, 10)
        vx2[a] = randint(-15, 15)
        vy2[a] = randint(-15, 15)
        curent_time[a] = 0
    else:
        curent_time[a] = curent_time[a] + 1
    if x2[a] <= 50 or x2[a] >= 1150 - 2 * r2[a]:
        vx2[a] = -vx2[a]
    if y2[a] <= 50 or y2[a] >= 750 - 2 * r2[a]:
        vy2[a] = -vy2[a]
    
    x2[a] = x2[a] + vx2[a]
    y2[a] = y2[a] + vy2[a]
    rect(screen, color2[a], (x2[a], y2[a], 2 * r2[a], 2 * r2[a]))


def board(name, score):
    with open('board.txt', 'r') as board:
        old_board = board.read().split()
    lenth = len(old_board) // 2
    name_of_player = [0 for i in range(lenth)]
    score_of_player = [0 for i in range(lenth)]
    k = -1
    for i in range(lenth):
        name_of_player[i] = old_board[i * 2]
        if name_of_player[i] == name:
            k = i
        score_of_player[i] = int(old_board[i * 2 + 1])
    flag = True
    if k < 0: #if this is a new player
        name_of_player.append(name)
        score_of_player.append(score)
        i = 0
        while score > score_of_player[lenth - 1 - i] and i != lenth:
            score_of_player[lenth - i] = score_of_player[lenth - 1 - i]
            name_of_player[lenth - i] = name_of_player[lenth - 1 - i]
            name_of_player[lenth - 1 - i] = name
            score_of_player[lenth - 1 - i] = score
            i = i + 1
        new_board = ''
        for i in range(lenth + 1):
            new_board = new_board + str(name_of_player[i]) + ' ' + str(score_of_player[i]) + '\n'        
    else:
        if score > score_of_player[k]:
            score_of_player[k] = score
            while score > score_of_player[k - 1] and k != 0:
                score_of_player[k] = score_of_player[k - 1]
                name_of_player[k] = name_of_player[k - 1]
                score_of_player[k - 1] = score
                name_of_player[k - 1] = name
                k = k - 1
        new_board = ''
        for i in range(lenth):
            new_board = new_board + str(name_of_player[i]) + ' ' + str(score_of_player[i]) + '\n'           
    with open('board.txt', 'w') as board:
        board.write(new_board)
        

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print('Your score: ',score)
            board(name, score)
            with open('board.txt', 'r') as board:
                print(board.read())
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(2):
                d2 = (event.pos[0] - x[i]) ** 2 + (event.pos[1] - y[i]) ** 2
                if d2 <= r[i] ** 2:
                    score = score + 1
                    new_ball(i)
            for i in range(2):
                if abs(event.pos[0] - r2[i] - x2[i]) <= r2[i] and abs(event.pos[1] - r2[i] - y2[i]) <= r2[i]:
                    score = score + 2
                    new_square(i)
    for i in range(2):
        if check[i] <= maxtime[i]:
            move_ball(i)
            check[i] = check[i] + 1
        else:
            new_ball(i)
            check[i] = 0
    for i in range(2):
        if check2[i] <= maxtime2[i]:
            move_square(i)
            check2[i] = check2[i] + 1
        else:
            new_square(i)
            check2[i] = 0
    pygame.display.update()
    screen.fill(BLACK)
    rect(screen, (255, 255, 255), (50, 50, 1100, 700))
    rect(screen, (0, 0, 0), (51, 51, 1098, 698))

pygame.quit()