def opposite_color(color):
    color_dict = {
        'W' : 'B',
        'B' : 'W'
    }
    if color not in color_dict.keys():
        return None

    return color_dict[color]