"""
    Universidad del Valle de Guatemala
    José Rodrigo Barrera García
    20807
    Proyecto 3 - DOOM GAME

"""

import pygame
from math import pi, cos, sin, atan2

#Declaramos los colores a utilizar
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LOSE = (90, 30, 5)
GRAY = (136, 136, 136)
BACKGROUND = (190, 190, 190)
INICIO = (255, 0, 0)
WIN = (60, 130, 140)

pygame.init()
gameDisplay = pygame.display.set_mode((1000, 600))

wall1 = pygame.image.load('./Proyecto_3_Utilizadades/wall1.png').convert()
wall2 = pygame.image.load('./Proyecto_3_Utilizadades/wall2.png').convert()
wall3 = pygame.image.load('./Proyecto_3_Utilizadades/wall3.png').convert()
enemy = pygame.image.load('./Proyecto_3_Utilizadades/sprite1.png').convert()
hand = pygame.image.load('./Proyecto_3_Utilizadades/player.png').convert()

#Establecemos el diccionario de texturas a utilizar
textures = {
	"1": wall1,
	"2": wall2,
	"3": wall3,
}

#Establecemos el diccionario de enemigos a utilizar
enemies = [
	{
		"x": 100,
		"y": 150,
		"texture": enemy
	}
]

PLAYER_SIZE = 0.125
CAST_SIZE = 2.56

