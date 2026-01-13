import time
import sys

import pygame

from settings import BGCOLOUR, Settings, MULTIPLAYER_SIDEBAR_WIDTH
from sprites import Board
from start_screen import Start_Screen

class Game:
    def __init__(self, settings=None, multiplayer=None):
        pygame.init()
        self.settings = settings or Settings()
        self.multiplayer = multiplayer
        pygame.display.set_caption(self.settings.title)
        self.sidebar_width = MULTIPLAYER_SIDEBAR_WIDTH if multiplayer else 0
        self.screen = pygame.display.set_mode(
            (
                self.settings.screen_width + self.sidebar_width,
                self.settings.screen_height,
            )
        )
        self.clock = pygame.time.Clock()
        self.timer_font = pygame.font.Font(None, 32)
        self.timer_rect = pygame.Rect(0, 0, 100, 50)
        self.timer_rect.centerx = self.screen.get_rect().centerx
        self.win = False
        pygame.mixer.init()
        self.current_track = None
        self.pending_track = None
        self.music_end_event = pygame.USEREVENT + 1

        self.explosion_sound = pygame.mixer.Sound("music/losegame.mp3")
        self.win_sound = pygame.mixer.Sound("music/winsound.mp3")

        pygame.font.init()

    def new(self):
        seed = None
        self.state = "playing"
        self.waiting_message = None
        self.leaderboard = []
        self.leaderboard_ranked_by = "time"
        self.leaderboard_tie = False
        self.play_music("music/game.mp3")
        if self.multiplayer:
            seed = self.multiplayer.get("seed")
            self.start_timestamp = self.multiplayer.get("start_time", time.time())
        self.board = Board(self.settings, seed=seed)
        self.board.display_board()
        self.start_time = pygame.time.get_ticks()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(self.settings.fps)
            self.poll_network()
            self.events()
            self.update_win_state()
            self.draw()
            if self.multiplayer and self.state == "waiting":
                continue
            if not self.playing:
                if not self.multiplayer:
                    self.you_lost()
                    self.lose_screen()

    def draw(self):
        if not pygame.display.get_init():
            return

        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)

        if self.multiplayer:
            elapsed_time = int(time.time() - self.start_timestamp)
        else:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        timer_text = self.timer_font.render(
            f"Time: {elapsed_time}", True, (255, 255, 255)
        )
        timer_text_rect = timer_text.get_rect(center=self.timer_rect.center)
        self.screen.blit(timer_text, timer_text_rect)

        mine_count = sum(
            1 for row in self.board.board_list for tile in row if tile.flagged
        )
        mine_count_text = self.timer_font.render(
            f"Mines: {mine_count}/{self.settings.amount_mines}",
            True,
            (255, 255, 255),
        )
        mine_right_edge = self.screen.get_width() - 10
        if self.multiplayer:
            mine_right_edge -= self.sidebar_width
        mine_count_rect = mine_count_text.get_rect(topright=(mine_right_edge, 10))
        self.screen.blit(mine_count_text, mine_count_rect)

        if self.multiplayer:
            self.draw_sidebar()
            if self.state == "waiting":
                self.draw_waiting_overlay()

        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "X" and not tile.revealed:
                    return False
        print("win")
        return True

    def events(self):
        mines = self.settings.amount_mines

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit(0)
            if event.type == self.music_end_event:
                self.handle_music_end()
                continue

            if self.state == "waiting":
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= self.settings.tilesize
                my //= self.settings.tilesize
                if mx < 0 or my < 0 or mx >= self.settings.cols or my >= self.settings.rows:
                    continue

                if event.button == 1:
                    if not self.board.board_list[mx][my].flagged:
                        if not self.board.dig(mx, my):
                            for row in self.board.board_list:
                                for tile in row:
                                    if tile.flagged and tile.type != "X":
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = self.settings.tile_not_mine
                                    elif tile.type == "X":
                                        tile.revealed = True
                            print("lost")
                            if self.multiplayer:
                                self.handle_multiplayer_end("dead")
                            else:
                                self.play_music(
                                    "music/losegame.mp3",
                                    loops=0,
                                    on_end="music/waiting_players.mp3",
                                )
                                self.playing = False
                        else:
                            pygame.mixer.Sound("music/flags.mp3").play()

                if event.button == 3:
                    if not self.board.board_list[mx][my].revealed:
                        if self.board.board_list[mx][my].flagged:
                            mines += 1
                        else:
                            mines -= 1
                        self.board.board_list[mx][my].flagged = not self.board.board_list[
                            mx
                        ][my].flagged
                        pygame.mixer.Sound("music/flagp.mp3").play()
                        if self.multiplayer:
                            self.send_flag_update()

    def update_win_state(self):
        if self.state == "waiting":
            return
        if not self.check_win():
            return
        if not self.win:
            self.win_time = pygame.time.get_ticks()
            self.win = True
            for row in self.board.board_list:
                for tile in row:
                    if not tile.revealed:
                        tile.flagged = True
            if self.multiplayer:
                self.play_music(
                    "music/winsound.mp3",
                    loops=0,
                    on_end="music/waiting_players.mp3",
                )
            else:
                pygame.mixer.music.stop()
                self.current_track = None
                self.win_sound.play()

        if self.win_time + 10 < pygame.time.get_ticks():
            if self.multiplayer:
                self.handle_multiplayer_end("finished")
            else:
                self.playing = False
                self.you_won()
                self.win_screen()

    def lose_screen(self):
        if self.multiplayer:
            return
        font = pygame.font.Font("fonts/Jolana.ttf", 40)
        font_big = pygame.font.Font("fonts/Jolana.ttf", 72)
        you_won_text = font_big.render("You lost!", True, (255, 255, 255))
        play_again_text = font.render("Play again", True, (255, 255, 255))
        back_to_menu_text = font.render("Back to main menu", True, (255, 255, 255))

        you_won_text_rect = you_won_text.get_rect(center=self.screen.get_rect().center)
        play_again_text_rect = play_again_text.get_rect(
            center=self.screen.get_rect().center
        )
        back_to_menu_text_rect = back_to_menu_text.get_rect(
            center=self.screen.get_rect().center
        )

        you_won_text_rect.move_ip(0, -50)
        play_again_text_rect.move_ip(0, 70)
        back_to_menu_text_rect.move_ip(0, 140)

        background_image = pygame.image.load("images/lost.png").convert()
        background_img = pygame.transform.scale(
            background_image, self.screen.get_size()
        )
        self.screen.blit(background_img, (0, 0))

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
                    if back_to_menu_text_rect.collidepoint(mx, my):
                        pygame.quit()
                        s = Start_Screen()
                        while s.running:
                            pygame.display.set_caption("Minesweeper")
                            icon = pygame.image.load(r"images\icon.png")
                            pygame.display.set_icon(icon)
                            s.curr_menu.display_menu()
                            s.game_loop()

                        return

    def win_screen(self):
        if self.multiplayer:
            return
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        final_time = elapsed_time - 3
        convert = time.strftime("%H:%M:%S", time.gmtime(final_time))
        font = pygame.font.Font("fonts/Jolana.ttf", 40)
        font_big = pygame.font.Font("fonts/Jolana.ttf", 72)
        you_won_text = font_big.render("You won!", True, (255, 255, 255))
        play_again_text = font.render("Play again", True, (255, 255, 255))
        back_to_menu_text = font.render("Back to main menu", True, (255, 255, 255))
        test_text = font.render(f"Total time - {convert}", True, (255, 255, 255))

        you_won_text_rect = you_won_text.get_rect(center=self.screen.get_rect().center)
        play_again_text_rect = play_again_text.get_rect(
            center=self.screen.get_rect().center
        )
        back_to_menu_text_rect = back_to_menu_text.get_rect(
            center=self.screen.get_rect().center
        )
        test_text_rect = test_text.get_rect(center=self.screen.get_rect().center)

        you_won_text_rect.move_ip(0, -50)
        play_again_text_rect.move_ip(0, 70)
        back_to_menu_text_rect.move_ip(0, 140)
        test_text_rect.move_ip(0, 210)

        background_image = pygame.image.load("images/win.png").convert()
        background_img = pygame.transform.scale(
            background_image, self.screen.get_size()
        )
        self.screen.blit(background_img, (0, 0))

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
                    if back_to_menu_text_rect.collidepoint(mx, my):
                        pygame.quit()
                        s = Start_Screen()
                        while s.running:
                            pygame.display.set_caption("Minesweeper")
                            icon = pygame.image.load(r"images\icon.png")
                            pygame.display.set_icon(icon)
                            s.curr_menu.display_menu()
                            s.game_loop()

                        return

    def you_lost(self):
        font_big = pygame.font.Font("fonts/Jolana.ttf", 100)
        you_lost_text = font_big.render("YOU LOST!", True, (255, 255, 255))
        you_lost_text_rect = you_lost_text.get_rect()
        you_lost_text_rect.center = self.screen.get_rect().center
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
        font_big = pygame.font.Font("fonts/Jolana.ttf", 100)
        you_lost_text = font_big.render("YOU WON!", True, (255, 255, 255))
        you_lost_text_rect = you_lost_text.get_rect()
        you_lost_text_rect.center = self.screen.get_rect().center
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

    def send_flag_update(self):
        if not self.multiplayer:
            return
        flag_count = sum(
            1 for row in self.board.board_list for tile in row if tile.flagged
        )
        self.multiplayer["client"].send(
            "flag_update",
            {
                "flags": flag_count,
                "code": self.multiplayer.get("room_code"),
                "player_id": self.multiplayer.get("player_id"),
            },
        )

    def handle_multiplayer_end(self, status):
        if self.state != "playing":
            return
        self.state = "waiting"
        elapsed_time = int(time.time() - self.start_timestamp)
        self.multiplayer["client"].send(
            "player_status",
            {
                "status": status,
                "time": elapsed_time,
                "code": self.multiplayer.get("room_code"),
                "player_id": self.multiplayer.get("player_id"),
            },
        )
        if status == "dead":
            self.play_music(
                "music/losegame.mp3",
                loops=0,
                on_end="music/waiting_players.mp3",
            )
            self.waiting_message = "You died! Waiting for others..."
        else:
            if self.current_track != "music/winsound.mp3":
                self.play_music("music/waiting_players.mp3")
            self.waiting_message = "You finished! Waiting for others..."

    def play_music(self, track, loops=-1, on_end=None):
        if self.current_track == track:
            return
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(loops)
        self.current_track = track
        self.pending_track = on_end
        pygame.mixer.music.set_endevent(
            self.music_end_event if on_end is not None else 0
        )

    def handle_music_end(self):
        if not self.pending_track:
            return
        next_track = self.pending_track
        self.pending_track = None
        self.play_music(next_track)

    def draw_sidebar(self):
        sidebar_rect = pygame.Rect(
            self.screen.get_width() - self.sidebar_width,
            0,
            self.sidebar_width,
            self.settings.screen_height,
        )
        pygame.draw.rect(self.screen, (30, 30, 30), sidebar_rect)
        title = self.timer_font.render("Players", True, (255, 255, 255))
        self.screen.blit(title, (sidebar_rect.x + 10, 10))
        y_offset = 50
        for player in self.multiplayer.get("players", []):
            status = player.get("status", "alive")
            flags = player.get("flags", 0)
            label = f"{player.get('name', 'Player')} - {status} - flags: {flags}"
            color = (255, 255, 255)
            if status == "dead":
                color = (255, 80, 80)
            elif status == "finished":
                color = (80, 255, 120)
            text = self.timer_font.render(label, True, color)
            self.screen.blit(text, (sidebar_rect.x + 10, y_offset))
            y_offset += 30

    def draw_waiting_overlay(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        message = self.waiting_message or "Waiting for others..."
        text = self.timer_font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, text_rect)

    def poll_network(self):
        if not self.multiplayer:
            return
        client = self.multiplayer["client"]
        for message in client.get_messages():
            if message.get("type") == "game_update":
                self.multiplayer["players"] = message["payload"].get("players", [])
            elif message.get("type") == "game_finished":
                self.leaderboard = message["payload"].get("leaderboard", [])
                self.leaderboard_ranked_by = message["payload"].get("ranked_by", "time")
                self.leaderboard_tie = message["payload"].get("tie", False)
                self.playing = False
                self.leaderboard_screen()

    def leaderboard_screen(self):
        font = pygame.font.Font("fonts/Jolana.ttf", 40)
        font_big = pygame.font.Font("fonts/Jolana.ttf", 72)
        title_text = font_big.render("Leaderboard", True, (255, 255, 255))
        background_image = pygame.image.load("images/win.png").convert()
        background_img = pygame.transform.scale(background_image, self.screen.get_size())
        self.screen.blit(background_img, (0, 0))
        title_rect = title_text.get_rect(
            center=(self.screen.get_rect().centerx, 80)
        )
        self.screen.blit(title_text, title_rect)
        y_offset = 150
        if self.leaderboard_tie:
            tie_text = font.render("Tie!", True, (255, 255, 255))
            tie_rect = tie_text.get_rect(
                center=(self.screen.get_rect().centerx, y_offset)
            )
            self.screen.blit(tie_text, tie_rect)
            y_offset += 50
        for idx, entry in enumerate(self.leaderboard, start=1):
            name = entry.get("name", "Player")
            status = entry.get("status", "alive")
            if self.leaderboard_ranked_by == "flags":
                flags = entry.get("flags", 0)
                line = f"{idx}. {name} - {status} - flags: {flags}"
            else:
                time_taken = entry.get("time", "-")
                line = f"{idx}. {name} - {status} - {time_taken}s"
            text = font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (80, y_offset))
            y_offset += 50
        return_text = font.render("Return to lobby", True, (255, 255, 255))
        return_rect = return_text.get_rect(
            center=(self.screen.get_rect().centerx, y_offset + 60)
        )
        self.screen.blit(return_text, return_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if return_rect.collidepoint(mx, my):
                        waiting = False


if __name__ == "__main__":
    game = Game()
    game.new()
    game.run()