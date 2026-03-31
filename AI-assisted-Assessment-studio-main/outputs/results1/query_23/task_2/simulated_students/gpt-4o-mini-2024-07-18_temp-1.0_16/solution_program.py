class ChessBoard:
    def __init__(self):
        pass

    def is_valid_move(self, piece, start, end):
        def convert_position(pos):
            column = ord(pos[0]) - ord('a') + 1
            row = int(pos[1])
            return (row, column)

        start_row, start_col = convert_position(start)
        end_row, end_col = convert_position(end)

        if piece == 'Rook':
            return start_row == end_row or start_col == end_col
        elif piece == 'Bishop':
            return abs(start_row - end_row) == abs(start_col - end_col)
        else:
            return False