from game_objects.Piece import Piece


class Z(Piece):
    def __init__(self):
        super().__init__()
    
        self.color = Piece.get_matrix_color_value("red")
        self.matrix = [
            [0, 0, 0],
            [self.color, self.color, 0],
            [0, self.color, self.color],
        ]
