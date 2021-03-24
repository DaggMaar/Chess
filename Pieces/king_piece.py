import numpy as np
from Pieces.Piece import Piece

class King(Piece):
    def __init__(self, color, coordinates):
        offsets = [(1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (-1, 0), (0, 1), (0, -1)]
        unicode = u'♔' if color == 'W' else u'♚'
        Piece.__init__(self, coordinates, unicode, 'K', color, offsets)

        self.moved = False

    def legal_moves(self, board):
        '''Generates all legal moves for a King piece in chess game'''

        moves = []
        row_x, col_y = self.coordinates
        for off_x, off_y in self.offsets:
            row = row_x + off_x
            col = col_y + off_y

            if row not in range(8) or col not in range(8):
                continue

            piece_to = board[row][col]

            if piece_to.is_empty() or piece_to.color != self.color:
                moves.append((row, col))

        return moves
