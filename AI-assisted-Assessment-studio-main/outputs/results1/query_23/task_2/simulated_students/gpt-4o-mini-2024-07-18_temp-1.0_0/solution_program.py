class ChessBoard:
    def __init__(self):
        pass

    def is_valid_move(self, piece, start, end):
        start_col, start_row = start[0], int(start[1])
        end_col, end_row = end[0], int(end[1])

        col_start_index = ord(start_col) - ord('a')
        col_end_index = ord(end_col) - ord('a')

        if piece == 'Rook':
            return col_start_index == col_end_index or start_row == end_row
        elif piece == 'Bishop':
            return abs(col_start_index - col_end_index) == abs(start_row - end_row)
        else:
            return False