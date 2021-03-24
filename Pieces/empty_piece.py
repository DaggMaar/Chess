from Pieces.Piece import Piece

class Empty(Piece):
    def __init__(self, coordinates):
        Piece.__init__(self, coordinates, u'', '-')

    def is_empty(self):
        return True
