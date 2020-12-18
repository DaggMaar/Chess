import numpy as np
import matplotlib.pyplot as plt

class Chess:
    def __init__(self):
        self.colors = {
            True: 'W',
            False: 'B'}

        self.UNICODE_PIECES = {
            'BR': u'♜', 'BN': u'♞', 'BB': u'♝', 'BQ': u'♛',
            'BK': u'♚', 'BP': u'♟', 'WR': u'♖', 'WN': u'♘',
            'WB': u'♗', 'WQ': u'♕', 'WK': u'♔', 'WP': u'♙',
            None: ' '
        }

        self.anti_color = {
            'B' : 'W',
            'W' : 'B'
        }

        self.color = {
            'W' : 'W',
            'B' : 'B'
        }

        self.bullet = u'•'
        self.circle = u'◯'

        self.board = self.init_board()
        self.copy_board = None
        self.chess_diagram = self.init_diagram()
        self.turn = True  # white
        self.unicode_board = None
        self.selected = False #selection mode
        self.moved = False #move mode
        self.selected_x = None
        self.selected_y = None
        self.move_x = None
        self.move_y = None
        self.fig, self.ax = plt.subplots(figsize=(8,8))
        self.color_map = self.init_colormap()
        self.deselected_color = None
        self.white_score = 0
        self.black_score = 0
        self.check = False
        self.check_mate = False
        self.wins = ''
        self.white_killed = ''
        self.black_killed = ''
        self.castle_moves = {'a1' : False,
                             'e1' : False,
                             'h1': False,
                             'a8': False,
                             'e8': False,
                             'h8': False} #left rook - king - white rook
        #print(self.chess_diagram[7][7])
        self.print_board()

    def play(self):
        self.print_board()

    def castle(self, field_from, field_to):

        if (field_from, field_to) == ('e1', 'c1'):
            moving_str = ('e1', 'a1')
            none_fields = [(7, 3), (7, 2), (7, 1)]
            castle_fields = none_fields + [(7, 0)]
            new_king = (7, 2)
            new_rook = (7, 3)
            old_king = (7, 4)
            old_rook = (7, 0)

            king = 'WK'
            rook = 'WR'

        elif (field_from, field_to) == ('e1', 'g1'):
            moving_str = ['e1', 'h1']
            none_fields = [(7, 6), (7, 5)]
            castle_fields = none_fields + [(7, 7)]
            new_king = (7, 6)
            new_rook = (7, 5)
            old_king = (7, 4)
            old_rook = (7, 7)
            king = 'WK'
            rook = 'WR'

        elif (field_from, field_to) == ('e8', 'c8'):
            moving_str = ['e8', 'a8']
            none_fields = [(0, 1), (0, 2), (0, 3)]
            castle_fields = none_fields + [(0, 0)]
            new_king = (0, 2)
            new_rook = (0, 3)
            old_king = (0, 4)
            old_rook = (0, 0)
            king = 'BK'
            rook = 'BR'

        elif (field_from, field_to) == ('e8', 'g8'):
            moving_str = ['e8', 'h8']
            none_fields = [(0, 6), (0, 5)]
            castle_fields = none_fields + [(0, 7)]
            new_king = (0, 6)
            new_rook = (0, 5)
            old_king = (0, 4)
            old_rook = (0, 7)
            king = 'BK'
            rook = 'BR'

        if not self.castle_moves[moving_str[0]] and not self.castle_moves[moving_str[1]] and not self.check:
            for x, y in none_fields:
                if self.board[x][y] is not None:
                    print('fields between are not none')
                    return False

            moves = []
            for x, row in enumerate(self.board):
                for y, piece in enumerate(row):
                    if piece is not None and piece[0] is self.anti_color[piece[0]]:
                        moves += self.legal_moves(x, y, piece[1], self.anti_color[piece[0]], mode='killmove')

            for x, y in moves:
                if (x, y) in castle_fields:
                    print('something\'s pointng')
                    return False

            self.board[new_king[0]][new_king[1]] = king
            self.board[new_rook[0]][new_rook[1]] = rook
            self.board[old_king[0]][old_king[1]] = None
            self.board[old_rook[0]][old_rook[1]] = None

    def count_score(self, piece, color): #color gets points
        points = 0
        if piece == 'P':
            points = 1
        elif piece in ['B', 'N']:
            points = 2
        elif piece == 'R':
            points = 4
        elif piece == 'Q':
            points = 9

        if color == 'W':
            self.white_score += points
        elif color == 'B':
            self.black_score += points

    def on_click(self, event):
        if self.check_mate:
            return

        if event.xdata is None or event.ydata is None:
            return

        reverse = [7, 6, 5, 4, 3, 2, 1, 0]
        if self.turn:
            x = round(event.ydata)
            y = round(event.xdata)
            colormap_x = x
            colormap_y = y
        else:
            x = reverse[round(event.ydata)]
            y = reverse[round(event.xdata)]
            colormap_x = reverse[x]
            colormap_y = reverse[y]

        chosen_piece = self.board[x][y] # White, Black or None

        if not self.selected:
            if chosen_piece is None or (self.turn and chosen_piece[0] == 'B') or (not self.turn and chosen_piece[0] == 'W'):
                print('You cannot select that item.')
                return

            self.selected_x = x
            self.selected_y = y
            self.selected = True

            moves = self.legal_moves(x, y, self.board[x][y][1], self.colors[self.turn], mode='killmove')
            print(moves)
            if not self.turn:
                moves = [(reverse[x], reverse[y]) for x, y in moves]

            #for move_x, move_y in moves:
            #    self.color_map[move_x][move_y] = abs(self.color_map[move_x][move_y] - 0.008)

            self.color_map[colormap_x][colormap_y] = 0.05
            self.print_board(redraw=True, moves=moves)
            print('You selected :', self.chess_diagram[x][y])

        elif not self.moved and self.selected:
            selected = self.board[self.selected_x][self.selected_y]

            if chosen_piece is not None and selected is not None and selected[0] is chosen_piece[0]:
                self.color_map = self.init_colormap()
                self.selected_x = x
                self.selected_y = y

                moves = self.legal_moves(x, y, self.board[x][y][1], self.colors[self.turn], mode='killmove')
                print(moves)
                if not self.turn:
                    moves = [(reverse[x], reverse[y]) for x, y in moves]

                #for move_x, move_y in moves:
                #    self.color_map[move_x][move_y] = abs(self.color_map[move_x][move_y] - 0.006)

                self.color_map[colormap_x][colormap_y] = 0.05
                self.print_board(redraw=True, moves=moves)
                print('You selected :', self.chess_diagram[x][y])
                return

            if (self.turn and chosen_piece == 'W') or (not self.turn and chosen_piece == 'B'):
                self.ax.set_title('You cannot move here')
                print('You cannot move here.')
                return
            self.move_x = x
            self.move_y = y
            self.moved = True

            print('You are moving to :', self.chess_diagram[x][y])

            self.move(self.selected_x, self.selected_y, self.move_x, self.move_y) #perform move

            self.color_map = self.init_colormap()

            self.print_board(redraw=True)

            #clean selections
            self.selected = False
            self.moved = False
            self.selected_x = None
            self.selected_y = None
            self.move_x = None
            self.move_y = None

        else:
            return
            #TO-DO Co tu musi być? Error?

    def init_colormap(self):
        color_map = np.zeros(shape=(8, 8))
        color_map[1::2, 0::2] = 0.1
        color_map[0::2, 1::2] = 0.1
        return color_map

    def init_diagram(self):
        alphabet = 'abcdefgh'
        numbers = '87654321'
        chess_diagram = [letter + number for number in numbers for letter in alphabet]
        return np.array(chess_diagram).reshape(8, 8)

    def init_board(self):
        board = []
        for x in range(8):
            board.append([None for y in range(8)])

        board[0][0] = board[0][7] = 'BR'
        board[0][1] = board[0][6] = 'BN'
        board[0][2] = board[0][5] = 'BB'
        board[0][3] = 'BQ'
        board[0][4] = 'BK'

        board[7][0] = board[7][7] = 'WR'
        board[7][1] = board[7][6] = 'WN'
        board[7][2] = board[7][5] = 'WB'
        board[7][3] = 'WQ'
        board[7][4] = 'WK'

        for x in range(8):
            board[1] = ['BP' for x in range(8)]
            board[6] = ['WP' for x in range(8)]

        return np.array(board)

    def print_board(self, redraw=False, moves=[]):
        self.unicode_board = [[self.UNICODE_PIECES[x] for x in row] for row in self.board]
        if not self.turn:
            self.unicode_board = [row[::-1] for row in self.unicode_board]
            self.unicode_board = self.unicode_board[::-1]

        if redraw:
            self.ax.clear()

        self.ax.imshow(self.color_map, cmap='ocean')
        if self.check and not self.check_mate:
            self.ax.set_title('CHECK')
        elif self.check_mate:
            self.ax.set_title('CHECK MATE')
        else:
            self.ax.set_title('{2} White: {0}, Black: {1} {3}'.format( self.white_score, self.black_score, self.black_killed, self.white_killed))

        x_ticks = [0, 1, 2, 3, 4, 5, 6, 7]
        y_ticks = [0, 1, 2, 3, 4, 5, 6, 7]

        x_ticks_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        y_ticks_letters = ['8', '7', '6', '5', '4', '3', '2', '1']

        if not self.turn:
            x_ticks_letters = x_ticks_letters[::-1]
            y_ticks_letters = y_ticks_letters[::-1]

        self.ax.set_yticks(y_ticks)
        self.ax.set_yticklabels(y_ticks_letters)
        self.ax.set_xticks(x_ticks)
        self.ax.set_xticklabels(x_ticks_letters)

        for text in self.fig.texts:
            text.remove()

        for row_index, row in enumerate(self.unicode_board):
            for col_index, unicode in enumerate(row):
                plt.text(col_index - 0.33, row_index + 0.25, s=unicode, fontsize=40)

        for x, y in moves:
            if not self.turn:
                reverse = [7,6,5,4,3,2,1,0]
                cor_x = reverse[x]
                cor_y = reverse[y]
            else:
                cor_x = x
                cor_y = y

            if self.board[cor_x][cor_y] is None:
                plt.text(y - 0.21, x + 0.26, s=self.bullet, fontsize=40,  color='grey')
            else:
                plt.text(y - 0.505, x + 0.23, s=self.circle, fontsize=50, color='grey')

        if not redraw:
            self.fig.canvas.mpl_connect('button_press_event', self.on_click)
            plt.show()
        else:
            plt.draw()

    def after_move(self, from_x, from_y):
        self.unicode_board = [[self.UNICODE_PIECES[x] for x in row] for row in self.board]
        check = self.isCheck(self.colors[self.turn])
        if check:
            print('Check')
            self.check = True
            if self.isCheckMate(self.colors[self.turn]):
                print('Check-Mate')
                self.wins = self.colors[self.turn]
                self.check_mate = True
                return
        else:
            if self.chess_diagram[from_x][from_y] in self.castle_moves.keys():
                self.castle_moves[self.chess_diagram[from_x][from_y]] = True
            self.check = False
        self.turn = not self.turn

    def move(self, from_x, from_y, to_x, to_y):
        piece = self.board[from_x][from_y]
        piece_to = self.board[to_x][to_y]

        field_from = self.chess_diagram[from_x][from_y]
        field_to = self.chess_diagram[to_x][to_y]

        if (field_from, field_to) in [('e1', 'c1'), ('e1', 'g1'), ('e8', 'c8'), ('e8', 'g8')]:
            self.castle(field_from, field_to)
            self.after_move(from_x, from_y)

        elif self.isMovePossible(from_x, from_y, to_x, to_y):
            if self.turn and piece_to == 'BK':
                print('White wins')
            elif not self.turn and piece_to == 'WK':
                print('Black wins')

            if piece_to is not None:
                self.count_score(piece_to[1], self.colors[self.turn])

            if piece_to in ['BK', 'WK']:
                self.check_mate = True

            self.board[to_x][to_y] = piece  # move pawn
            self.board[from_x][from_y] = None  # empty field

            if self.turn and piece_to is not None:
                self.black_killed += self.UNICODE_PIECES[piece_to]
            elif not self.turn and piece_to is not None:
                self.white_killed += self.UNICODE_PIECES[piece_to]

            self.after_move(from_x, from_y)

    def isMovePossible(self, from_x, from_y, to_x, to_y):

        if from_x == to_x and from_y == to_y:
            return False

        turn = self.board[from_x][from_y][0]  # whose turn: black or white
        if not self.colors[self.turn] == turn:
            print('It is not your turn.')
            return False

        if to_x not in range(8) or to_y not in range(8):  # move out of range
            print('The place you want to move to it out of board.')
            return False

        piece = self.board[from_x][from_y][1]
        piece_color = self.board[from_x][from_y][0]
        move_to = self.board[to_x][to_y]
        if move_to:
            color_to = self.board[to_x][to_y][0] # color in place to move to
        else:
            color_to = None

        if move_to is not None:  # cannot jumpt to same color place
            if (self.turn and color_to == 'W') or (not self.turn and color_to == 'B'):
                return False

        if piece == 'P':  # pawn
            if self.turn:  # white moves up, black moves down
                offset = -1
                first_offset = -2
                first_row = 6
            else:
                offset = 1
                first_offset = 2
                first_row = 1

            if to_y == from_y and to_x == from_x + first_offset: #pawn first move two up
                if not (from_x == first_row and self.board[from_x + offset][from_y] is None) :
                    return False
            elif to_y == from_y and to_x == from_x + offset:  # pawn one up
                if move_to is not None:
                    return False
            elif (to_y == from_y - offset and to_x == from_x + offset) or (to_y == from_y + offset and to_x == from_x + offset): # pawn kills oponent
                if not (move_to is not None and color_to is not piece_color):
                    return False
            else: #otherwise an illegal move
                return False

        elif piece == 'N':  # knight
            if not ((to_x in [from_x + 2, from_x - 2] and to_y in [from_y + 1, from_y - 1]) or (to_x in [from_x + 1, from_x - 1] and to_y in [from_y + 2, from_y - 2])): #knight's moves
                return False

        elif piece == 'B':  # bishop
            diff_x = to_x - from_x
            diff_y = to_y - from_y

            direction_x = 1 if diff_x > 0 else -1
            direction_y = 1 if diff_y > 0 else -1

            if not (abs(diff_x) == abs(diff_y)): #bishop's moves
                return False

            for step in range(1, abs(diff_x)): #check if there's a piece on bishop's way
                if self.board[from_x + direction_x * step][from_y + direction_y * step] is not None:
                    return False

        elif piece == 'R':  # rook
            diff_x = to_x - from_x
            diff_y = to_y - from_y

            if diff_x < 0: #move left
                direction_x = -1
                direction_y = 0
            elif diff_x > 0: #move right
                direction_x = 1
                direction_y = 0
            elif diff_y < 0: #move down
                direction_x = 0
                direction_y = -1
            elif diff_y > 0: #move up
                direction_x = 0
                direction_y = 1

            if not (to_y == from_y or to_x == from_x): #rook's moves
                return False

            for step in range(1, abs(diff_x)): #check if there's a piece on rook's way
                if self.board[from_x + direction_x * step][from_y + direction_y * step] is not None:
                    return False

        elif piece == 'Q':  # queen
            diff_x = to_x - from_x
            diff_y = to_y - from_y

            if diff_x > 0:
                direction_x = 1
            elif diff_x < 0:
                direction_x = -1
            else:
                direction_x = 0

            if diff_y > 0:
                direction_y = 1
            elif diff_y < 0:
                direction_y = -1
            else:
                direction_y = 0

            if not ((abs(to_x - from_x) == abs(to_y - from_y)) or (to_y == from_y or to_x == from_x)): #queen's moves are rook's moves with bishop's moves
                return False

            for step in range(1, abs(diff_x)): #check if there's a pawn on queen's way
                if self.board[from_x + direction_x * step][from_y + direction_y * step] is not None:
                    return False

        elif piece == 'K':  # king
            if not (abs(to_x - from_x) == 1 or abs(to_y - from_y) == 1):
                return False

            if (self.turn and color_to == 'W') or (not self.turn and color_to == 'B'):
                return False

        return True

    def isCheck(self, color): #color which can generate check if moves

        moves = []
        for x, row in enumerate(self.board):
            for y, piece in enumerate(row):
                if piece is not None and piece[0] == color: #check all possible moves of all pawns of that color
                    moves += self.legal_moves(x, y, piece[1], color)

        for check_x, check_y in moves: # check if there's oponent's king on routes
            if color == 'W' and self.board[check_x][check_y] == 'BK':
                return True
            if color == 'B' and self.board[check_x][check_y] == 'WK':
                return True

        return False

    def isCheckMate(self, color):

        self.temp_board = self.board.copy()
        moves=[]
        #if self.isCheck(color):
        for x, row in enumerate(self.board):
            for y, piece in enumerate(row):
                if piece is not None and piece[0] is self.anti_color[color]:
                    moves = self.legal_moves(x, y, piece[1], self.anti_color[color])
                    for to_x, to_y in moves:
                        piece = self.board[x][y]
                        piece_to = self.board[to_x][to_y]
                        self.board[to_x][to_y] = piece  # move pawn
                        self.board[x][y] = None  # empty field
                        if not self.isCheck(color):
                            self.board = self.temp_board
                            self.temp_board = None
                            return False

                        self.board[to_x][to_y] = piece_to
                        self.board[x][y] = piece

        self.board = self.temp_board
        self.temp_board = None
        return True

    def legal_moves(self, x, y, piece, color, mode='kill'): #bishop, rook, queen, knight, king
        if color == 'B': # color which can check & which moves
            king = 'WK'
        elif color == 'W':
            king = 'BK'
        else:
            king = ''

        moves = []
        blocked = [False, False, False, False]

        if piece == 'B': # bishop
            offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        elif piece == 'R': # rook
            offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        elif piece == 'Q': #queen
            offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            blocked += blocked
        elif piece == 'N':  # knight
            offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        elif piece == 'K':  # king
            offsets = [(1, 1), (1, -1), (1, 0), (-1, 1), (-1, -1), (-1, 0), (0, 1), (0, -1)]
        else:
            offsets = []

        if piece in ['B', 'R', 'Q']:
            for dist in range(1, 8):
                for index, offset in enumerate(offsets):
                    off_x, off_y = offset
                    if not blocked[index]:
                        row = x + dist * off_x #calculate new coordinates
                        col = y + dist * off_y
                        if row not in range(8) or col not in range(8): #out of range
                            blocked[index] = True
                            continue

                        piece_to = self.board[row][col] #piece in new coordinates

                        if piece_to is not None and piece_to[0] is self.color[color] and piece_to is not king: #something's on way - block that route
                            blocked[index] = True
                            continue #skip

                        if piece_to is not None and piece_to[0] is self.anti_color[color]:
                            blocked[index] = True

                        moves.append((row, col))

        elif piece in ['N', 'K']:
            for off_x, off_y in offsets:
                row = x + off_x
                col = y + off_y
                if row not in range(8) or col not in range(8):
                    continue

                piece_to = self.board[row][col]

                if piece_to is None or piece_to[0] is self.anti_color[color]: #empty or other color - can move
                    moves.append((row, col))

        elif piece == 'P':
            if mode == 'kill' or mode == 'killmove':
                if color == 'W':  # white moves down, black moves up
                    row_offset = -1
                elif color == 'B':
                    row_offset = 1

                col_offsets = [1, -1]

                for col_offset in col_offsets:
                    row = x + row_offset
                    col = y + col_offset
                    print(row, col)

                    if row in range(8) and col in range(8):
                        piece_to = self.board[row][col]
                        print(piece_to)

                        if piece_to is not None and piece_to[0] is self.anti_color[color]:
                            moves.append((row, col))

            if mode == 'move' or mode == 'killmove':
                if color == 'W':  # white moves down, black moves up
                    row_offset = -1
                    first_offset = -2
                    first_row = 6
                elif color == 'B':
                    row_offset = 1
                    first_offset = 2
                    first_row = 1

                if x == first_row:
                    if x + first_offset in range(8) and self.board[x + first_offset][y] is None:
                        moves.append((x + first_offset, y))

                if x + row_offset in range(8) and self.board[x + row_offset][y] is None: #can only move up if empty
                        moves.append((x + row_offset, y))

        return moves

if __name__ == '__main__':
    chess = Chess()
    #chess.play()