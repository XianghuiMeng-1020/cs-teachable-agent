class ChessBoard:
    def __init__(self):
        self.size = 8
        self.file_mapping = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}

    def is_valid_move(self, piece, start, end):
        start_file, start_rank = start[0], int(start[1])
        end_file, end_rank = end[0], int(end[1])
        start_file_index = self.file_mapping[start_file]
        end_file_index = self.file_mapping[end_file]

        if piece == 'Rook':
            return start_file_index == end_file_index or start_rank == end_rank
        elif piece == 'Bishop':
            return abs(start_file_index - end_file_index) == abs(start_rank - end_rank)
        return False