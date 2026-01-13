import json
import os

import pygame

from menu import *
from networking import NetworkClient
from settings import Settings
# from game import Game               
# from board import Board             


class Start_Screen():


    def __init__(self):
        data2 = self.load_resolution()

        pygame.init()
        self.current_track = None
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.E_KEY = (
            False,
            False,
            False,
            False,
            False,
        )
        self.DISPLAY_W, self.DISPLAY_H = int(data2["width"]), int(data2["width"])
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

        self.resolution = Resolution(self)
        self.multiplayer_menu = MultiplayerMenu(self)
        self.name_menu = NameEntryMenu(self)
        self.room_menu = RoomMenu(self)
        self.lobby_menu = LobbyMenu(self)
        self.lobby_settings_menu = LobbySettingsMenu(self)
        # self.custplay = CustomPlay(self)
        self.curr_menu = self.main_menu
        self.lost_menu = self.main_menu
        self.network_client = None
        self.multiplayer_state = {
            "player_id": None,
            "room_code": None,
            "host_id": None,
            "players": [],
            "settings": {"rows": 10, "cols": 10, "probability": 0.15, "width": 720},
            "seed": None,
            "start_time": None,
            "leaderboard": [],
        }
        self.player_name = self.load_player_name()
        self.next_multiplayer_action = None
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
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_e:
                    self.E_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
        self.poll_network()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.E_KEY = (
            False,
            False,
            False,
            False,
            False,
        )

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

    def load_resolution(self):
        path = "jsons/resx.json"
        if os.path.exists(path):
            with open(path, "r") as file_handle:
                return json.load(file_handle)
        return {"width": 720}

    def load_player_name(self):
        path = "jsons/player_name.json"
        if os.path.exists(path):
            with open(path, "r") as file_handle:
                data = json.load(file_handle)
            return str(data.get("name", "")).strip()
        return ""

    def ensure_network(self):
        if self.network_client is None:
            server_url = os.environ.get("MULTIPLAYER_SERVER_URL", "ws://localhost:8765")
            self.network_client = NetworkClient(server_url)
        return self.network_client

    def poll_network(self):
        if not self.network_client:
            return
        for message in self.network_client.get_messages():
            message_type = message.get("type")
            payload = message.get("payload", {})
            if message_type in ("room_created", "room_joined", "lobby_update"):
                self.multiplayer_state["room_code"] = payload.get("code")
                self.multiplayer_state["host_id"] = payload.get("host_id")
                self.multiplayer_state["players"] = payload.get("players", [])
                self.multiplayer_state["settings"] = payload.get("settings", {})
                if payload.get("player_id"):
                    self.multiplayer_state["player_id"] = payload.get("player_id")
            elif message_type == "game_started":
                self.multiplayer_state["seed"] = payload.get("seed")
                self.multiplayer_state["start_time"] = payload.get("start_time")
                self.multiplayer_state["settings"] = payload.get("settings", {})
                if payload.get("players") is not None:
                    self.multiplayer_state["players"] = payload.get("players", [])
                self.start_multiplayer_game()
            elif message_type == "game_finished":
                self.multiplayer_state["leaderboard"] = payload.get("leaderboard", [])
            elif message_type == "game_update":
                self.multiplayer_state["players"] = payload.get("players", [])

    def start_multiplayer_game(self):
        from game import Game
        settings_data = self.multiplayer_state.get("settings", {})
        rows = settings_data.get("rows", 10)
        cols = settings_data.get("cols", rows)
        probability = settings_data.get("probability", 0.15)
        width = settings_data.get("width", self.DISPLAY_W)
        game_settings = Settings.from_values(rows, cols, probability, width)
        multiplayer = {
            "client": self.network_client,
            "seed": self.multiplayer_state.get("seed"),
            "start_time": self.multiplayer_state.get("start_time"),
            "players": self.multiplayer_state.get("players", []),
            "room_code": self.multiplayer_state.get("room_code"),
            "player_id": self.multiplayer_state.get("player_id"),
        }
        game = Game(settings=game_settings, multiplayer=multiplayer)
        game.new()
        game.run()
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.curr_menu = self.lobby_menu
        self.current_track = None
        self.play_music("music/menu.mp3")