import pygame
import subprocess              
# from board import Board
from menu import *
import time
import json
import math
import os
from settings import Settings, MULTIPLAYER_SIDEBAR_WIDTH

os.environ["SDL_VIDEO_CENTERED"] = "1"  # Center the window

class Menu():
    def __init__(self, start_screen):
        self.start_screen = start_screen
        self.mid_w, self.mid_h = self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100


    def draw_cursor(self):
        self.start_screen.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.start_screen.window.blit(self.start_screen.display, (0, 0))
        pygame.display.update()
        self.start_screen.reset_keys()


class MainMenu(Menu):

    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.state = "Start game"
        self.titlex, self.titley = self.mid_w, self.mid_h + -100
        self.startx, self.starty = self.mid_w + -15, self.mid_h + 10
        self.multiplayerx, self.multiplayery = self.mid_w, self.mid_h + 70
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 130
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 195
        self.secreditx, self.secredity = self.mid_w, self.mid_h + 10
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))
        self.title_size = 50

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            self.check_input()
            self.start_screen.display.blit(self.background, (0, 0))
            title_font_size = int(self.title_size)
            title_font = pygame.font.Font(None, title_font_size)
            title_text = title_font.render('Minesweeper', True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.titlex, self.titley))
            self.start_screen.display.blit(title_text, title_rect)
            self.start_screen.draw_text("Start game", 40, self.secreditx, self.secredity)
            self.start_screen.draw_text("Multiplayer", 40, self.multiplayerx, self.multiplayery)
            self.start_screen.draw_text("Options", 40, self.optionsx, self.optionsy)
            self.draw_cursor()
            self.blit_screen()

            # Update title_size to zoom the Minesweeper text
            self.title_size = 80 + 10 * abs(math.sin(pygame.time.get_ticks() / 400))


    def move_cursor(self):
        if self.start_screen.DOWN_KEY:
            if self.state == 'Start game':
                self.cursor_rect.midtop = (
                    self.multiplayerx + self.offset,
                    self.multiplayery,
                )
                self.state = 'Multiplayer'
            elif self.state == 'Multiplayer':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.secreditx + self.offset, self.secredity)
                self.state = 'Start game'

        elif self.start_screen.UP_KEY:
            if self.state == 'Options':
                self.cursor_rect.midtop = (
                    self.multiplayerx + self.offset,
                    self.multiplayery,
                )
                self.state = 'Multiplayer'
            elif self.state == 'Multiplayer':
                self.cursor_rect.midtop = (self.secreditx + self.offset, self.secredity)
                self.state = 'Start game'
            elif self.state == 'Start game':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'


    def check_input(self):
        self.move_cursor()
        if self.start_screen.START_KEY:
            if self.state == 'Start game':
                self.start_screen.curr_menu = self.start_screen.stardif
            elif self.state == 'Multiplayer':
                self.start_screen.curr_menu = self.start_screen.multiplayer_menu
            elif self.state == 'Options':
                self.start_screen.curr_menu = self.start_screen.options
            self.run_display = False

           
class OptionsMenu(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.state = 'Resolution'
        self.sizex, self.sizey = self.mid_w, self.mid_h - 10
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.sizex + self.offset, self.sizey)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            self.check_input()
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text('Options', 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 100)
            self.start_screen.draw_text("Resolution", 35, self.sizex, self.sizey)
            self.start_screen.draw_text("Credits", 35, self.creditsx, self.creditsy)


            self.draw_cursor()
            self.blit_screen()
 
    def check_input(self):
        if self.start_screen.BACK_KEY:
            self.start_screen.curr_menu = self.start_screen.main_menu
            self.run_display = False
        elif self.start_screen.DOWN_KEY:
            if self.state == 'Resolution':
                self.state = 'Credits'
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
            elif self.state == 'Credits':
                self.state = 'Resolution'
                self.cursor_rect.midtop = (self.sizex + self.offset, self.sizey)

        elif self.start_screen.UP_KEY:
            if self.state == 'Credits':
                self.state = 'Resolution'
                self.cursor_rect.midtop = (self.sizex + self.offset, self.sizey)
            elif self.state == 'Resolution':
                self.state = 'Credits'
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)

                
        elif self.start_screen.START_KEY:
            if self.state == 'Resolution':

                self.start_screen.curr_menu = self.start_screen.resolution
                self.run_display = False
      
            elif self.state == 'Credits':

                self.start_screen.curr_menu = self.start_screen.credits
                self.run_display = False
            
                   

