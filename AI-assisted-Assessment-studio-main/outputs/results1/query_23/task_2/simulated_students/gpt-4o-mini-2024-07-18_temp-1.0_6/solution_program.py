class ChessBoard:
    def __init__(self):
        pass

    def is_valid_move(self, piece, start, end):
        start_col, start_row = start[0], int(start[1])
        end_col, end_row = end[0], int(end[1])

        # Convert letters to numbers for easier calculation
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')

        if piece == 'Rook':
            # Rook moves in the same column or row
            return start_col_num == end_col_num or start_row == end_row
        elif piece == 'Bishop':
            # Bishop moves diagonally
            return abs(start_col_num - end_col_num) == abs(start_row - end_row)
        return False
