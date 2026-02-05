from consts.colors import *


class Piece:
    colors = {
        "red": 1,
        "green": 2,
        "blue": 3,
        "yellow": 4,
        "orange": 5,
        "cyan": 6,
        "magenta": 7
    }

    def __init__(self):
        self.color = None
        self.matrix = None

    @staticmethod
    def get_matrix_color_value(color):
        return Piece.colors.get(color.lower())

    def rotate(self, clockwise=True):
        if not self.matrix:
            return
        
        n, m = len(self.matrix), len(self.matrix[0])
        new_matrix = [[0 for _ in range(n)] for _ in range(m)]

        for i in range(n):
            for j in range(m):
                if clockwise:
                    new_matrix[j][n - i - 1] = self.matrix[i][j]
                else:
                    new_matrix[m - j - 1][i] = self.matrix[i][j]

        self.matrix = new_matrix