class CreditsMenu(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            if self.start_screen.START_KEY or self.start_screen.BACK_KEY:
                self.start_screen.curr_menu = self.start_screen.options
                self.run_display = False
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text('Credits', 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 70)
            self.start_screen.draw_text('Made by Kristers, Liva and Anna', 37, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 + 10)
            self.blit_screen()

class DiffucltyGame(Menu):
    
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.state = 'Beginner'
        self.volx, self.voly = self.mid_w, self.mid_h - 30
        self.Difficultyx, self.Difficultyy = self.mid_w, self.mid_h + 20
        self.sizex, self.sizey = self.mid_w, self.mid_h + 220
        self.beginnerx, self.beginnery = self.mid_w, self.mid_h - 80
        self.mediumx, self.mediumy = self.mid_w, self.mid_h + 80
        self.hardx, self.hardy = self.mid_w, self.mid_h + 70
        self.impossiblex, self.impossibley = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.beginnerx + self.offset, self.beginnery)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            self.check_input()
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text('Options', 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 170)
            self.start_screen.draw_text("Beginner", 35, self.beginnerx, self.beginnery)
            self.start_screen.draw_text("Easy", 35, self.volx, self.voly)
            self.start_screen.draw_text("Medium", 35, self.Difficultyx, self.Difficultyy)
            self.start_screen.draw_text("Hard", 35, self.hardx, self.hardy)
            self.start_screen.draw_text("Impossible", 35, self.impossiblex, self.impossibley)

            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.start_screen.BACK_KEY:
            self.start_screen.curr_menu = self.start_screen.stardif
            self.run_display = False
        elif self.start_screen.DOWN_KEY:
            if self.state == 'Beginner':
                self.state = 'Easy'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
            elif self.state == 'Easy':
                self.state = 'Medium'
                self.cursor_rect.midtop = (self.Difficultyx + self.offset, self.Difficultyy)
            elif self.state == 'Medium':
                self.state = 'Hard'
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
            elif self.state == 'Hard':
                self.state = 'Impossible'
                self.cursor_rect.midtop = (self.impossiblex + self.offset, self.impossibley)
            elif self.state == 'Impossible':
                self.state = 'Beginner'
                self.cursor_rect.midtop = (self.beginnerx + self.offset, self.beginnery)
        elif self.start_screen.UP_KEY:
            if self.state == 'Impossible':
                self.state = 'Hard'
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
            elif self.state == 'Hard':
                self.state = 'Medium'
                self.cursor_rect.midtop = (self.Difficultyx + self.offset, self.Difficultyy)
            elif self.state == 'Medium':
                self.state = 'Easy'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
            elif self.state == 'Easy':
                self.state = 'Beginner'
                self.cursor_rect.midtop = (self.beginnerx + self.offset, self.beginnery)
            elif self.state == 'Beginner':
                self.state = 'Impossible'
                self.cursor_rect.midtop = (self.impossiblex + self.offset, self.impossibley)
                
        elif self.start_screen.START_KEY:
            if self.state == 'Beginner':

                try:
                    prob = 0.1
                    tiles = 4

                    print('entered prob:', prob)
                    print('entered prob:', tiles)
                    with open('jsons/prob.json', 'w') as f:
                        json.dump({'prob': prob}, f)

                    with open('jsons/tiles.json', 'w') as f:
                        json.dump({'tiles': tiles}, f)

                    subprocess.Popen(['python', 'game.py'])
                    pygame.quit()
                    # from game import Game
                    # game = Game()
                    # game.new()
                    # game.run()
                    # self.start_screen.curr_menu = self.start_screen.custom
                    # self.run_display = False
                except ValueError:
                    print('error')

            elif self.state == 'Easy':
                
                try:
                    prob = 0.1
                    tiles = 7
                    print('entered prob:', prob)
                    print('entered prob:', tiles)
                    with open('jsons/prob.json', 'w') as f:
                        json.dump({'prob': prob}, f)

                    with open('jsons/tiles.json', 'w') as f:
                        json.dump({'tiles': tiles}, f)

                    subprocess.Popen(['python', 'game.py'])
                    pygame.quit()
                    # game = Game()
                    # game.new()
                    # game.run()
                    # self.start_screen.curr_menu = self.start_screen.custom
                    # self.run_display = False
                except ValueError:
                    print('error')

      
            elif self.state == 'Medium':

                try:
                    prob = 0.1
                    tiles = 12
                    print('entered prob:', prob)
                    print('entered prob:', tiles)
                    with open('jsons/prob.json', 'w') as f:
                        json.dump({'prob': prob}, f)

                    with open('jsons/tiles.json', 'w') as f:
                        json.dump({'tiles': tiles}, f)

                    subprocess.Popen(['python', 'game.py'])
                    pygame.quit()
                    # from game import Game 
                    # game = Game()
                    # game.new()
                    # game.run()
                    # self.start_screen.curr_menu = self.start_screen.custom
                    # self.run_display = False
                except ValueError:
                    print('error')
            
            elif self.state == 'Hard':

                try:
                    prob = 0.2
                    tiles = 16
                    print('entered prob:', prob)
                    print('entered prob:', tiles)
                    with open('jsons/prob.json', 'w') as f:
                        json.dump({'prob': prob}, f)

                    with open('jsons/tiles.json', 'w') as f:
                        json.dump({'tiles': tiles}, f)

                    subprocess.Popen(['python', 'game.py'])
                    pygame.quit()     
                    # from game import Game  
                    # game = Game()
                    # game.new()
                    # game.run()
                    # self.start_screen.curr_menu = self.start_screen.custom
                    # self.run_display = False
                except ValueError:
                    print('error')
            
            elif self.state == 'Impossible':

                try:
                    prob = 0.5
                    tiles = 25
                    print('entered prob:', prob)
                    print('entered prob:', tiles)
                    with open('jsons/prob.json', 'w') as f:
                        json.dump({'prob': prob}, f)

                    with open('jsons/tiles.json', 'w') as f:
                        json.dump({'tiles': tiles}, f)

                    subprocess.Popen(['python', 'game.py'])
                    pygame.quit()
                    # from game import Game  
                    # game = Game()
                    # game.new()
                    # game.run()
                    # self.start_screen.curr_menu = self.start_screen.custom
                    # self.run_display = False
                except ValueError:
                    print('error')
        
