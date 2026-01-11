import pygame
import os
from menu import *
# from game import Game               
# from board import Board             


class Start_Screen():


    def __init__(self):

        with open('jsons/resx.json',  'r') as f:
            data2 = json.load(f)

        pygame.init()
        self.current_track = None
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = int(data2['width']), int(data2['width'])
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE, self.green = (0, 0, 0), (255, 255, 255), (0, 255, 0)
        self.main_menu = MainMenu(self)
        self.stardif = StartGame(self)
        self.secredit = DiffucltyGame(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.custom = Custom(self)
        self.prob = Prob(self)
        self.size = Size(self)
        self.resw = ResWidth(self)
        self.win = Win(self)
        self.lose = Lose(self)
        self.resolution = Resolution(self)
        # self.custplay = CustomPlay(self)
        self.curr_menu = self.main_menu
        self.lost_menu = self.main_menu
        self.play_music("music/menu.mp3")




    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:                                                
                self.playing= False
 

    


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def play_music(self, track):
        if self.current_track == track:
            return
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)
        self.current_track = track

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font('fonts/Jolana.ttf', size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)