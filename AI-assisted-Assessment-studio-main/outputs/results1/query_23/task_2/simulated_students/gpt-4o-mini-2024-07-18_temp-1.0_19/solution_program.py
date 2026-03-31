class ChessBoard:
    def __init__(self):
        pass

    def is_valid_move(self, piece, start, end):
        # Convert board positions into numeric coordinates
        start_col = ord(start[0]) - ord('a') + 1
        start_row = int(start[1])
        end_col = ord(end[0]) - ord('a') + 1
        end_row = int(end[1])

        if piece == 'Rook':
            # Rook moves are valid if they are in the same row or column
            return (start_row == end_row) or (start_col == end_col)

        elif piece == 'Bishop':
            # Bishop moves are valid if they are on the same diagonal
            return abs(start_col - end_col) == abs(start_row - end_row)

        return False