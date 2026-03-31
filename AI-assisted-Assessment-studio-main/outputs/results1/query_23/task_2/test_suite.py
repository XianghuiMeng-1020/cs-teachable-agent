import pytest
from chess_module import ChessBoard

def setup_module(module):
    module.chessboard = ChessBoard()

def teardown_module(module):
    del module.chessboard

class TestChessMoves:

    def test_rook_horizontal_move(self):
        assert chessboard.is_valid_move('Rook', 'a1', 'a8') == True

    def test_bishop_diagonal_move(self):
        assert chessboard.is_valid_move('Bishop', 'a1', 'b2') == True

    def test_rook_invalid_diagonal_move(self):
        assert chessboard.is_valid_move('Rook', 'a1', 'b2') == False

    def test_bishop_invalid_vertical_move(self):
        assert chessboard.is_valid_move('Bishop', 'a1', 'a2') == False

    def test_edge_case_valid_move_across_board(self):
        # Testing border limits
        assert chessboard.is_valid_move('Bishop', 'a1', 'h8') == True

    def test_edge_case_invalid_move_same_position(self):
        assert chessboard.is_valid_move('Rook', 'a1', 'a1') == False

    def test_rook_moving_one_square(self):
        assert chessboard.is_valid_move('Rook', 'b2', 'b3') == True

    def test_bishop_moving_one_square(self):
        assert chessboard.is_valid_move('Bishop', 'c1', 'd2') == True