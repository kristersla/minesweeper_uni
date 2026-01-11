import subprocess
import pygame
from board import Board
from start_screen import Start_Screen
import json
import time

pygame.init()
pygame.display.set_caption('Minesweeper')
icon = pygame.image.load(r"images\icon.png")
pygame.display.set_icon(icon)

with open('resx.json', 'r') as f:
    data2 = json.load(f)

screen = pygame.display.set_mode((int(data2['width']), int(data2['width'])))
background_image = pygame.image.load('background3.png').convert()

# Scale the background image to the size of the display screen
background_image = pygame.transform.scale(background_image, screen.get_size())

screen.blit(background_image, [0, 0])

font = pygame.font.Font('Jolana.ttf', 50)
text_surface = font.render('Loading...', True, (255, 255, 255))
text_rect = text_surface.get_rect(center=screen.get_rect().center)
screen.blit(text_surface, text_rect)

pygame.display.flip()

# Start test.py as a separate process
# subprocess.Popen(['python', 'music.py'])

s = Start_Screen()
while s.running:
    pygame.display.set_caption('Minesweaper')
    icon = pygame.image.load(r"images\icon.png")
    pygame.display.set_icon(icon)
    s.lose.display_menu()
    s.game_loop()
