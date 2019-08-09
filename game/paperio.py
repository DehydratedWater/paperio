import pygame
from pygame.locals import *
from sys import exit
from game.player import Player
from game.tools import *

screen_size = (1280, 720)
screen_center = (screen_size[0]/2, screen_size[1]/2)


player = Player()
pygame.init()
screen = pygame.display.set_mode((screen_size[0], screen_size[1]), 0, 32)

mouse_pos = screen_center
angle = 0
direction = (0, 0)
clock = pygame.time.Clock()
while True:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEMOTION:  # if mouse click then coordinate array will append x,y tuple
            mouse_pos = event.pos
            angle = get_angle(screen_center, mouse_pos)
            direction = normalise_vector(get_vector(screen_center, mouse_pos))

    screen.fill((255, 255, 255))
    screen.lock()
    player.move_player(angle, direction, dt)
    player.draw(screen, screen_center)
    player.check_collisions()
    screen.unlock()
    pygame.display.update()