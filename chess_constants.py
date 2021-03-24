'''Module containing chess constants'''

BULLET = u'•'
CIRCLE = u'◯'

CASTLE = {
    (0, 4, 0, 6): {
        'none_fields': ((0, 6), (0, 5)),
        'pointed_fields': ((0, 6), (0, 5), (0, 7)),
        'rook_from_x': 0,
        'rook_from_y': 7,
        'rook_to_x': 0,
        'rook_to_y':  5
    },
    (0, 4, 0, 2): {
        'none_fields': ((0, 1), (0, 2), (0, 3)),
        'pointed_fields': ((0, 1), (0, 2), (0, 3), (0, 0)),
        'rook_from_x': 0,
        'rook_from_y': 0,
        'rook_to_x': 0,
        'rook_to_y': 3
    },
    (7, 4, 7, 6): {
        'none_fields': ((7, 6), (7, 5)),
        'pointed_fields': ((7, 6), (7, 5), (7, 7)),
        'rook_from_x': 7,
        'rook_from_y': 7,
        'rook_to_x': 7,
        'rook_to_y': 5
    },
    (7, 4, 7, 2): {
        'none_fields': ((7, 3), (7, 2), (7, 1)),
        'pointed_fields': ((7, 3), (7, 2), (7, 1), (7, 0)),
        'rook_from_x': 7,
        'rook_from_y': 0,
        'rook_to_x': 7,
        'rook_to_y': 3
    }
}
