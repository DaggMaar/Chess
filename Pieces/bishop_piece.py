'''Cos tam'''

from Pieces.Piece import Piece
from Pieces.Piece_Functions import opposite_color

class Bishop(Piece):
    '''Class representing a Bishop piece in chess game'''

    def __init__(self, color, coordinates):
        offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        unicode = u'♗' if color == 'W' else u'♝'
        Piece.__init__(self, coordinates, unicode, 'B', color, offsets)

    def legal_moves(self, board):
        '''Generates all legal moves for a Bishop piece in chess game'''

        moves = []
        row_x, col_y = self.coordinates
        blocked = [False] * 4
        king = opposite_color(self.color) + 'K'

        for dist in range(1, 8):
            for index, offset in enumerate(self.offsets):
                offset_x, offset_y = offset
                if not blocked[index]:
                    row = row_x + dist * offset_x  # calculate new coordinates
                    col = col_y + dist * offset_y
                    if row not in range(8) or col not in range(8):  # out of range
                        blocked[index] = True
                        continue

                    piece_to = board[row][col]  # piece in new coordinates

                    if not piece_to.is_empty()\
                            and piece_to.color is self.color \
                            and piece_to is not king:
                        # something's on way - block that route
                        blocked[index] = True
                        continue  # skip

                    if not piece_to.is_empty() and piece_to.color != self.color:
                        blocked[index] = True

                    moves.append((row, col))

        return moves
