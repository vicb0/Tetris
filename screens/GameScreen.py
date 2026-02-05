import pygame

from components.Button import Button
from consts.colors import *
from game_objects.Grid import Grid
from core.ScreenInterface import ScreenInterface


class GameScreen(ScreenInterface):
    def __init__(self, game):
        super().__init__(game)

        self.drawables = []
        self.game_grid = None

        self.input_linker = {
            pygame.MOUSEMOTION: self.on_mouse_motion,
            pygame.MOUSEBUTTONDOWN: self.on_click,
            pygame.KEYDOWN: self.on_key_down
        }

    def on_key_down(self, event):
        if event.key == pygame.K_ESCAPE:
            self.game.screens_manager.set_screen("mainmenu")
        self.game_grid.key_down_handler(event)

    def on_mouse_motion(self, event):
        for obj in self.drawables:
            if getattr(obj, "handle_hover", None):
                obj.handle_hover(event)

    def on_click(self, event):
        for obj in self.drawables:
            if getattr(obj, "handle_click", None):
                obj.handle_click(event)

    def event_handler(self, event):
        func = self.input_linker.get(event.type)
        if func:
            func(event)

    def update(self, dt):
        for obj in self.drawables:
            if getattr(obj, "update", None):
                obj.update(dt)

    def draw(self):
        self.game.screen.fill(BLACK)

        for obj in self.drawables:
            if getattr(obj, "draw", None):
                obj.draw(self.game.screen)

    def on_enter(self):
        self.game.audio_manager.load_bgm("assets/Game/bgm.mp3")
        self.game.audio_manager.load_sfx("denied", "assets/Game/denied.mp3")
        self.game.audio_manager.load_sfx("point1", "assets/Game/point1.wav")
        self.game.audio_manager.load_sfx("point2", "assets/Game/point2.wav")
        self.game.audio_manager.load_sfx("point3", "assets/Game/point3.wav")
        self.game.audio_manager.load_sfx("point4", "assets/Game/point4.wav")
        self.game.audio_manager.load_sfx("gameover", "assets/Game/gameover.wav")

        self.game_grid = Grid(self.game)

        self.drawables.append(self.game_grid)
        self.drawables.append(self.game_grid.next_piece)
        self.drawables.append(self.game_grid.piece_holder)
        self.drawables.append(self.game_grid.speed_text)

        game_over_button = Button(
            text="Play again",
            font=pygame.font.SysFont(None, self.game.screen.get_height() // 12),
            rect=(
                self.game.screen.get_width() // 2,
                self.game.screen.get_height() // 2,
                self.game.screen.get_width() // 4,
                self.game.screen.get_height() // 4
            ),
            on_click=self.game_grid.reset,
            bg=RED,
            hover_bg=DARK_RED,
            center=True
        )

        prev_draw = game_over_button.draw
        def display_game_over(screen):
            if self.game_grid.game_over:
                prev_draw(screen)

        game_over_button.draw = display_game_over

        self.drawables.append(game_over_button)

        self.game.audio_manager.play_bgm()

    def on_exit(self):
        self.game.audio_manager.clear()
