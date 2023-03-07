import sys
import pygame
import time
import random
import pygame_menu
from pygame.locals import *

pygame.init()
pygame.font.init()
pygame.display.set_caption('Flappy bird')
pygame.display.set_icon(pygame.image.load("img/icon.png"))

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 680
screen = pygame.display.set_mode((width, height))

score = 0

settings = {
    "dist": 100,
    "hitbox": False,
    "del": 1500
}
my_font = pygame.font.SysFont('Comic Sans MS', 30)


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("img/bird.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 0.1)
        self.rect = self.image.get_rect()
        self.rect.width = 68
        self.rect.height -= 10
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.surface.fill((255, 227, 0))
        self.rect.center = (120, 50)
        self.y_vel = 0
        self.rotation = 0
        self.temp_image = None

        self.settings = settings

    def draw(self):
        if self.settings["hitbox"]:
            screen.blit(self.surface, self.rect)
        self.rotation = (self.rotation * 2 + self.y_vel * -1.7) / 3
        self.temp_image = pygame.transform.rotate(self.image, self.rotation)
        screen.blit(self.temp_image, (self.rect.x - 14, self.rect.y - 15))

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
        self.pipe_img1 = pygame.image.load("img/pipe.png")
        self.pipe_img1 = pygame.transform.rotozoom(self.pipe_img1, 0, 0.4)

        self.rect1 = self.pipe_img1.get_rect()
        self.pipe_img2 = pygame.transform.flip(self.pipe_img1, False, True)

        self.rect1 = self.pipe_img1.get_rect()
        self.rect2 = self.pipe_img2.get_rect()

        self.surf = pygame.Surface((self.rect1.width, self.rect1.height))
        self.surf.fill((0, 255, 0))

        self.rect1.center = (740, 50)
        self.rect2.center = (740, 50)

        self.cord = random.randint(120, 560)
        self.rect1.bottom = self.cord - settings["dist"]
        self.rect2.top = self.cord + settings["dist"]

    def draw(self):
        if settings["hitbox"]:
            screen.blit(self.surf, self.rect1)
            screen.blit(self.surf, self.rect2)
        screen.blit(self.pipe_img1, self.rect1)
        screen.blit(self.pipe_img2, self.rect2)

    def move(self, bird):
        self.rect1.move_ip(-self.speed, 0)
        self.rect2.move_ip(-self.speed, 0)
        if self.rect1.colliderect(bird) or self.rect2.colliderect(bird):
            return 1


def start_game():
    global score

    for i in menu.get_widgets():
        i.hide()

    t = time.time()
    game_loop, d = True, False
    bird = Bird()
    pipes = []
    score = -1

    bg_displacement = 0
    bg_image = pygame.image.load("img/bg.jpg")

    pipe_event = pygame.USEREVENT + 1
    pygame.time.set_timer(pipe_event, settings["del"])

    # Game loop.
    while game_loop:
        screen.fill((112, 195, 244))
        bg_displacement -= 2

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.jump()
            if event.type == pipe_event:
                pipes.append(Pipes())
                score += 1
                if d is True and len(pipes) > 6:
                    d = False
                    del pipes[0]
                else:
                    d = True

        # Update.
        if time.time() > t + 1:
            bird.gravity()
            collisions = [i.move(bird.get_rect()) for i in pipes]
            if 1 in collisions:
                game_loop = False
        else:
            pipes.clear()
            continue
        # Draw.
        screen.blit(bg_image, (bg_displacement - 1920, -20))
        screen.blit(bg_image, (bg_displacement, -20))
        bg_displacement %= 1920
        bird.draw()
        [i.draw() for i in pipes]
        if score >= 0:
            text_surface = my_font.render(str(score), False, (0, 0, 0))
        else:
            text_surface = my_font.render("0", False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))

        pygame.display.flip()
        fpsClock.tick(fps)
    transition = pygame.Surface((640, 680))
    for i in range(75):
        screen.blit(transition, (0, i * 12 - 680))
        pygame.display.flip()
        fpsClock.tick(fps * 2)

    for i in menu.get_widgets():
        i.show()


def set_difficulty(_, hitbox):
    settings["hitbox"] = hitbox


def set_range(n):
    settings["dist"] = int(n)


def set_distance(n):
    settings["del"] = int(n)


def reset_settings():
    global settings
    settings = {
        "dist": 100,
        "hitbox": False,
        "del": 1500
    }
    for i in menu.get_widgets():
        i.reset_value()


def update_menu():
    menu_score.set_title(f'Счёт: {score}')


menu = pygame_menu.Menu('Настройки', width, height,
                        theme=pygame_menu.themes.THEME_GREEN)

menu_score = menu.add.label(f'Счёт: {score}')
menu_score.set_title("1")
menu.add.range_slider('Зазор между трубами', default=settings["dist"], range_values=[80, 200], increment=10,
                      value_format=lambda n: str(int(n)), onchange=set_range)
menu.add.range_slider('Расстояние между трубами', default=settings["del"], range_values=[800, 2000], increment=10,
                      value_format=lambda n: str(int(n)), onchange=set_distance)

menu.add.selector('Хитбоксы:', [('да', True), ('нет', False)], onchange=set_difficulty, default=1)
menu.add.button("Сбросить настройки", reset_settings)
menu.add.button('Играть', start_game)
menu.mainloop(screen, update_menu)
