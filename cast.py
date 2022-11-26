import pygame
import random
from math import *

BLACK = (0,0,0)
WHITE = (255,255,255)

SKY = (40,100,200)
GROUND = (200,200,100)

colors = [
    (0,20,10),
    (4,40,63),
    (0,91,82),
    (219,248,38),
    (2,248,50),
]

walls = {
    '1': pygame.image.load('./walls/wall1.png'),
    '2': pygame.image.load('./walls/wall1.png'),
    '3': pygame.image.load('./walls/wall1.png'),
    '4': pygame.image.load('./walls/wall1.png'),
    '5': pygame.image.load('./walls/wall1.png'),
}

class Raycaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.heihgt= screen.get_rect()
        self.blocksize = 50
        self.map = []
        self.player = {
            'x': int(self.blocksize + self.blocksize / 2),
            'y': int(self.blocksize + self.blocksize / 2),
            'fov': int(pi/3),
            'a': int(pi/3),
        }

    def point(self, x, y, c=WHITE):
        self.screen.set_at((x,y),c)

    def block(self, x,y, wall):
        for i in range(x,x + self.blocksize):
            for j in range(y,y + self.blocksize):
                tx = int((i - x) * 128 / self.blocksize)
                ty = int((j - y) * 128 / self.blocksize)
                c = wall.get_at((tx,ty))
                self.point(i,j,c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def draw_stake(self,x,h,c,tx):
        start_y = int(self.heihgt/2 - h/2)
        end_y = int(self.heihgt/2 + h/2)
        height = end_y - start_y

        for y in range(start_y,end_y):
            ty = int((y-start_y) * 128 / height)
            color = walls[c].get_at((tx,ty))
            self.point(x,y,color)

    def cast_ray(self, a):
        d = 0
        ox = self.player['x']
        oy = self.player['y']
        
        while True:
            x = int(ox + d * cos(a))
            y = int(oy + d * sin(a))

            i = int(x / self.blocksize)
            j = int(y / self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x -i*self.blocksize
                hity = y -j*self.blocksize

                if 1 < hitx < self.blocksize - 1:
                    maxhit = hitx
                else:
                    maxhit = hity

                tx = int(maxhit * 128 / self.blocksize)
                return d, self.map[j][i], tx

            self.point(x,y)
            d += 1
    
    def draw_map(self):
        for x in range(0,500,self.blocksize):
            for y in range(0,500,self.blocksize):
                i = int(x / self.blocksize)
                j = int(y / self.blocksize)
                if self.map[j][i] != ' ':
                    self.block(x,y, walls[self.map[j][i]])
    
    def draw_player(self):
        self.point(self.player['x'],self.player['y'])
    
    def render(self):
        self.draw_map()
        self.draw_player()

        density = 100
        #minimapa
        for i in range(0,density):
            a = self.player['a'] - self.player['fov']/2 + self.player['fov'] * i/density
            d,c, _ = self.cast_ray(a)
        #line
        for i in range(0,500):
            self.point(499,i)
            self.point(500,i)
            self.point(501,i)

        #draw in 3d
        for i in range(0,int(self.width/2)):
            a = self.player['a'] - self.player['fov']/2 + self.player['fov'] * i/(self.width/2)
            d,c,tx = self.cast_ray(a)

            x = int(self.width/2) + i
            h = self.heihgt/(d * cos(a - self.player['a'])) * self.heihgt /10

        
            self.draw_stake(x,h,c,tx)


pygame.init()
screen = pygame.display.set_mode((1000,500))
r = Raycaster(screen)
r.load_map('./map.txt')

running = True
while running:
    screen.fill(BLACK,(0,0,r.width,r.heihgt))
    screen.fill(SKY,(r.width/2,0,r.width,r.heihgt/2))
    screen.fill(GROUND, (r.width/2,r.heihgt/2,r.width,r.heihgt/2))
    r.render()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                r.player['a'] -= pi/10
            if event.key == pygame.K_d:
                r.player['a'] += pi/10

            if event.key == pygame.K_RIGHT:
                r.player['x'] += 10
            if event.key == pygame.K_LEFT:
                r.player['x'] -= 10
            if event.key == pygame.K_UP:
                r.player['y'] -= 10
            if event.key == pygame.K_DOWN:
                r.player['y'] += 10