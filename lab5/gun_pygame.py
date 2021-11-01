import math
from random import randrange as rnd, choice

import pygame


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
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
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
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

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


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = 0.5 * self.f2_power * math.cos(self.an)
        new_ball.vy = 0.5 * self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        # FIXIT don't know how to do it
        pygame.draw.line(screen, self.color, (50, 450),
                         (50 + math.cos(self.an) * self.f2_power,
                          450 + math.sin(self.an) * self.f2_power),
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


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
counter = 0

clock = pygame.time.Clock()
gun = Gun(screen)
target1 = Target()
target2 = Target()
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

pygame.quit()
