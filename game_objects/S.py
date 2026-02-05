from game_objects.Piece import Piece


class S(Piece):
    def __init__(self):
        super().__init__()
    
        self.color = Piece.get_matrix_color_value("green")
        self.matrix = [
            [0, 0, 0],
            [0, self.color, self.color],
            [self.color, self.color, 0],
        ]
