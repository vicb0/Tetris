from game_objects.Piece import Piece


class O(Piece):
    def __init__(self):
        super().__init__()
    
        self.color = Piece.get_matrix_color_value("yellow")
        self.matrix = [
            [self.color, self.color],
            [self.color, self.color],
        ]
