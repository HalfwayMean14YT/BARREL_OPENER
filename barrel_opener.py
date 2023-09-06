import pygame
import pygame_gui
import os
import pygame.freetype

WIDTH = 1000
HEIGHT = 1000

path = os.path.dirname(os.path.abspath(__file__))

pygame.freetype.init()
manager = pygame_gui.UIManager((WIDTH, HEIGHT), path + '/themeing.json')

def main(running: bool):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    while running:
        background = pygame.Surface(screen.get_size())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()