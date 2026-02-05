from game_objects.Piece import Piece


class I(Piece):
    def __init__(self):
        super().__init__()
    
        self.color = Piece.get_matrix_color_value("cyan")
        self.matrix = [
            [0, self.color, 0, 0],
            [0, self.color, 0, 0],
            [0, self.color, 0, 0],
            [0, self.color, 0, 0]
        ]
