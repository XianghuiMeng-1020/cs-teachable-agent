class ChessBoard:
    def __init__(self):
        pass

    def is_valid_move(self, piece, start, end):
        # Convert board positions to numeric coordinates
        start_col = ord(start[0]) - ord('a') + 1
        start_row = int(start[1])
        end_col = ord(end[0]) - ord('a') + 1
        end_row = int(end[1])

        if piece == 'Rook':
            # Rook can move horizontally or vertically
            return start_col == end_col or start_row == end_row
        elif piece == 'Bishop':
            # Bishop can move diagonally
            return abs(start_col - end_col) == abs(start_row - end_row)
        return False