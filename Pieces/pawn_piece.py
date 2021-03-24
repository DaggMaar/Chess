from Pieces.Piece import Piece


class Pawn(Piece):
    '''Class representing a Pawn piece in chess game'''

    def __init__(self, color, coordinates):
        unicode = u'♙' if color == 'W' else u'♟'
        Piece.__init__(self, coordinates, unicode, 'P', color)

        self.row_offset = 1 if self.color == 'B' else -1
        self.first_offset = 2 if self.color == 'B' else -2
        self.first_row = 1 if self.color == 'B' else 6

    def legal_moves(self, board):
        '''Generates all legal moves for a Pawn piece in chess game'''

        moves = self.legal_kill_moves(board)

        row_x, col_y = self.coordinates

        row_index = row_x + self.first_offset
        if row_x == self.first_row and row_index in range(8) and board[row_index][col_y].is_empty():
            moves.append((row_x + self.first_offset, col_y))

        row_index = row_x + self.row_offset
        if row_index in range(8) and board[row_index][col_y].is_empty():
            moves.append((row_x + self.row_offset, col_y))

        return moves

    def legal_kill_moves(self, board):
        '''Killing moves only'''

        moves = []
        row_x, col_y = self.coordinates

        col_offsets = [1, -1]

        for col_offset in col_offsets:
            row = row_x + self.row_offset
            col = col_y + col_offset

            if row in range(8) and col in range(8):
                piece_to = board[row][col]

                if not piece_to.is_empty() and piece_to.color != self.color:
                    moves.append((row, col))

        return moves