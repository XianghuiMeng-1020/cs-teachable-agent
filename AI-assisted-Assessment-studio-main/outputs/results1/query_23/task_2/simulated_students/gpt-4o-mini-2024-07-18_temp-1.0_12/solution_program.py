class ChessBoard:
    def __init__(self):
        pass

    def is_valid_move(self, piece, start, end):
        start_col = start[0]
        start_row = int(start[1])
        end_col = end[0]
        end_row = int(end[1])

        # Check Rook movement
        if piece == 'Rook':
            return start_col == end_col or start_row == end_row

        # Check Bishop movement
        elif piece == 'Bishop':
            return abs(ord(start_col) - ord(end_col)) == abs(start_row - end_row)

        return False