class StartGame(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.state = 'Presetted'
        self.predx, self.predy = self.mid_w, self.mid_h - 0
        self.codx, self.cody = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.predx + self.offset, self.predy)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            self.check_input()
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text('Difficulty', 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 80)
            self.start_screen.draw_text("Presetted", 35, self.predx, self.predy)
            self.start_screen.draw_text("Custom", 35, self.codx, self.cody)


            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.start_screen.BACK_KEY:
            self.start_screen.curr_menu = self.start_screen.main_menu
            self.run_display = False
        elif self.start_screen.UP_KEY:
            if self.state == 'Custom':
                self.state = 'Presetted'
                self.cursor_rect.midtop = (self.predx + self.offset, self.predy)
            elif self.state == 'Presetted':
                self.state = 'Custom'
                self.cursor_rect.midtop = (self.codx + self.offset, self.cody)
        elif self.start_screen.DOWN_KEY:
            if self.state == 'Presetted':
                self.state = 'Custom'
                self.cursor_rect.midtop = (self.codx + self.offset, self.cody)
            elif self.state == 'Custom':
                self.state = 'Presetted'
                self.cursor_rect.midtop = (self.predx + self.offset, self.predy)
                
        elif self.start_screen.START_KEY:
            if self.state == 'Presetted':

                self.start_screen.curr_menu = self.start_screen.secredit
                self.run_display = False

            elif self.state == 'Custom':

                self.start_screen.curr_menu = self.start_screen.custom
                self.run_display = False
    
