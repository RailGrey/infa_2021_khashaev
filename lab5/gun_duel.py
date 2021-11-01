import math
from random import randrange as rnd, choice

import pygame
from pygame.locals import *
from pygame import time


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.count = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        g = 1
        if self.y >= 600 - self.r:
            self.vy = round(-self.vy * 0.7)
            self.vx = round(self.vx * 0.7)
            self.y = 600 - self.r
            self.count += 1
        if self.x >= 800 - self.r:
            self.vx = round(-self.vx * 0.7)
            self.vy = round(self.vy * 0.7)
            self.x = 800 - self.r
            self.count += 1
        self.vy = self.vy + g        
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        d = (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2
        if d <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Square(Ball):        
    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x - self.r / 2, self.y - self.r / 2, 2 * self.r, 2 * self.r))
        

class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.v = 2
        self.x = 50
        self.y = 450
        
    def new_gun(self, x, y):
        self.x = x
        self.y = y
        
    def move(self, n):
        if n == 1:
            self.x = self.x + self.v
        elif n == 2:
            self.x = self.x - self.v
        elif n == 3:
            self.y = self.y + self.v
        elif n == 4:
            self.y = self.y - self.v

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, is_ball, r
        r = r + 1
        r = r % 2
        if event.button == 1:
            is_ball = True
            bullet += 1
        else:
            is_ball = False
            bullet += 2
        if is_ball:
            new_ball = Ball(self.screen, self.x, self.y)
        else:
            new_ball = Square(self.screen, self.x, self.y)
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        if is_ball:
            k = 0.5
        else:
            k = 1
        new_ball.vx = k * self.f2_power * math.cos(self.an)
        new_ball.vy = k * self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2(event.pos[1] - self.y, event.pos[0] - self.x)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(screen, self.color, (self.x, self.y),
                         (self.x + math.cos(self.an) * self.f2_power,
                          self.y + math.sin(self.an) * self.f2_power),
                          10)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
            
    def hittest(self, obj):
        d = (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2
        if d <= (obj.r + 3) ** 2:
            return True
        else:
            return False


      
        
                

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
r = 0 #number of player
balls = []
guns = []
counter = 0

clock = pygame.time.Clock()
gun1 = Gun(screen)
gun1.new_gun(100, 550)
gun2 = Gun(screen)
gun2.new_gun(700, 550)
guns.append(gun1)
guns.append(gun2)
finished = False
f = pygame.font.Font(None, 30)

while not finished:
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (400, 0), (400, 600))
    gun1.draw()
    gun2.draw()
    for b in balls:
        b.move()
        b.draw()
        if guns[r].hittest(b):
            text = f.render('Player ' + str((r + 1) % 2 + 1) + ' win!', True, (0, 0, 0))
            screen.blit(text, (330, 300))
            pygame.display.update()
            finished = True
            pygame.time.wait(5000) 
    for b in balls[:]:
        if b.count >= 1:
            balls.remove(b)     
    pygame.display.update()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            guns[r].fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            guns[r].fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            guns[r].targetting(event)
        if pygame.key.get_pressed()[K_d]:
            guns[r].move(1)
        if pygame.key.get_pressed()[K_a]:
            guns[r].move(2)
        if pygame.key.get_pressed()[K_s]:
            guns[r].move(3)
        if pygame.key.get_pressed()[K_w]:
            guns[r].move(4)
    guns[r].power_up()                  

    

pygame.quit()
