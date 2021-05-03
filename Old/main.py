import math
import os
import pygame

class Node():
    def __init__(self,name,x = 0,y = 0,isEntry = False,isOutput = False):
        self.transitions = []
        self.isEntry = isEntry
        self.isOutput = isOutput
        self.position = (x,y)
        self.name_position = (x-12,y-12)
        self.name = name
        self.name_render = font.render(name,25,(0,0,0))
        self.selected = False

    def display(self):
        if self.selected:
            pygame.draw.rect(screen,(255,0,0),(self.position[0]-50,self.position[1]-50,100,100),5)
        pygame.draw.circle(screen,(0,0,0),self.position,50,5)
        screen.blit(self.name_render,self.name_position)

    def move(self,x,y):
        self.position = (x,y)

class Automaton():
    def __init__(self,states = []):
        self.states = states
        self.isDet = False
        self.isStandard = False

    def display(self):
        for state in self.states:
            state.display()

def draw_arrow(screen, color, start, end, width = 2):
    pygame.draw.line(screen,color,start,end,width)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    pygame.draw.polygon(screen, color, ((end[0]+20*math.sin(math.radians(rotation)), end[1]+20*math.cos(math.radians(rotation))), (end[0]+20*math.sin(math.radians(rotation-120)), end[1]+20*math.cos(math.radians(rotation-120))), (end[0]+20*math.sin(math.radians(rotation+120)), end[1]+20*math.cos(math.radians(rotation+120)))))

pygame.init()

screenx = 1240
screeny = 720
screen = pygame.display.set_mode((screenx,screeny))
font_text=pygame.font.Font(None, 24)
font=pygame.font.Font(None, 50)

test = Node('1',150,150,True)
test2 = Node('2',300,150,True)
test3 = Node('3',150,300,False,True)

auto = Automaton([test,test2])

a = True

textx = font_text.render('0',3,(49,140,231))
texty = font_text.render('0',3,(49,140,231))


while a:
    screen.fill(color = (255,255,255))
    keys = pygame.key.get_pressed()
    mousepress = pygame.mouse.get_pressed()
    mousedelta = pygame.mouse.get_rel()
    mousepos = pygame.mouse.get_pos()
    textx = font_text.render(str(mousepos[0]),3,(49,140,231))
    texty = font_text.render(str(mousepos[1]),3,(49,140,231))
    screen.blit(textx, (10, 10))
    screen.blit(texty, (10, 25))
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
    draw_arrow(screen, (0,0,0),(200,150),(210,150),5)
    auto.display()
    pygame.display.update()