class Custom(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.state = 'Tiles'
        self.predx, self.predy = self.mid_w, self.mid_h - 0
        self.codx, self.cody = self.mid_w, self.mid_h + 50
        self.playx, self.playy = self.mid_w, self.mid_h + 120
        self.tilesx, self.tilesy = self.mid_w, self.mid_h + 160
        self.probx, self.proby = self.mid_w, self.mid_h + 190
        self.cursor_rect.midtop = (self.predx + self.offset, self.predy)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))

    def display_menu(self):


        with open('jsons/tiles.json',  'r') as f:
            data = json.load(f)
        
        with open('jsons/prob.json',  'r') as f:
            data1 = json.load(f)

        probs = str(data1['prob'])
        tiles = str(data['tiles'])
            
        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            self.check_input()
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text('Make it your own!', 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 80)
            self.start_screen.draw_text("Tiles", 35, self.predx, self.predy)
            self.start_screen.draw_text("Probability", 35, self.codx, self.cody)
            self.start_screen.draw_text("Play!", 35, self.playx, self.playy)
            self.start_screen.draw_text("Current tiles - " + tiles + ' x ' + tiles, 17, self.tilesx, self.tilesy)
            self.start_screen.draw_text("Current probability - " + probs, 17, self.probx, self.proby)

            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.start_screen.BACK_KEY:
            self.start_screen.curr_menu = self.start_screen.main_menu
            self.run_display = False
        elif self.start_screen.DOWN_KEY:
            if self.state == 'Tiles':
                self.state = 'Probability'
                self.cursor_rect.midtop = (self.codx + self.offset, self.cody)
            elif self.state == 'Probability':
                self.state = 'Play!'
                self.cursor_rect.midtop = (self.playx + self.offset, self.playy)
            elif self.state == 'Play!':
                self.state = 'Tiles'
                self.cursor_rect.midtop = (self.predx + self.offset, self.predy)
        elif self.start_screen.UP_KEY:
            if self.state == 'Play!':
                self.state = 'Probability'
                self.cursor_rect.midtop = (self.codx + self.offset, self.cody)
            elif self.state == 'Probability':
                self.state = 'Tiles'
                self.cursor_rect.midtop = (self.predx + self.offset, self.predy)
            elif self.state == 'Tiles':
                self.state = 'Play!'
                self.cursor_rect.midtop = (self.playx + self.offset, self.playy)
                
        elif self.start_screen.START_KEY:
            if self.state == 'Tiles':

                self.start_screen.curr_menu = self.start_screen.size
                self.run_display = False

            elif self.state == 'Probability':

                self.start_screen.curr_menu = self.start_screen.prob
                self.run_display = False

            elif self.state == 'Play!':

                subprocess.Popen(['python', 'game.py'])
                pygame.quit()


class Size(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))
    def display_menu(self):
        self.run_display = True
        input_box = pygame.Rect(self.start_screen.DISPLAY_W / 2 - 100, self.start_screen.DISPLAY_H / 2, 200, 32)
        input_text = ''
        while self.run_display:
            self.start_screen.check_events()
            if self.start_screen.START_KEY or self.start_screen.BACK_KEY:
                self.start_screen.curr_menu = self.start_screen.custom
                self.run_display = False
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text('Adjust tiles', 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 70)


            font = pygame.font.Font('fonts/Jolana.ttf', 30)
            font2 = pygame.font.Font('fonts/Jolana.ttf', 20)
            input_surface = font.render('Number of tiles -  ' + input_text, True, self.start_screen.WHITE)
            self.start_screen.display.blit(input_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(200, input_surface.get_width() + 10)


            save_text = font2.render("Press 's' to save", True, self.start_screen.WHITE)
            self.start_screen.display.blit(save_text, (self.start_screen.DISPLAY_W / 2 - save_text.get_width() / 2, self.start_screen.DISPLAY_H / 2 + 60))
            save_text = font2.render("Press 'enter' to exit", True, self.start_screen.WHITE)
            self.start_screen.display.blit(save_text, (self.start_screen.DISPLAY_W / 2 - save_text.get_width() / 2, self.start_screen.DISPLAY_H / 2 + 90))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isnumeric():
                        input_text += event.unicode
                    elif event.key == pygame.K_RETURN:
                        if input_text:
                            tiles = {'tiles': input_text}
                            with open('jsons/tiles.json', 'w') as f:
                                json.dump(tiles, f)
                            print('User entered size:', input_text, 'and saved to tiles.json')
                        self.start_screen.curr_menu = self.start_screen.custom
                        self.run_display = False
                    elif event.key == pygame.K_s:
                        if input_text:
                            tiles = {'tiles': input_text}
                            with open('jsons/tiles.json', 'w') as f:
                                json.dump(tiles, f)
                            print('User entered size:', input_text, 'and saved to tiles.json')
                    elif event.key == pygame.K_r:
                        self.start_screen.curr_menu = self.start_screen.custom
                        self.run_display = False

            self.blit_screen()




class Prob(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))

    def display_menu(self):
        self.run_display = True
        input_box = pygame.Rect(self.start_screen.DISPLAY_W / 2 - 100, self.start_screen.DISPLAY_H / 2, 200, 32)
        input_text = ''
        while self.run_display:
            self.start_screen.check_events()
            if self.start_screen.START_KEY or self.start_screen.BACK_KEY:
                self.start_screen.curr_menu = self.start_screen.custom
                self.run_display = False
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text('Adjust probability', 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 70)


            font = pygame.font.Font('fonts/Jolana.ttf', 30)
            font2 = pygame.font.Font('fonts/Jolana.ttf', 20)
            input_surface = font.render('Odds of a bomb -  ' + input_text, True, self.start_screen.WHITE)
            self.start_screen.display.blit(input_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(200, input_surface.get_width() + 10)

            save_text = font2.render("Press 's' to save", True, self.start_screen.WHITE)
            self.start_screen.display.blit(save_text, (self.start_screen.DISPLAY_W / 2 - save_text.get_width() / 2, self.start_screen.DISPLAY_H / 2 + 60))
            save_text = font2.render("Press 'enter' to exit", True, self.start_screen.WHITE)
            self.start_screen.display.blit(save_text, (self.start_screen.DISPLAY_W / 2 - save_text.get_width() / 2, self.start_screen.DISPLAY_H / 2 + 90))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit() or event.unicode == '.':
                        if event.unicode == '.' and '.' in input_text:
                            pass
                        else:
                            input_text += event.unicode
                    elif event.key == pygame.K_RETURN:
                        try:
                            prob = float(input_text)
                            print('entered prob:', prob)
                            with open('jsons/prob.json', 'w') as f:
                                json.dump({'prob': prob}, f)
                            self.start_screen.curr_menu = self.start_screen.custom
                            self.run_display = False
                        except ValueError:
                            print('error')
            self.blit_screen()

# class CustomPlay(Menu):

#     def __init__(self, start_screen):
#         Menu.__init__(self, start_screen)
#         self.background = pygame.image.load('images/background3.png').convert()
#         self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))


#     def display_menu(self):

        
#         subprocess.Popen(['python', 'game.py'])
#         pygame.quit()
#         # from game import Game  
#         # game = Game()
#         # game.new()
#         # game.run()

class Resolution(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.state = 'Width'
        self.predx, self.predy = self.mid_w, self.mid_h + 20
        self.codx, self.cody = self.mid_w, self.mid_h + 80
        self.cursor_rect.midtop = (self.predx + self.offset, self.predy)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))
        
    def display_menu(self):

        with open('jsons/resx.json',  'r') as f:
                    data2 = json.load(f)
                    print(data2['width'])


        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            self.check_input()
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text('Change resolution', 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 100)
            self.start_screen.draw_text('Current resolution - ' + data2['width']+ ' x ' + data2['width'], 20, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 40)
            self.start_screen.draw_text("Width", 35, self.predx, self.predy)
            # self.start_screen.draw_text("Height", 35, self.codx, self.cody)

            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.start_screen.BACK_KEY:
            self.start_screen.curr_menu = self.start_screen.options
            self.run_display = False
        elif self.start_screen.UP_KEY:
            if self.state == 'Width':
                self.state = 'Width'
                self.cursor_rect.midtop = (self.predx + self.offset, self.predy)
        elif self.start_screen.DOWN_KEY:
            if self.state == 'Width':
                self.state = 'Width'
                self.cursor_rect.midtop = (self.predx + self.offset, self.predy)

                
        elif self.start_screen.START_KEY:
            if self.state == 'Width':

                self.start_screen.curr_menu = self.start_screen.resw
                self.run_display = False


