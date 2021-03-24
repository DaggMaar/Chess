'''Class representing a chess board in chess game'''
import matplotlib.pyplot as plt

from chess_functions import init_colormap, reverse
from chess_logic import ChessLogic
from chess_constants import BULLET, CIRCLE


class BoardGUI:
    '''Class representing a chess board in checc game'''

    def __init__(self):
        self.color_map = init_colormap()
        self.fig, self.axe= plt.subplots(figsize=(8, 8))
        self.logic = ChessLogic()
        self.selected = False

        self.print_board()

    def print_board(self, redraw=False, moves=None):
        '''Prints the chess board with all it's pawns using matplotlib'''

        unicode_board = [[x.unicode for x in row] for row in self.logic.board]
        if not self.logic.turn:
            unicode_board = [row[::-1] for row in unicode_board[::-1]]

        if redraw:
            self.axe.clear()

        self.axe.imshow(self.color_map, cmap='Pastel1')

        self.set_axes_title()
        self.set_axes_ticks()

        for row_index, row in enumerate(unicode_board):
            for col_index, unicode in enumerate(row):
                plt.text(col_index - 0.37, row_index + 0.28, s=unicode, fontsize=40)

        if moves is not None:
            for row_x, col_y in moves:
                if not self.logic.turn:
                    cor_x = reverse(row_x)
                    cor_y = reverse(col_y)
                else:
                    cor_x = row_x
                    cor_y = col_y

                if self.logic.board[cor_x][cor_y].is_empty():
                    plt.text(col_y - 0.25, row_x + 0.31, s=BULLET, fontsize=40, color='grey')
                else:
                    plt.text(col_y - 0.53, row_x + 0.23, s=CIRCLE, fontsize=46, color='grey')

        plt.plot(8, 0, marker='X', markersize=30, color='tab:blue', label='reset')

        self.axe.spines['top'].set_visible(False)
        self.axe.spines['right'].set_visible(False)
        self.axe.spines['bottom'].set_visible(False)
        self.axe.spines['left'].set_visible(False)

        if not redraw:
            self.fig.canvas.mpl_connect('button_press_event', self.on_click)
            plt.show()
        else:
            plt.draw()

    def on_click(self, event):
        '''Implements logic after clicking on a board'''
        if None in (event.xdata, event.ydata):
            return

        if round(event.xdata) not in range(9) or round(event.ydata) not in range(8)\
                or self.logic.check_mate:
            return

        if round(event.xdata) == 8 :
            if round(event.ydata) == 0:
                self.logic.reset_game()
                self.print_board(redraw=True)
                return
            return

        if self.logic.turn:
            row_x = round(event.ydata)
            col_y = round(event.xdata)
        else:
            row_x = reverse(round(event.ydata))
            col_y = reverse(round(event.xdata))

        colormap_x = round(event.ydata)
        colormap_y = round(event.xdata)

        piece = self.logic.board[row_x][col_y]

        if not self.selected and piece.color != self.logic.turn_color():
            return

        if self.selected and piece.color != self.logic.turn_color():
            self.logic.move(row_x, col_y)
            self.print_board(redraw=True)
            self.selected = False

        else:
            self.selected = True
            self.logic.from_x = row_x
            self.logic.from_y = col_y

            moves = self.logic.check_legal_moves(piece)

            if not self.logic.turn:
                moves = [(reverse(row_x), reverse(col_y)) for row_x, col_y in moves]

            self.color_map[colormap_x][colormap_y] = 0.19
            self.print_board(redraw=True, moves=moves)

        self.color_map = init_colormap()

    def set_axes_title(self):
        '''Sets axes title according to white's or black's turn'''

        if self.logic.check_mate:
            self.axe.set_title('CHECK MATE')
        elif self.logic.check:
            self.axe.set_title('CHECK')
        else:
            self.axe.set_title('{2} White: {0}, Black: {1} {3}'.format(
                self.logic.score.white_score,
                self.logic.score.black_score,
                self.logic.score.black_killed,
                self.logic.score.white_killed))

    def set_axes_ticks(self):
        '''Sets axes ticks according to white's or black's turn'''

        ticks = [0, 1, 2, 3, 4, 5, 6, 7]

        x_ticks_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        y_ticks_letters = ['8', '7', '6', '5', '4', '3', '2', '1']

        if not self.logic.turn:
            x_ticks_letters = x_ticks_letters[::-1]
            y_ticks_letters = y_ticks_letters[::-1]

        self.axe.set_yticks(ticks)
        self.axe.set_yticklabels(y_ticks_letters)
        self.axe.set_xticks(ticks)
        self.axe.set_xticklabels(x_ticks_letters)
