class ChessBoard:
    def __init__(self):
        pass

    def is_valid_move(self, piece, start, end):
        # Map column letters to numbers for easy calculation
        columns = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

        # Parse the start and end positions
        start_col, start_row = columns[start[0]], int(start[1])
        end_col, end_row = columns[end[0]], int(end[1])

        if piece == 'Rook':
            # Rook moves in straight line horizontally or vertically
            if start_col == end_col or start_row == end_row:
                return True
        elif piece == 'Bishop':
            # Bishop moves diagonally
            if abs(start_col - end_col) == abs(start_row - end_row):
                return True

        return False

# This program should pass the provided test cases, validating moves based on piece type and position on a chessboard.