class ResWidth(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))
    def display_menu(self):
        self.run_display = True
        input_box = pygame.Rect(self.start_screen.DISPLAY_W / 2 - 100, self.start_screen.DISPLAY_H / 2, 200, 32)
        input_text = ''
        while self.run_display:
            self.start_screen.check_events()
            if self.start_screen.START_KEY or self.start_screen.BACK_KEY:
                self.start_screen.curr_menu = self.start_screen.resolution
                self.run_display = False
            self.start_screen.display.blit(self.background, (0, 0))


            font = pygame.font.Font('fonts/Jolana.ttf', 40)
            font2 = pygame.font.Font('fonts/Jolana.ttf', 20)
            input_surface = font.render('Width -  ' + input_text, True, self.start_screen.WHITE)
            self.start_screen.display.blit(input_surface, (input_box.x + 5, input_box.y + -35))
            input_box.w = max(200, input_surface.get_width() + 10)

            save_text = font2.render("Press 's' to save", True, self.start_screen.WHITE)
            self.start_screen.display.blit(save_text, (self.start_screen.DISPLAY_W / 2 - save_text.get_width() / 2, self.start_screen.DISPLAY_H / 2 + 30))
            save_text = font2.render("Press 'enter' to exit", True, self.start_screen.WHITE)
            self.start_screen.display.blit(save_text, (self.start_screen.DISPLAY_W / 2 - save_text.get_width() / 2, self.start_screen.DISPLAY_H / 2 + 60))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isnumeric():
                        input_text += event.unicode
                    elif event.key == pygame.K_RETURN:
                        if input_text:
                            res = {'width': input_text}
                            with open('jsons/resx.json', 'w') as f:
                                json.dump(res, f)
                            print('User entered width:', input_text, 'and saved to resx.json')
                        self.start_screen.curr_menu = self.start_screen.resolution
                        self.run_display = False
                    elif event.key == pygame.K_s:
                        if input_text:
                            res = {'width': input_text}
                            with open('jsons/resx.json', 'w') as f:
                                json.dump(res, f)
                            print('User entered width:', input_text, 'and saved to resx.json')
                    elif event.key == pygame.K_r:
                        self.start_screen.curr_menu = self.start_screen.resolution
                        self.run_display = False


            self.blit_screen()

