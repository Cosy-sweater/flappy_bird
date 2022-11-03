import sys
import pygame
import time
import random
import pygame_menu
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 680
screen = pygame.display.set_mode((width, height))

settings = {
    "dist": 100,
    "hitbox": False
}


class Bird(pygame.sprite.Sprite):
    def __init__(self, settings):
        super().__init__()
        self.image = pygame.image.load("img/bird.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 0.1)
        self.rect = self.image.get_rect()
        self.rect.width = 68
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.surface.fill((255, 0, 0))
        self.rect.center = (120, 50)
        self.y_vel = 0

        self.settings = settings

    def draw(self):
        if self.settings["hitbox"]:
            screen.blit(self.surface, self.rect)
        screen.blit(self.image, (self.rect.x - 14, self.rect.y))

    def gravity(self):
        if self.rect.bottom >= height:
            self.rect.bottom = height - 1
            self.y_vel = -8
        elif self.rect.top <= 0:
            self.y_vel = 8
        elif self.y_vel < 16:
            self.y_vel += 0.8
        self.rect.move_ip(0, self.y_vel)

    def jump(self):
        self.y_vel = -12

    def get_rect(self):
        return self.rect


class Pipes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 5
        self.pipe_img1 = pygame.image.load("img/pipe_top.png")
        self.pipe_img2 = pygame.image.load("img/pipe_bottom.png")

        self.pipe_img1 = pygame.transform.rotozoom(self.pipe_img1, 0, 0.4)
        self.pipe_img2 = pygame.transform.rotozoom(self.pipe_img2, 0, 0.4)
        self.rect1 = self.pipe_img1.get_rect()
        self.rect2 = self.pipe_img2.get_rect()

        self.rect1.center = (740, 50)
        self.rect2.center = (740, 50)

        self.cord = random.randint(120, 560)
        self.rect1.bottom = self.cord - settings["dist"]
        self.rect2.top = self.cord + settings["dist"]

    def draw(self):
        screen.blit(self.pipe_img1, self.rect1)
        screen.blit(self.pipe_img2, self.rect2)

    def move(self, bird):
        self.rect1.move_ip(-self.speed, 0)
        self.rect2.move_ip(-self.speed, 0)
        if self.rect1.colliderect(bird) or self.rect2.colliderect(bird):
            return 1


def start_game():
    t = time.time()
    game_loop, update = True, False
    bird = Bird(settings)
    pipes = []
    score = 0

    pipe_event = pygame.USEREVENT + 1
    pygame.time.set_timer(pipe_event, 1500)

    # Game loop.
    while game_loop:
        screen.fill((107, 180, 214))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
            if event.type == pipe_event:
                pipes.append(Pipes())
                score += 1

        # Update.
        if time.time() > t + 1 or update:
            update = True
            bird.gravity()
            collisions = [i.move(bird.get_rect()) for i in pipes]
            if 1 in collisions:
                game_loop = False
        else:
            pipes.clear()
            continue
        # Draw.
        bird.draw()
        [i.draw() for i in pipes]

        pygame.display.flip()
        fpsClock.tick(fps)


def set_difficulty(_, hitbox):
    settings["hitbox"] = hitbox


def start_the_game():
    # Do the job here !
    pass


def set_range(n):
    settings["dist"] = int(n)


menu = pygame_menu.Menu('Настройки', width, height,
                        theme=pygame_menu.themes.THEME_GREEN)

menu.add.range_slider(f'Зазор между трубами', default=100, range_values=[80, 200], increment=10,
                      value_format=lambda n: str(int(n)), onchange=set_range)

menu.add.selector('Хитбоксы:', [('да', 1), ('нет', 0)], onchange=set_difficulty, default=1)
menu.add.button('Играть', start_game)
menu.mainloop(screen)