import pygame
from pygame.draw import *
import numpy as np

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 600))

#background - grass and sky respectively
rect(screen, (152, 251, 152), (0, 300, 1000, 300), 0) 
rect(screen, (176, 224, 230), (0, 0, 1000, 300), 0)


def man(x, y, f):
    
    '''Function draw a man. 
    x, y are coordinates of the center of head of man,
    f show orientation of mans legs'''
    
    x = x - 40
    y = y - 35
    #man: body
    ellipse(screen, (147, 112, 219), (x - 10, y + 40, 100, 200))
    #man: head
    ellipse(screen, (255, 228, 196), (x, y, 80, 70))
    #man: arms
    line(screen, (0, 0, 0), (x + 5, y + 75), (x - 60, y + 180))
    line(screen, (0, 0, 0), (x + 75, y + 75), (x + 130, y + 180))   
    #man:legs
    if f == 1:
        line(screen, (0, 0, 0), (x + 75, y + 210), (x + 90, y + 360))
        line(screen, (0, 0, 0), (x + 5, y + 210), (x - 50, y + 360))
        line(screen, (0, 0, 0), (x - 80, y + 365), (x - 50, y + 360)) 
        line(screen, (0, 0, 0), (x + 90, y + 360), (x + 125, y + 360))
    else:
        line(screen, (0, 0, 0), (x - 75 + 80, y + 210), (x - 90 + 80, y + 360))
        line(screen, (0, 0, 0), (x - 5 + 80, y + 210), (x + 50 + 80, y + 360))
        line(screen, (0, 0, 0), (x + 80 + 80, y + 365), (x + 50 + 80, y + 360))
        line(screen, (0, 0, 0), (x - 90 + 80, y + 360), (x - 125 + 80, y + 360))

def woman(x, y, f, g):
    
    '''Function draw a man. x, y are coordinates of the center of head of woman,
    f shows orientation of woman, if f == 1 left arm is up, if f != 1 right arm is up,
    g shows orientation of womans legs'''
    
    x = x - 40
    y = y - 35
    #woman: body
    polygon(screen, (255, 105, 180), [(x + 40, y + 30), (x - 20, y + 240), (x + 100, y + 240)])
    #woman:head
    ellipse(screen, (255, 228, 196), (x, y, 80, 70))
    #woman: arms
    if f == 1:
        #arm straight
        line(screen, (0, 0, 0), (x + 30, y + 80), (x - 30, y + 180))
        #arm curved
        line(screen, (0, 0, 0), (x + 50, y + 80),(x + 110, y + 140))
        line(screen, (0, 0, 0), (x + 130, y + 60),(x + 110, y + 140))
    else:
        #arm straight
        line(screen, (0, 0, 0), (x + 50, y + 80), (x + 110, y + 180))
        #arm curved
        line(screen, (0, 0, 0), (x + 30, y + 80), (x - 30, y + 140))
        line(screen, (0, 0, 0), (x - 50, y + 60), (x - 30, y + 140))
    #woman:legs
    if g == 1:
        line(screen, (0, 0, 0), (x + 10, y + 240), (x - 5, y + 360))
        line(screen, (0, 0, 0), (x + 65, y + 240), (x + 100, y + 360))
        line(screen, (0, 0, 0), (x - 30, y + 365), (x - 5, y + 360))
        line(screen, (0, 0, 0), (x + 100, y + 360), (x + 125, y + 365))
    else:
        line(screen, (0, 0, 0), (x - 10 + 80, y + 240), (x + 5 + 80, y + 360))
        line(screen, (0, 0, 0), (x - 65 + 80, y + 240), (x - 100 + 80, y + 360))
        line(screen, (0, 0, 0), (x + 30 + 80, y + 365), (x + 5 + 80, y + 360))
        line(screen, (0, 0, 0), (x - 100 + 80, y + 360), (x - 125 + 80, y + 365))        

def heart(x, y, s):
    
    '''Function draw a baloon with shape of heart. x, y  are coordinates of bottem part of baloon,
    s is a scale coefficient'''
    
    #heart
    polygon(screen, (255, 0, 0), [(x, y), (x + s * 33 , y - np.abs(s) * 32), (x - s * 20, y - np.abs(s) * 40)])
    circle(screen, (255, 0, 0), (x - s * 5, y - np.abs(s) * 40), np.abs(s) * 15)
    circle(screen, (255, 0, 0), (x + s * 20, y - np.abs(s) * 37), np.abs(s) * 15)
    #line
    line(screen, (0 ,0 ,0), (x, y), (x - s * 20, y + np.abs(s) * 70))

def icecream(x, y, s):
    
    '''Function draw an icecream which consist of cone and three balls.
    x, y are coordinates of corner of cone of icecream,
    s is a scale coefficient'''
    
    #cone
    polygon(screen, (218, 165, 32), [(x + s * 20, y), (x + s * 40, y - np.abs(s) * 20),(x + s * 20, y - np.abs(s) * 40)])
    #red ball
    ellipse(screen, (220, 20, 60), (x + s * 30, y - np.abs(s) * 35 ,s * 18, np.abs(s) * 16))
    #brown ball
    ellipse(screen, (129, 49, 9), (x + s * 14 , y - np.abs(s) * 45, s * 22, np.abs(s) * 20))
    #white ball
    ellipse(screen, (255, 248, 220), (x + s * 29, y - np.abs(s) * 52, s * 23, np.abs(s) * 20))



man(250, 195, 1)
man(760, 195, 0)
woman(410, 195, 1 , 1)
woman(590, 195, 0, 1)
heart(114, 205, -2)
icecream(820, 345, 1.5)
icecream(540, 140, -2.5)
line(screen,(0, 0, 0),(490, 140),(500, 220))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()