class Win(Menu):

    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.state = 'Main menu'
        self.predx, self.predy = self.mid_w, self.mid_h - 0
        self.codx, self.cody = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.codx + self.offset, self.cody)
        self.background = pygame.image.load('images/background3.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            self.check_input()
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text('You won!', 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 80)
            self.start_screen.draw_text("Main menu", 35, self.codx, self.cody)


            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.start_screen.BACK_KEY:
            self.start_screen.curr_menu = self.start_screen.main_menu
            self.run_display = False
        elif self.start_screen.UP_KEY:
            if self.state == 'Main menu':
                self.state = 'Main menu'
                self.cursor_rect.midtop = (self.codx + self.offset, self.cody)
        elif self.start_screen.DOWN_KEY:
            if self.state == 'Main menu':
                self.state = 'Main menu'
                self.cursor_rect.midtop = (self.codx + self.offset, self.cody)

                
        elif self.start_screen.START_KEY:
            if self.state == 'Main menu':
                print("in")
                self.start_screen.curr_menu = self.start_screen.main_menu
                pygame.quit()


           

class MultiplayerMenu(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.state = "Set Name"
        self.namex, self.namey = self.mid_w, self.mid_h - 40
        self.createx, self.createy = self.mid_w, self.mid_h + 20
        self.joinx, self.joiny = self.mid_w, self.mid_h + 80
        self.backx, self.backy = self.mid_w, self.mid_h + 140
        self.cursor_rect.midtop = (self.namex + self.offset, self.namey)
        self.background = pygame.image.load("images/background3.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H)
        )

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            self.check_input()
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text(
                "Multiplayer", 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 120
            )
            self.start_screen.draw_text(
                f"Set Name", 30, self.namex, self.namey
            )
            self.start_screen.draw_text("Create Room", 30, self.createx, self.createy)
            self.start_screen.draw_text("Join Room", 30, self.joinx, self.joiny)
            self.start_screen.draw_text("Back", 30, self.backx, self.backy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.start_screen.DOWN_KEY:
            if self.state == "Set Name":
                self.cursor_rect.midtop = (self.createx + self.offset, self.createy)
                self.state = "Create Room"
            elif self.state == "Create Room":
                self.cursor_rect.midtop = (self.joinx + self.offset, self.joiny)
                self.state = "Join Room"
            elif self.state == "Join Room":
                self.cursor_rect.midtop = (self.backx + self.offset, self.backy)
                self.state = "Back"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.namex + self.offset, self.namey)
                self.state = "Set Name"

        elif self.start_screen.UP_KEY:
            if self.state == "Set Name":
                self.cursor_rect.midtop = (self.backx + self.offset, self.backy)
                self.state = "Back"
            elif self.state == "Back":
                self.cursor_rect.midtop = (self.joinx + self.offset, self.joiny)
                self.state = "Join Room"
            elif self.state == "Join Room":
                self.cursor_rect.midtop = (self.createx + self.offset, self.createy)
                self.state = "Create Room"
            elif self.state == "Create Room":
                self.cursor_rect.midtop = (self.namex + self.offset, self.namey)
                self.state = "Set Name"

    def check_input(self):
        self.move_cursor()
        if self.start_screen.BACK_KEY:
            self.start_screen.curr_menu = self.start_screen.main_menu
            self.run_display = False
        elif self.start_screen.START_KEY:
            if self.state == "Set Name":
                self.start_screen.curr_menu = self.start_screen.name_menu
            elif self.state == "Create Room":
                self.start_screen.next_multiplayer_action = "create"
                if not self.start_screen.player_name:
                    self.start_screen.curr_menu = self.start_screen.name_menu
                else:
                    client = self.start_screen.ensure_network()
                    client.send(
                        "create_room",
                        {"name": self.start_screen.player_name},
                    )
                    self.start_screen.curr_menu = self.start_screen.lobby_menu
            elif self.state == "Join Room":
                self.start_screen.next_multiplayer_action = "join"
                if not self.start_screen.player_name:
                    self.start_screen.curr_menu = self.start_screen.name_menu
                else:
                    self.start_screen.curr_menu = self.start_screen.room_menu
            elif self.state == "Back":
                self.start_screen.curr_menu = self.start_screen.main_menu
            self.run_display = False


class NameEntryMenu(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.background = pygame.image.load("images/background3.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H)
        )

    def display_menu(self):
        self.run_display = True
        input_box = pygame.Rect(
            self.start_screen.DISPLAY_W / 2 - 160,
            self.start_screen.DISPLAY_H / 2,
            320,
            32,
        )
        input_text = self.start_screen.player_name
        while self.run_display:
            self.start_screen.check_events()
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text(
                "Enter your name",
                40,
                self.start_screen.DISPLAY_W / 2,
                self.start_screen.DISPLAY_H / 2 - 80,
            )
            font = pygame.font.Font("fonts/Jolana.ttf", 30)
            input_surface = font.render(input_text, True, self.start_screen.WHITE)
            self.start_screen.display.blit(input_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(320, input_surface.get_width() + 10)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.start_screen.player_name = input_text.strip() or "Player"
                        with open("jsons/player_name.json", "w") as file_handle:
                            json.dump({"name": self.start_screen.player_name}, file_handle)
                        self.start_screen.curr_menu = self.start_screen.multiplayer_menu
                        self.run_display = False
                    elif event.unicode.isprintable():
                        input_text += event.unicode
                    self.start_screen.player_name = input_text.strip()
            
            self.blit_screen()


class RoomMenu(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.background = pygame.image.load("images/background3.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H)
        )

    def display_menu(self):
        self.run_display = True
        input_box = pygame.Rect(
            self.start_screen.DISPLAY_W / 2 - 160,
            self.start_screen.DISPLAY_H / 2,
            320,
            32,
        )
        input_text = ""
        action = self.start_screen.next_multiplayer_action
        while self.run_display:
            self.start_screen.check_events()
            self.start_screen.display.blit(self.background, (0, 0))
            if action == "join":
                self.start_screen.draw_text(
                    "Enter room code",
                    40,
                    self.start_screen.DISPLAY_W / 2,
                    self.start_screen.DISPLAY_H / 2 - 80,
                )
            else:
                self.start_screen.draw_text(
                    "Create a room",
                    40,
                    self.start_screen.DISPLAY_W / 2,
                    self.start_screen.DISPLAY_H / 2 - 80,
                )
                self.start_screen.draw_text(
                    "Press Enter to create",
                    24,
                    self.start_screen.DISPLAY_W / 2,
                    self.start_screen.DISPLAY_H / 2 - 20,
                )
            font = pygame.font.Font("fonts/Jolana.ttf", 30)
            input_surface = font.render(input_text, True, self.start_screen.WHITE)
            if action == "join":
                self.start_screen.display.blit(input_surface, (input_box.x + 5, input_box.y + 5))
                input_box.w = max(320, input_surface.get_width() + 10)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        client = self.start_screen.ensure_network()
                        if action == "join":
                            client.send(
                                "join_room",
                                {
                                    "code": input_text.strip().upper(),
                                    "name": self.start_screen.player_name,
                                },
                            )
                        else:
                            client.send(
                                "create_room",
                                {"name": self.start_screen.player_name},
                            )
                        self.start_screen.curr_menu = self.start_screen.lobby_menu
                        self.run_display = False
                    elif event.unicode.isprintable() and action == "join":
                        input_text += event.unicode

            self.blit_screen()


class LobbyMenu(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.background = pygame.image.load("images/background3.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H)
        )

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            self.check_input()
            state = self.start_screen.multiplayer_state
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text(
                "Lobby", 50, self.start_screen.DISPLAY_W / 2, 80
            )
            room_code = state.get("room_code") or "---"
            self.start_screen.draw_text(
                f"Room Code: {room_code}", 30, self.start_screen.DISPLAY_W / 2, 140
            )
            settings = state.get("settings", {})
            settings_line = (
                f"Tiles: {settings.get('rows', 10)} | "
                f"Prob: {settings.get('probability', 0.15)} | "
                f"Width: {settings.get('width', self.start_screen.DISPLAY_W)}"
            )
            self.start_screen.draw_text(
                settings_line,
                22,
                self.start_screen.DISPLAY_W / 2,
                180,
            )
            self.start_screen.draw_text("Players:", 30, 140, 200)
            y_offset = 240
            for player in state.get("players", []):
                label = f"{player.get('name', 'Player')} - {player.get('status', 'alive')}"
                self.start_screen.draw_text(label, 24, 200, y_offset)
                y_offset += 40
            if self.is_host():
                self.start_screen.draw_text(
                    "Edit settings 'E'", 24, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H - 140
                )
                self.start_screen.draw_text(
                    "Start game 'Enter'", 24, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H - 100
                )
            self.start_screen.draw_text(
                "Back 'Esc'", 24, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H - 60
            )
            self.blit_screen()

    def is_host(self):
        state = self.start_screen.multiplayer_state
        return state.get("player_id") == state.get("host_id")

    def check_input(self):
        if self.start_screen.BACK_KEY:
            self.start_screen.curr_menu = self.start_screen.multiplayer_menu
            self.run_display = False
            return
        if self.start_screen.E_KEY and self.is_host():
            self.start_screen.curr_menu = self.start_screen.lobby_settings_menu
            self.run_display = False
            return
        if self.start_screen.START_KEY and self.is_host():
            state = self.start_screen.multiplayer_state
            client = self.start_screen.ensure_network()
            client.send(
                "start_game",
                {
                    "code": state.get("room_code"),
                    "player_id": state.get("player_id"),
                },
            )


class LobbySettingsMenu(Menu):
    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.background = pygame.image.load("images/background3.png").convert()
        self.background = pygame.transform.scale(
            self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H)
        )

    def display_menu(self):
        self.run_display = True
        input_box = pygame.Rect(
            self.start_screen.DISPLAY_W / 2 - 200,
            self.start_screen.DISPLAY_H / 2,
            400,
            32,
        )
        settings = self.start_screen.multiplayer_state.get("settings", {})
        rows = str(settings.get("rows", 10))
        probability = str(settings.get("probability", 0.15))
        width = str(settings.get("width", self.start_screen.DISPLAY_W))
        field = "rows"
        while self.run_display:
            self.start_screen.poll_network()
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text(
                "Lobby Settings",
                40,
                self.start_screen.DISPLAY_W / 2,
                self.start_screen.DISPLAY_H / 2 - 120,
            )
            self.start_screen.draw_text(
                "Use Tab to switch fields, Enter to save, Esc to cancel",
                20,
                self.start_screen.DISPLAY_W / 2,
                self.start_screen.DISPLAY_H / 2 - 80,
            )
            font = pygame.font.Font("fonts/Jolana.ttf", 26)
            tiles_label = f"'{rows}'" if field == "rows" else rows
            prob_label = f"'{probability}'" if field == "probability" else probability
            width_label = f"'{width}'" if field == "width" else width
            field_label = (
                f"Tiles: {tiles_label}  |  Probability: {prob_label}  |  Width: {width_label}"
            )
            input_surface = font.render(field_label, True, self.start_screen.WHITE)
            self.start_screen.display.blit(input_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(400, input_surface.get_width() + 10)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        field = "probability" if field == "rows" else "width" if field == "probability" else "rows"
                    elif event.key == pygame.K_BACKSPACE:
                        if field == "rows":
                            rows = rows[:-1]
                        elif field == "probability":
                            probability = probability[:-1]
                        else:
                            width = width[:-1]
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.save_settings(rows, probability, width)
                        self.start_screen.curr_menu = self.start_screen.lobby_menu
                        self.run_display = False
                    elif event.key == pygame.K_ESCAPE:
                        self.start_screen.curr_menu = self.start_screen.lobby_menu
                        self.run_display = False
                    elif event.unicode.isdigit() or (event.unicode == "." and field == "probability"):
                        if field == "rows":
                            rows += event.unicode
                        elif field == "probability":
                            probability += event.unicode
                        else:
                            width += event.unicode
                elif event.type == pygame.QUIT:
                    self.start_screen.running = False
                    self.run_display = False

            self.blit_screen()

    def save_settings(self, rows, probability, width):
        try:
            settings = {
                "rows": int(rows),
                "cols": int(rows),
                "probability": float(probability),
                "width": max(int(width), MULTIPLAYER_SIDEBAR_WIDTH + 200),
            }
        except ValueError:
            return
        state = self.start_screen.multiplayer_state
        state["settings"] = settings
        client = self.start_screen.ensure_network()
        client.send(
            "update_settings",
            {
                "code": state.get("room_code"),
                "player_id": state.get("player_id"),
                "settings": settings,
            },
        )