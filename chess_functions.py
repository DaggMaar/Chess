'''Module containing utility functions for chess game'''

import numpy as np

from Pieces.knight_piece import Knight
from Pieces.rook_piece import Rook
from Pieces.bishop_piece import Bishop
from Pieces.queen_piece import Queen
from Pieces.king_piece import King
from Pieces.pawn_piece import Pawn
from Pieces.empty_piece import Empty


def init_board():
    '''Initializes the chess board with black and white pawns'''

    board = [[None for x in range(8)] for y in range(8)]

    for row_x in range(2,6):
        board[row_x] = [Empty((row_x, col_y)) for col_y in range(8)]

    board[0][0] = Rook('B', (0,0))
    board[0][7] = Rook('B', (0,7))
    board[0][1] = Knight('B', (0,1))
    board[0][6] = Knight('B', (0,6))
    board[0][2] = Bishop('B', (0,2))
    board[0][5] = Bishop('B', (0,5))
    board[0][3] = Queen('B', (0,3))
    board[0][4] = King('B', (0,4))

    board[7][0] = Rook('W', (7,0))
    board[7][7] = Rook('W', (7,7))
    board[7][1] = Knight('W', (7,1))
    board[7][6] = Knight('W', (7,6))
    board[7][2] = Bishop('W', (7,2))
    board[7][5] = Bishop('W', (7,5))
    board[7][3] = Queen('W', (7,3))
    board[7][4] = King('W', (7,4))

    board[1] = [Pawn('B', (1, x)) for x in range(8)]
    board[6] = [Pawn('W', (6, x)) for x in range(8)]

    return np.array(board)


# def init_colormap():
#     '''Initializes the colormap'''
#
#     color_map = np.zeros(shape=(8, 8))
#     color_map[1::2, 0::2] = 0.1
#     color_map[0::2, 1::2] = 0.1
#     return color_map

def init_colormap():
    '''Initializes the colormap'''

    color_map = np.zeros(shape=(8, 9))
    color_map[1::2, 0::2] = 0.1
    color_map[0::2, 1::2] = 0.1
    for row in color_map:
        row[8] = 0.19
    return color_map

def opposite_color(color):
    '''Returns a reverse color for chess turns'''

    color_dict = {
        'W': 'B',
        'B': 'W'
    }
    if color not in color_dict.keys():
        return None

    return color_dict[color]


def reverse(index):
    '''Reverses index coordinate according to reverse array'''
    reverse_array = [7, 6, 5, 4, 3, 2, 1, 0]
    return reverse_array[index]
