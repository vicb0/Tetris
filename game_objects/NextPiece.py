import pygame

from consts.colors import *
from components.Text import Text
from utils.drawUtils import draw_outlined_rect


class NextPiece:
    def __init__(self, game, grid):
        self.game = game
        self.grid = grid

        self.x_start = (self.game.screen.get_width() + self.grid.width * self.grid.square_size) // 2
        self.y_start = (self.game.screen.get_height() - self.grid.height * self.grid.square_size) // 2

        self.piece = None
        self.next_text = Text(
            "Next",
            pygame.font.SysFont(None, self.game.screen.get_height() // 12),
            (self.x_start + self.grid.square_size, self.y_start),
            WHITE
        )

    def draw(self, screen):
        self.next_text.draw(screen)

        for y, line in enumerate(self.piece.matrix):
            for x, _ in enumerate(line):
                if self.piece.matrix[y][x] == 0:
                    continue

                rect = (
                    self.x_start + (x + 1) * self.grid.square_size,
                    self.y_start + (y + 2) * self.grid.square_size,
                    self.grid.square_size, self.grid.square_size
                )

                draw_outlined_rect(
                    screen,
                    self.grid.colors[self.piece.color],
                    rect
                )
