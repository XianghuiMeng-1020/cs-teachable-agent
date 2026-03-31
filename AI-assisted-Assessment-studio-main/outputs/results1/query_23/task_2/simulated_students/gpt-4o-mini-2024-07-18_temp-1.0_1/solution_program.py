class ChessBoard:
    def __init__(self):
        self.columns = 'abcdefgh'
        self.rows = '12345678'

    def is_valid_move(self, piece, start, end):
        start_column, start_row = start[0], start[1]
        end_column, end_row = end[0], end[1]
        
        if piece == 'Rook':
            return (start_column == end_column) or (start_row == end_row)
        elif piece == 'Bishop':
            return abs(ord(start_column) - ord(end_column)) == abs(int(start_row) - int(end_row))
        return False
