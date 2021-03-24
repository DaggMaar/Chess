
from Pieces.Piece_Functions import opposite_color

class Piece:
    '''Class representing a piece in chess game'''

    def __init__(self, coordinates,unicode, piece, color='', offsets=None):
        self.color = color
        self.piece = piece
        self.code = color + piece
        self.coordinates = coordinates
        self.offsets = offsets
        self.unicode = unicode

    def is_empty(self):
        return False

    def legal_moves(self, board):
        return []

    def legal_kill_moves(self, board):
        return self.legal_moves(board)

