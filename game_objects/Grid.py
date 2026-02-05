import random

import pygame

from components.Text import Text
from consts.colors import *
from game_objects.NextPiece import NextPiece
from game_objects.Piece import Piece
from game_objects.I import I
from game_objects.O import O
from game_objects.PieceHolder import PieceHolder
from game_objects.T import T
from game_objects.S import S
from game_objects.Z import Z
from game_objects.L import L
from game_objects.J import J
from utils.drawUtils import draw_outlined_rect


class Grid:
    def __init__(self, game):
        self.game = game

        self.width = 10
        self.height = 20
        self.grid = self.new_grid()
        
        self.square_size = min(self.game.screen.get_size()) * 0.045
        self.colors = {
            Piece.get_matrix_color_value("red"): RED,
            Piece.get_matrix_color_value("green"): GREEN,
            Piece.get_matrix_color_value("blue"): BLUE,
            Piece.get_matrix_color_value("yellow"): YELLOW,
            Piece.get_matrix_color_value("orange"): ORANGE,
            Piece.get_matrix_color_value("cyan"): CYAN,
            Piece.get_matrix_color_value("magenta"): MAGENTA
        }

        self.pieces = {
            "I": I,
            "O": O,
            "T": T,
            "S": S,
            "Z": Z,
            "L": L,
            "J": J
        }

        self.paused = False
        self.game_over = False
        self.can_swap = True
        self.points = 0
        self.speed_up_after_every = 20
        self.interval = 1
        self.min_interval = 0.05
        self.speed_up_percentage = 0.10  # 10% every speedup
        self.elapsed_time = 0

        self.current_piece = None
        self.current_piece_pos = None

        self.points_text = Text(
            f"Points\n{str(self.points)}",
            pygame.font.SysFont(None, self.game.screen.get_height() // 12),
            (self.game.screen.get_width() // 4, self.square_size * 2.5),
            WHITE,
            center=True
        )

        self.speed_text = Text(
            f"Speed\n{str(round(1 / self.interval))}",
            pygame.font.SysFont(None, self.game.screen.get_height() // 12),
            (self.game.screen.get_width() // 4, self.game.screen.get_height() - self.square_size * 6.5),
            WHITE,
            center=True
        )

        self.next_piece = NextPiece(self.game, self)
        self.piece_holder = PieceHolder(self.game, self)
        self.speed_up()
        self.spawn_piece()

    def not_game_over_and_not_paused(func):
        def wrapper(self, *args, **kwargs):
            if not self.game_over and not self.paused:
                func(self, *args, **kwargs)
        return wrapper

    def reset(self):
        self.add_points(-self.points)
        self.grid = self.new_grid()

        self.game_over = False
        self.piece_holder.piece = None
        self.current_piece = None
        self.current_piece_pos = None
        self.spawn_piece()
        
        self.elapsed_time = 0
        self.interval = 1

    def new_grid(self):
        grid = []

        for _ in range(self.height):
            line = []

            for _ in range(self.width):
                line.append(0)

            grid.append(line)

        return grid
    
    def rotate_piece(self, clockwise=True):
        self.current_piece.rotate(clockwise)
        self.current_piece_pos[0] = max(0, min(self.width - len(self.current_piece.matrix[0]), self.current_piece_pos[0]))
        self.current_piece_pos[1] = max(0, min(self.height - len(self.current_piece.matrix), self.current_piece_pos[1]))

    @not_game_over_and_not_paused
    def key_down_handler(self, event):
        dx, dy = 0, 0
        rotated = False

        if event.key == pygame.K_RIGHT:
            dx = 1
        elif event.key == pygame.K_LEFT:
            dx = -1
        elif event.key == pygame.K_DOWN:
            dy = 1
        elif event.key == pygame.K_UP:
            prev_pos = self.current_piece_pos.copy()
            self.rotate_piece()
            rotated = True
        elif event.key == pygame.K_SPACE:
            self.fall_piece(instant=True)
        elif event.key == pygame.K_LCTRL:
            self.swap_pieces()
        else:
            return

        success = self.move_piece(dx, dy)
        if rotated and not success:
            self.rotate_piece(clockwise=False)
            self.current_piece_pos = prev_pos

    def swap_pieces(self):
        if not self.can_swap:
            self.game.audio_manager.play_sfx("denied")
            return

        self.can_swap = False
        self.erase_piece_matrix()

        if self.piece_holder.piece is None:
            self.piece_holder.piece = self.current_piece
            self.spawn_piece(check_game_over=False)
        else:
            self.piece_holder.piece, self.current_piece = self.current_piece, self.piece_holder.piece

        self.current_piece_pos = [self.width // 2 - 1, -len(self.current_piece.matrix)]

    def is_x_inbound(self, x):
        return 0 <= x < self.width

    def is_y_inbound(self, y):
        return 0 <= y < self.height

    def is_inbound(self, pos):
        return self.is_x_inbound(pos[0]) and self.is_y_inbound(pos[1])

    def speed_up(self):
        self.speedmeter = self.points // self.speed_up_after_every
        self.interval = max(self.min_interval, (1 - self.speed_up_percentage) ** self.speedmeter)
        self.speed_text.set_text(f"Speed\n{str(round(1 / self.interval, 1))}")

    def add_points(self, points):
        self.points += points
        self.points_text.set_text(f"Points\n{str(self.points)}")
        self.speed_up()

    def drop_above(self, height):
        for y in range(height, 0, -1):
            above = self.grid[y - 1].copy()
            self.grid[y] = above

    def clear_completed_lines(self):
        rows = 0
        for y, line in enumerate(self.grid):
            if not all(line):
                continue

            rows += 1
            self.drop_above(y)
        if rows == 0:
            return

        self.game.audio_manager.play_sfx("point" + str(rows))
        points = int((rows ** 2) * (1 / self.interval))
        self.add_points(points)

    def freeze_piece(self):
        self.can_swap = True
        for y, line in enumerate(self.current_piece.matrix):
            for x, _ in enumerate(line):
                new_x, new_y = self.current_piece_pos[0] + x, self.current_piece_pos[1] + y
                if self.is_inbound((new_x, new_y)) and self.grid[new_y][new_x] > 0:
                    self.grid[new_y][new_x] *= -1
        self.clear_completed_lines()

    def check_game_over(self):
        if not self.is_y_inbound(self.current_piece_pos[1]):
            self.game_over = True
            self.game.screens_manager.current_screen.game_over_button.set_enabled(True)
            self.game.screens_manager.current_screen.game_over_button.set_visible(True)
            self.game.audio_manager.play_sfx("gameover")

    def spawn_piece(self, check_game_over=True):
        if self.current_piece and check_game_over:
            self.check_game_over()

        if self.next_piece.piece:
            self.current_piece = self.next_piece.piece
        else:
            self.current_piece = self.pieces[random.choice(list(self.pieces.keys()))]()

        self.next_piece.piece = self.pieces[random.choice(list(self.pieces.keys()))]()
        self.current_piece_pos = [self.width // 2 - 1, -len(self.current_piece.matrix)]

    def erase_piece_matrix(self):
        for y, line in enumerate(self.current_piece.matrix):
            for x, _ in enumerate(line):
                new_x, new_y = self.current_piece_pos[0] + x, self.current_piece_pos[1] + y
                if self.is_inbound((new_x, new_y)) and self.grid[new_y][new_x] > 0:
                    self.grid[new_y][new_x] = 0

    def move_piece(self, dx, dy):
        rollback_grid = []
        for line in self.grid:
            rollback_grid.append(line.copy())

        self.erase_piece_matrix()

        for y, line in enumerate(self.current_piece.matrix):
            for x, value in enumerate(line):
                new_x, new_y = self.current_piece_pos[0] + x + dx, self.current_piece_pos[1] + y + dy
                if not value:
                    continue

                if not self.is_x_inbound(new_x) or \
                        new_y >= self.height or \
                        (self.is_y_inbound(new_y) and self.grid[new_y][new_x] < 0):
                    self.grid = rollback_grid
                    return False
                
                if self.is_inbound((new_x, new_y)):
                    self.grid[new_y][new_x] = value

        self.current_piece_pos[0] += dx
        self.current_piece_pos[1] += dy

        return True

    def fall_piece(self, instant=False):
        while (success := self.move_piece(0, 1)) and instant:
            pass

        if not success:
            self.freeze_piece()
            self.spawn_piece()

    @not_game_over_and_not_paused
    def update(self, dt):
        self.elapsed_time += dt

        if self.elapsed_time >= self.interval:
            actions = int(self.elapsed_time // self.interval)
            self.elapsed_time %= self.interval

            for _ in range(actions):
                self.fall_piece()

    def draw(self, screen):
        x_start = (screen.get_width() - self.width * self.square_size) // 2
        y_start = (screen.get_height() - self.height * self.square_size) // 2

        self.points_text.draw(screen)

        for y, line in enumerate(self.grid):
            for x, _ in enumerate(line):
                rect = (
                    x_start + x * self.square_size,
                    y_start + y * self.square_size,
                    self.square_size, self.square_size
                )

                draw_outlined_rect(
                    screen,
                    self.colors[abs(self.grid[y][x])] if self.grid[y][x] != 0 else BLACK,
                    rect
                )
