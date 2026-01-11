import pygame
import subprocess              
# from board import Board
from menu import *
import time
import json
import math
import os

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
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 70
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 135
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
            self.start_screen.draw_text("Options", 40, self.optionsx, self.optionsy)
            self.draw_cursor()
            self.blit_screen()

            # Update title_size to zoom the Minesweeper text
            self.title_size = 80 + 10 * abs(math.sin(pygame.time.get_ticks() / 400))


    def move_cursor(self):
        if self.start_screen.DOWN_KEY:
            if self.state == 'Start game':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.secreditx + self.offset, self.secredity)
                self.state = 'Start game'

        elif self.start_screen.UP_KEY:
            if self.state == 'Options':
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
            self.start_screen.draw_text('Made by Kristaps un Kristers', 37, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 + 10)
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


class Lose(Menu):


    def __init__(self, start_screen):
        Menu.__init__(self, start_screen)
        self.state = 'Main menu'
        self.codx, self.cody = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.codx + self.offset, self.cody)
        self.background = pygame.image.load('images/TileExploded.png').convert()
        self.background = pygame.transform.scale(self.background, (self.start_screen.DISPLAY_W, self.start_screen.DISPLAY_H))
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.start_screen.check_events()
            self.check_input()
            self.start_screen.display.blit(self.background, (0, 0))
            self.start_screen.draw_text('You lost!', 50, self.start_screen.DISPLAY_W / 2, self.start_screen.DISPLAY_H / 2 - 80)
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


           