import pygame
from settings import *
from sprites import *
from start_screen import *
import time
import json
import sys


class Game:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.timer_font = pygame.font.Font(None, 32)  # set the font and size for the timer text
        self.timer_rect = pygame.Rect(0, 0, 100, 50)  # define a rectangle for the timer position and size
        self.timer_rect.centerx = self.screen.get_rect().centerx  # center the timer horizontally
        self.win = False
        pygame.mixer.init()
        self.current_track = None

        self.explosion_sound = pygame.mixer.Sound("music/losegame.mp3")
        self.win_sound = pygame.mixer.Sound("music/winsound.mp3")

        pygame.font.init()


    def new(self):
        self.board = Board()
        self.board.display_board()
        self.start_time = pygame.time.get_ticks()  # set the start time for the timer
        self.play_music("music/game.mp3")  # set the start time for the timer

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            if not self.playing:
                self.you_lost()
                self.lose_screen()


    def draw(self):
        if not pygame.display.get_init():
            return
            
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)
        
        # update and blit the timer text to the timer rectangle
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # calculate elapsed time in seconds
        timer_text = self.timer_font.render(f"Time: {elapsed_time}", True, (255, 255, 255))
        timer_text_rect = timer_text.get_rect(center=self.timer_rect.center)
        self.screen.blit(timer_text, timer_text_rect)
        
        # update and blit the mine count text to the screen
        mine_count = sum([1 for row in self.board.board_list for tile in row if tile.flagged])
        mine_count_text = self.timer_font.render(f"Mines: {mine_count}/{AMOUNT_MINES}", True, (255, 255, 255))
        mine_count_rect = mine_count_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.screen.blit(mine_count_text, mine_count_rect)
        
        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        print("win")
        return True

    def events(self):
        mines = AMOUNT_MINES
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= TILESIZE
                my //= TILESIZE

                if event.button == 1:
                    if not self.board.board_list[mx][my].flagged:
                        # dig and check if exploded
                        if not self.board.dig(mx, my):
                            # explode
                            for row in self.board.board_list:
                                for tile in row:
                                    if tile.flagged and tile.type != "X":
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = tile_not_mine
                                    elif tile.type == "X":
                                        tile.revealed = True
                            self.play_music("music/losegame.mp3")
                            self.playing = False
                            self.explosion_sound.play()
                            print("lost")
                            # pygame.quit()
                        else:
                            # play sound
                            pygame.mixer.Sound("music/flags.mp3").play()

                if event.button == 3:
                    if not self.board.board_list[mx][my].revealed:
                        if self.board.board_list[mx][my].flagged:
                            mines += 1 # Increment mine counter by 1
                        else:
                            mines -= 1 # Decrement mine counter by 1
                        self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged
                        # play sound
                        pygame.mixer.Sound("music/flagp.mp3").play()

            if self.check_win():
                if not self.win:
                    self.win_time = pygame.time.get_ticks()  # set the win time for the timer
                    self.win = True
                    for row in self.board.board_list:
                        for tile in row:
                            if not tile.revealed:
                                tile.flagged = True
                    self.win_sound.play()
                
                if self.win_time + 10 < pygame.time.get_ticks():  # if 3 seconds have passed since winning
                    self.playing = False
                    self.you_won()

                if self.win_time + 10 < pygame.time.get_ticks():  # if 3 seconds have passed since winning
                    self.playing = False
                    self.win_screen()

    def play_music(self, track):
        if self.current_track == track:
            return
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(-1)
        self.current_track = track
                    

    def lose_screen(self):
        font = pygame.font.Font('fonts/Jolana.ttf', 40)
        font_big = pygame.font.Font('fonts/Jolana.ttf', 72)
        you_won_text = font_big.render("You lost!", True, (255, 255, 255))
        play_again_text = font.render("Play again", True, (255, 255, 255))
        back_to_menu_text = font.render("Back to main menu", True, (255, 255, 255))

        you_won_text_rect = you_won_text.get_rect(center=self.screen.get_rect().center)
        play_again_text_rect = play_again_text.get_rect(center=self.screen.get_rect().center)
        back_to_menu_text_rect = back_to_menu_text.get_rect(center=self.screen.get_rect().center)
        
        # move the "You won!" text 50 pixels higher than the center
        you_won_text_rect.move_ip(0, -50)
        play_again_text_rect.move_ip(0, 70) # move the "Play again!" button below the "You won!" text
        back_to_menu_text_rect.move_ip(0, 140) # move the "Back to main menu" button below the "Play again!" button

        background_image = pygame.image.load("images/lost.png").convert()
        background_img = pygame.transform.scale(background_image, self.screen.get_size())
        self.screen.blit(background_img, (0, 0)) # blit the background image onto the screen

        # pygame.draw.rect(self.screen, (0, 0, 0, 0), you_won_text_rect, border_radius=5) # change color to (0, 0, 0, 0) to make it transparent
        # pygame.draw.rect(self.screen, (0, 0, 0, 0), play_again_text_rect, border_radius=5) # change color to (0, 0, 0, 0) to make it transparent
        # pygame.draw.rect(self.screen, (0, 0, 0, 0), back_to_menu_text_rect, border_radius=5) # change color to (0, 0, 0, 0) to make it transparent

        self.screen.blit(you_won_text, you_won_text_rect)
        self.screen.blit(play_again_text, play_again_text_rect)
        self.screen.blit(back_to_menu_text, back_to_menu_text_rect)

        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    if play_again_text_rect.collidepoint(mx, my):
                        self.playing = True
                        self.win = False
                        self.new()
                        self.run()
                        return
                    elif back_to_menu_text_rect.collidepoint(mx, my):
                        pygame.quit()
                        s = Start_Screen()
                        while s.running:
                            pygame.display.set_caption('Minesweeper')
                            icon = pygame.image.load(r"images\icon.png")
                            pygame.display.set_icon(icon)
                            s.curr_menu.display_menu()
                            s.game_loop()

                        return
                    
    def win_screen(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # calculate elapsed time in seconds
        fianle = elapsed_time - 3
        convert = time.strftime("%H:%M:%S", time.gmtime(fianle))
        font = pygame.font.Font('fonts/Jolana.ttf', 40)
        font_big = pygame.font.Font('fonts/Jolana.ttf', 72)
        you_won_text = font_big.render("You won!", True, (255, 255, 255))
        play_again_text = font.render("Play again", True, (255, 255, 255))
        back_to_menu_text = font.render("Back to main menu", True, (255, 255, 255))
        test_text = font.render(f"Total time - {convert}", True, (255, 255, 255))

        you_won_text_rect = you_won_text.get_rect(center=self.screen.get_rect().center)
        play_again_text_rect = play_again_text.get_rect(center=self.screen.get_rect().center)
        back_to_menu_text_rect = back_to_menu_text.get_rect(center=self.screen.get_rect().center)
        test_text_rect = test_text.get_rect(center=self.screen.get_rect().center)

        # move the "You won!" text 50 pixels higher than the center
        you_won_text_rect.move_ip(0, -50)
        play_again_text_rect.move_ip(0, 70) # move the "Play again!" button below the "You won!" text
        back_to_menu_text_rect.move_ip(0, 140) # move the "Back to main menu" button below the "Play again!" button
        test_text_rect.move_ip(0, 210) # move the "Test" button below the "Back to main menu" button

        background_image = pygame.image.load("images/win.png").convert()
        background_img = pygame.transform.scale(background_image, self.screen.get_size())
        self.screen.blit(background_img, (0, 0)) # blit the background image onto the screen


        pygame.draw.rect(self.screen, (0, 0, 0, 0), you_won_text_rect, border_radius=5) # change color to (0, 0, 0, 0) to make it transparent
        pygame.draw.rect(self.screen, (0, 0, 0, 0), play_again_text_rect, border_radius=5) # change color to (0, 0, 0, 0) to make it transparent
        pygame.draw.rect(self.screen, (0, 0, 0, 0), back_to_menu_text_rect, border_radius=5) # change color to (0, 0, 0, 0) to make it transparent
        pygame.draw.rect(self.screen, (0, 0, 0, 0), test_text_rect, border_radius=5) # change color to (0, 0, 0, 0) to make it transparent

        self.screen.blit(you_won_text, you_won_text_rect)
        self.screen.blit(play_again_text, play_again_text_rect)
        self.screen.blit(back_to_menu_text, back_to_menu_text_rect)
        self.screen.blit(test_text, test_text_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    if play_again_text_rect.collidepoint(mx, my):
                        self.playing = True
                        self.win = False
                        self.new()
                        self.run()
                        return
                    elif back_to_menu_text_rect.collidepoint(mx, my):
                        pygame.quit()
                        s = Start_Screen()
                        while s.running:
                            pygame.display.set_caption('Minesweeper')
                            icon = pygame.image.load(r"images\icon.png")
                            pygame.display.set_icon(icon)
                            s.curr_menu.display_menu()
                            s.game_loop()

                        return
                    

    def you_lost(self):

        font_big = pygame.font.Font('fonts/Jolana.ttf', 100)
        you_lost_text = font_big.render("YOU DIED!", True, (255, 255, 255))
        you_lost_text_rect = you_lost_text.get_rect()
        you_lost_text_rect.center = self.screen.get_rect().center
        # pygame.draw.rect(self.screen, (0, 0, 0, 1), you_lost_text_rect, border_radius=5)
        self.screen.blit(you_lost_text, you_lost_text_rect)
        pygame.display.flip()
        
        time_to_wait = 3
        start_time = time.monotonic()

        while time.monotonic() - start_time < time_to_wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        self.screen.fill((0, 0, 0))
        pygame.display.flip()   
    
    def you_won(self):

        font_big = pygame.font.Font('fonts/Jolana.ttf', 100)
        you_lost_text = font_big.render("YOU WON!", True, (255, 255, 255))
        you_lost_text_rect = you_lost_text.get_rect()
        you_lost_text_rect.center = self.screen.get_rect().center
        # pygame.draw.rect(self.screen, (0, 0, 0, 1), you_lost_text_rect, border_radius=5)
        self.screen.blit(you_lost_text, you_lost_text_rect)
        pygame.display.flip()
        
        time_to_wait = 3
        start_time = time.monotonic()

        while time.monotonic() - start_time < time_to_wait:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        self.screen.fill((0, 0, 0))
        pygame.display.flip()
                    




game = Game()
game.new()
game.run()