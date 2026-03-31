class ChessBoard:
    def __init__(self):
        pass

    def is_valid_move(self, piece, start, end):
        start_col = ord(start[0]) - ord('a')  # Convert 'a'-'h' to 0-7
        start_row = int(start[1]) - 1          # Convert '1'-'8' to 0-7
        end_col = ord(end[0]) - ord('a')      
        end_row = int(end[1]) - 1              

        if piece == 'Rook':
            return start_col == end_col or start_row == end_row
        elif piece == 'Bishop':
            return abs(start_col - end_col) == abs(start_row - end_row)
        else:
            return False