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
        #self.live = 30
        self.count = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
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
        # FIXME
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
        global balls, bullet, is_ball
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
        # FIXIT don't know how to do it
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


class Target:
    
    def __init__(self):
        self.points = 0
        self.live = 1
        # FIXME: don't work!!! How to call this functions when object is created?
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        vx = self.vx = rnd(-5, 5)
        vy = self.vy = rnd(-5, 5)
        color = self.color = choice(GAME_COLORS)
        self.live = 1
        
    def move(self):
        if self.y >= 600 - self.r:
            self.vy = -self.vy
            self.y = 600 - self.r
        if self.y <= self.r:
            self.vy = -self.vy
            self.y = self.r
        if self.x >= 800 - self.r:
            self.vx = -self.vx
            self.x = 800 - self.r
        if self.x <= self.r:
            self.vx = -self.vx
            self.x = self.r
        self.x += self.vx
        self.y += self.vy     

    def hit(self, points=1):
        """Попадание шарика в цель."""
        global counter
        self.points += points
        counter += 1

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)
        
   
class Fast_Target(Target):
    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        vx = self.vx = rnd(-5, 5)
        vy = self.vy = rnd(-5, 5)
        color = self.color = choice(GAME_COLORS)        
        self.live = 1
        self.t = 0
    def move(self):
        if self.t >= 10:
            self.vy = rnd(-10, 10)
            self.vx = rnd(-10, 10)
            self.t = 0
        if self.y >= 600 - self.r:
            self.vy = -self.vy
            self.y = 600 - self.r
        if self.y <= self.r:
            self.vy = -self.vy
            self.y = self.r
        if self.x >= 800 - self.r:
            self.vx = -self.vx
            self.x = 800 - self.r
        if self.x <= self.r:
            self.vx = -self.vx
            self.x = self.r
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.t = self.t + 1
        
        
class Bomb():
    def __init__(self):
        self.screen = screen
        self.color = BLACK
        self.vy = rnd(0, 5)
        self.y = 0
        self.r = 10
        self.x = rnd(50, 750)
        
    def new_bomb(self):
        self.x = rnd(50, 750)
        self.y = 10
        self.vy = rnd(0, 5)
        self.r = 10
    
    def move(self):
        g = 0.5  
        self.vy = self.vy + g
        self.y = self.y + self.vy
    
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)
        
    def reborn(self):
        if self.y >= 600:
            return True
        else:
            return False
        
    def detonation(self, obj):
        d = (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2
        if d <= (self.r + 5) ** 2:
            return True
        else:
            return False
        
        
def board():
    pass
                

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
bombs = []
counter = 0
is_ball = True

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target()
target2 = Fast_Target()
bomb1 = Bomb()
bomb2 = Bomb()
bombs.append(bomb1)
bombs.append(bomb2)
finished = False
f = pygame.font.Font(None, 30)

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target1.move()
    target2.move()
    target1.draw()
    target2.draw()
    text1 = f.render(str(counter), True, (0, 0, 0))
    text2 = f.render(str(bullet), True, (0, 0, 0))
    screen.blit(text1, (10, 10))
    screen.blit(text2, (50, 10))
    for b in balls:
        b.draw()
    for b in bombs:
        if b.reborn():
            b.new_bomb()
        b.move()
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        if pygame.key.get_pressed()[K_d]:
            gun.move(1)
        if pygame.key.get_pressed()[K_a]:
            gun.move(2)
        if pygame.key.get_pressed()[K_s]:
            gun.move(3)
        if pygame.key.get_pressed()[K_w]:
            gun.move(4)

    for b in balls:
        b.move()
        if b.hittest(target1) and target1.live:
            target1.live = 0
            target1.hit()
            target1.new_target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()
    for b in balls[:]:
        if b.count >= 5:
            balls.remove(b)
    gun.power_up()
    for b in bombs:
        if b.detonation(gun):
            text = f.render('You are died. Your score: ' + str(counter - bullet), True, (0, 0, 0))
            screen.blit(text, (250, 300))
            bullet = 0
            counter = 0            
            pygame.display.update()
            pygame.time.wait(10000)

pygame.quit()
