class ChessBoard:
    
    def __init__(self):
        pass

    def is_valid_move(self, piece, start, end):
        start_col, start_row = start
        end_col, end_row = end

        start_row = int(start_row)
        end_row = int(end_row)

        if piece == 'Rook':
            return start_col == end_col or start_row == end_row
        elif piece == 'Bishop':
            col_diff = abs(ord(start_col) - ord(end_col))
            row_diff = abs(start_row - end_row)
            return col_diff == row_diff
        return False