class Raycaster (object):
    def __init__(self, gameDisplay):
        _, _, self.width, self.height = gameDisplay.get_rect()
        self.gameDisplay = gameDisplay
        self.blocksize = 50
        self.map = []
        self.zbuffer = [-float('inf') for z in range(0, 500)]
        self.player = {
			"x": self.blocksize + 20,
			"y": self.blocksize + 20,
			"a": 0,
			"fov": pi/3
		}

    def point(self, x, y, c=None):
        gameDisplay.set_at((x, y), c)

    def draw_rectangle(self, x, y, texture, size):
        for cx in range(x, x + size):
            for cy in range(y, y + size):
                tx = int((cx - x) * 12.8)
                ty = int((cy - y) * 12.8)
                c = texture.get_at((tx, ty))
                self.point(cx, cy, c)

    def draw_player(self, xi, yi, element, w=256, h=256):
        for x in range(xi, xi + w):
            for y in range(yi, yi + h):
                tx = int((x - xi) * PLAYER_SIZE)
                ty = int((y - yi) * PLAYER_SIZE)
                c = element.get_at((tx, ty))
                if c != (152, 0, 136, 255):
                    self.point(x, y, c)

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def cast_ray(self, a):
        d = 0
        cosa = cos(a)
        sina = sin(a)
        while True:
            x = int(self.player["x"] + d * cosa)
            y = int(self.player["y"] + d * sina)

            i = int(x / self.blocksize)
            j = int(y / self.blocksize)

            if self.map[j][i] != ' ':
                hitx = x - i * 50
                hity = y - j * 50
                if 1 < hitx < 49:
                    maxhit = hitx
                else:
                    maxhit = hity
                tx = int(maxhit * CAST_SIZE)
                return d, self.map[j][i], tx
            d += 1

    def draw_stake(self, x, h, tx, texture):
        h_half = h/2
        start = int(250 - h_half)
        end = int(250 + h_half)
        end_start_pro = 128 / (end - start)
        for y in range(start, end):
            ty = int((y - start) * end_start_pro)
            c = texture.get_at((tx, ty))
            self.point(x, y, c)

    def draw_sprite(self, sprite):
        sprite_a = atan2((sprite["y"] - self.player["y"]),
						 (sprite["x"] - self.player["x"]))
        sprite_d = ((self.player["x"] - sprite["x"]) ** 2 +
					(self.player["y"] - sprite["y"]) ** 2) ** 0.5
        sprite_size_half = int(250/sprite_d * 70)
        sprite_size = sprite_size_half * 2
        sprite_x = int(500 + (sprite_a - self.player["a"]) * 477.46 +
					   250 - sprite_size_half)
        sprite_y = int(250 - sprite_size_half)

        sprite_size_pro = 128/sprite_size
        for x in range(sprite_x, sprite_x + sprite_size):
            for y in range(sprite_y, sprite_y + sprite_size):
                if 500 < x < 1000 and self.zbuffer[x - 500] <= sprite_d:
                    tx = int((x - sprite_x) * sprite_size_pro)
                    ty = int((y - sprite_y) * sprite_size_pro)
                    c = sprite["texture"].get_at((tx, ty))
                    if c != (152, 0, 136, 255):
                        self.point(x, y, c)
                        self.zbuffer[x - 500] = sprite_d

    def render(self):
        for i in range(0, 1000):
            try:
                a = self.player["a"] - self.player["fov"] / \
                    2 + (i * 0.00105)
                d, m, tx = self.cast_ray(a)
                x = i
                h = (500 / (d * cos(a - self.player["a"]))) * 50
                self.draw_stake(x, h, tx, textures[m])
            except:
                self.player["x"] = 70
                self.player["y"] = 70
                self.game_over()

        for enemy in enemies:
            self.point(enemy["x"], enemy["y"], BLACK)
            self.draw_sprite(enemy)
		
        for x in range(0, 100, 10):
            for y in range(0, 100, 10):
                i = int(x * 0.1)
                j = int(y * 0.1)
                if self.map[j][i] != ' ':
                    y = 500 + y
                    x1 = 900 + x
                    self.draw_rectangle(x1, y, textures[self.map[j][i]], 10)

        self.point(int(self.player["x"] * 0.2) + 900, int(self.player["y"] * 0.2) + 500, LOSE)
		
        self.draw_player(466, 244, hand)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, WHITE)
        return textSurface, textSurface.get_rect()
    
    def game_intro(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        intro = False
                        self.game_start()
            gameDisplay.fill(INICIO)
            largeText = pygame.font.Font('freesansbold.ttf', 55)
            mediumText = pygame.font.Font('freesansbold.ttf', 25)
            smallText = pygame.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = self.text_objects(
	        	"DOOM GAME", largeText)
            TextRect.center = (500, 250)
            gameDisplay.blit(TextSurf, TextRect)
            TextSurf, TextRect = self.text_objects(
				"PRESIONE Q PARA EMPEZAR", mediumText)
            TextRect.center = (500, 350)
            gameDisplay.blit(TextSurf, TextRect)
            TextSurf, TextRect = self.text_objects(
				"ESC PARA SALIR", smallText)
            TextRect.center = (500, 450)
            gameDisplay.blit(TextSurf, TextRect)
            pygame.display.update()

    def game_over(self):
        lose_sound = pygame.mixer.Sound('./Proyecto_3_Utilizadades/perder.wav')
        pygame.mixer.Sound.play(lose_sound)
        pygame.mixer.music.stop()
		
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        intro = False
                        self.game_intro()

            gameDisplay.fill(LOSE)
            largeText = pygame.font.Font('freesansbold.ttf', 55)
            mediumText = pygame.font.Font('freesansbold.ttf', 25)
            smallText = pygame.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = self.text_objects(
	        	"PERDISTE EL JUEGO", largeText)
            TextRect.center = (500, 250)
            gameDisplay.blit(TextSurf, TextRect)
            TextSurf, TextRect = self.text_objects(
				"PRESIONE R PARA VOLVER A EMPEZAR", mediumText)
            TextRect.center = (500, 350)
            gameDisplay.blit(TextSurf, TextRect)
            TextSurf, TextRect = self.text_objects(
				"ESC PARA SALIR", smallText)
            TextRect.center = (500, 450)
            gameDisplay.blit(TextSurf, TextRect)
            pygame.display.update()
			

    def game_win(self):
        win_sound = pygame.mixer.Sound('./Proyecto_3_Utilizadades/ganar.wav')
        pygame.mixer.Sound.play(win_sound)
        pygame.mixer.music.stop()
		
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        intro = False
                        self.game_intro()

            gameDisplay.fill(WIN)
            largeText = pygame.font.Font('freesansbold.ttf', 55)
            mediumText = pygame.font.Font('freesansbold.ttf', 25)
            smallText = pygame.font.Font('freesansbold.ttf', 10)
            TextSurf, TextRect = self.text_objects(
	        	"GANASTE EL JUEGO", largeText)
            TextRect.center = (500, 250)
            gameDisplay.blit(TextSurf, TextRect)
            TextSurf, TextRect = self.text_objects(
				"PRESIONE R PARA VOLVER A EMPEZAR", mediumText)
            TextRect.center = (500, 350)
            gameDisplay.blit(TextSurf, TextRect)
            TextSurf, TextRect = self.text_objects(
				"ESC PARA SALIR", smallText)
            TextRect.center = (500, 450)
            gameDisplay.blit(TextSurf, TextRect)
            pygame.display.update()
			

    def sound(self):
        pygame.mixer.music.load('./Proyecto_3_Utilizadades/fondo.wav')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)

    def Update(self):
        fuente = pygame.font.Font(None, 25)
        texto_de_salida = "FPS: " + str(round(clock.get_fps(), 2))
        texto = fuente.render(texto_de_salida, True, WHITE)
        return texto


    def game_start(self):
        paused = False
        running = True
        d = 10
        while running:
            gameDisplay.fill(BACKGROUND)
            if not paused:
                gameDisplay.blit(self.Update(), [600, 550])
                if (r.player["x"] >= 400 and r.player["x"] <= 420) and (r.player["y"] >= 250 and r.player["y"] <= 265):
                    self.game_win() 
                r.render()
                pygame.display.flip()
                clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if not paused:
                        if event.key == pygame.K_LEFT:
                            r.player["x"] -= 0.16
                        if event.key == pygame.K_RIGHT:
                            r.player["x"] += 0.16
                        if event.key == pygame.K_UP:
                            r.player["x"] += int(d * cos(r.player["a"]))
                            r.player["y"] += int(d * sin(r.player["a"]))
                        if event.key == pygame.K_DOWN:
                            r.player["x"] -= int(d * cos(r.player["a"]))
                            r.player["y"] -= int(d * sin(r.player["a"]))
                        if event.key == pygame.K_SPACE:
                            paused = not paused
                        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                            if not paused:
                                if event.button == 4:
                                    r.player['a'] -= 0.16
                                if event.button == 5:
                                    r.player['a'] += 0.16
			


gameDisplay.set_alpha(None)
r = Raycaster(gameDisplay)
r.load_map('./Proyecto_3_Utilizadades/map.txt')
pygame.display.set_caption('Proyecto 3 - DOOM GAME')
clock = pygame.time.Clock()
r.game_intro()