class ChessBoard:
    def __init__(self):
        pass

    def is_valid_move(self, piece, start, end):
        start_col, start_row = ord(start[0]) - ord('a'), int(start[1])
        end_col, end_row = ord(end[0]) - ord('a'), int(end[1])
        
        if piece == 'Rook':
            return start_col == end_col or start_row == end_row
        elif piece == 'Bishop':
            return abs(start_col - end_col) == abs(start_row - end_row)
        return False