'''Class representing chess score'''

class Score:
    '''Class representing chess score'''

    def __init__(self):
        self.white_score = 0
        self.black_score = 0
        self.white_killed = ''
        self.black_killed = ''

    def count_score(self, piece):
        '''Counts player's scores'''

        points = 0
        if piece.piece == 'P':
            points = 1
        elif piece.piece in ['B', 'N']:
            points = 3
        elif piece.piece == 'R':
            points = 4
        elif piece.piece == 'Q':
            points = 9

        if piece.color == 'B':
            self.white_score += points
        elif piece.color == 'W':
            self.black_score += points

    def track_killed(self, turn, piece):
        '''Tracks player's killed unicode pieces'''

        if turn:
            self.black_killed += piece.unicode
        else:
            self.white_killed += piece.unicode
