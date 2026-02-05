import pygame

from consts.colors import WHITE
from components.Text import Text
from utils.drawUtils import draw_outlined_rect


class PieceHolder:
    def __init__(self, game, grid):
        self.game = game
        self.grid = grid
        self.piece = None

        self.x_start = (self.game.screen.get_width() + self.grid.width * self.grid.square_size) // 2
        self.y_start = self.game.screen.get_height() - self.grid.square_size * 8

        self.hold_text = Text(
            "Hold",
            pygame.font.SysFont(None, self.game.screen.get_height() // 12),
            (self.x_start + self.grid.square_size, self.y_start),
            WHITE
        )

    def draw(self, screen):
        self.hold_text.draw(screen)

        if self.piece is None:
            return

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
