'''Python Chess Game'''

from chess_functions import init_board, opposite_color
from Pieces.empty_piece import Empty
from chess_score import Score
from chess_constants import CASTLE


class ChessLogic:
    '''Class implementing chess logic with an interactive GUI'''

    def __init__(self):
        self.score = Score()
        self.board = init_board()
        self.turn = True
        self.check = False
        self.check_mate = False
        self.from_x = None
        self.from_y = None

    def turn_color(self):
        '''Returns a string color of a current turn'''

        if self.turn:
            return 'W'

        return 'B'

    def castle(self, from_x, from_y, to_x, to_y):
        '''Performs a castle move logic'''

        key = (from_x, from_y, to_x, to_y)
        king = self.board[from_x][from_y]
        rook = self.board[CASTLE[key]['rook_from_x']][CASTLE[key]['rook_from_y']]

        if not king.moved and not rook.moved and not self.check:
            for row_x, col_y in CASTLE[key]['none_fields']:
                if not self.board[row_x][col_y].is_empty():
                    print('none_fields')
                    return False

            moves = []
            for row_x, row in enumerate(self.board):
                for col_y, piece in enumerate(row):
                    if not piece.is_empty() and piece.color != self.turn_color():
                        moves += piece.legal_moves(self.board)

            for row_x, col_y in moves:
                if (row_x, col_y) in CASTLE[key]['pointed_fields']:
                    print('pointing fields')
                    return False

            self.board[to_x][to_y] = self.board[from_x][from_y]
            self.board[to_x][to_y].coordinates = (to_x, to_y)

            self.board[CASTLE[key]['rook_to_x']][CASTLE[key]['rook_to_y']] = \
                self.board[CASTLE[key]['rook_from_x']][CASTLE[key]['rook_from_y']]

            self.board[CASTLE[key]['rook_to_x']][CASTLE[key]['rook_to_y']].coordinates = \
                (CASTLE[key]['rook_from_x'], CASTLE[key]['rook_from_y'])

            self.board[from_x][from_y] = Empty((from_x, from_y))

            self.board[CASTLE[key]['rook_from_x']][CASTLE[key]['rook_from_y']] = \
                Empty((CASTLE[key]['rook_from_x'], CASTLE[key]['rook_from_y']))

        return True

    def is_move_possible(self, to_x, to_y, piece):
        '''Checks if a move is possible for a given piece'''

        moves = self.check_legal_moves(piece)
        if (to_x, to_y) in moves:
            return True
        return False

    def check_legal_moves(self, piece):
        '''Checks all legal moves with regards to a possible check'''

        moves = piece.legal_moves(self.board)
        new_moves = []
        from_x, from_y = piece.coordinates

        for row_x, col_y in moves:
            piece_to = self.board[row_x][col_y]
            self.board[from_x][from_y] = Empty((row_x, col_y))
            self.board[row_x][col_y] = piece

            if not self.is_check(opposite_color(self.turn_color())):
                new_moves.append((row_x, col_y))

            self.board[from_x][from_y] = piece
            self.board[row_x][col_y] = piece_to

        return new_moves

    def move(self, to_x, to_y):
        '''Perform a move if it's possible'''
        piece = self.board[self.from_x][self.from_y]

        piece_to = self.board[to_x][to_y]

        key = (self.from_x, self.from_y, to_x, to_y)

        if key in CASTLE.keys():
            if not self.castle(self.from_x, self.from_y, to_x, to_y):
                return

        elif self.is_move_possible(to_x, to_y, piece):
            if not piece_to.is_empty():
                self.score.count_score(piece_to)
                self.score.track_killed(self.turn, piece_to)

            if piece_to.piece == 'K':
                self.check_mate = True

            if piece.piece in ['K', 'R']:
                piece.moved = True

            self.move_piece(self.from_x, self.from_y, to_x, to_y)

        else:
            return

        check = self.is_check(self.turn_color())
        if check:
            self.check = True
            if self.is_check_mate():
                self.check_mate = True
                return
        else:
            self.check = False

        self.turn = not self.turn
        self.from_x = None
        self.from_y = None

    def move_piece(self, from_x, from_y, to_x, to_y):
        '''Performs a piece's move'''

        piece = self.board[from_x][from_y]

        self.board[from_x][from_y] = Empty((from_x, from_y))
        self.board[to_x][to_y] = piece

        piece.coordinates = (to_x, to_y)

    def is_check(self, color):
        '''Checks if there's a check after move'''

        moves = []
        for row in self.board:
            for piece in row:
                if not piece.is_empty() and piece.color == color:
                    moves += piece.legal_kill_moves(self.board)

        for check_x, check_y in moves:
            if (color == 'W' and self.board[check_x][check_y].code == 'BK') \
                    or (color == 'B' and self.board[check_x][check_y].code == 'WK'):
                return True

        return False

    def reset_game(self):
        '''Resets the current chess game'''

        self.board = init_board()
        self.turn = True
        self.score = Score()

    def is_check_mate(self):
        '''Checks if there's a check mate (end of game)'''

        temp_board = self.board.copy()

        for row_x, row in enumerate(self.board):
            for col_y, piece in enumerate(row):
                if not piece.is_empty() and piece.color != self.turn_color():
                    moves = piece.legal_kill_moves(self.board)
                    for to_x, to_y in moves:
                        piece = self.board[row_x][col_y]
                        piece_to = self.board[to_x][to_y]

                        self.board[to_x][to_y] = piece
                        self.board[row_x][col_y] = Empty((row_x, col_y))

                        if not self.is_check(self.turn_color()):
                            self.board = temp_board
                            return False

                        self.board[to_x][to_y] = piece_to
                        self.board[row_x][col_y] = piece

        self.board = temp_board
        return True


if __name__ == '__main__':
    chess = ChessLogic()
