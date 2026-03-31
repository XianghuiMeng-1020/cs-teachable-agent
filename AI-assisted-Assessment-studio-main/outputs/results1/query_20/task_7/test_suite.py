import pytest

from solution_program import move_player_on_board

board_profit_1 = '0 20 -50 30 40 10 0 -20 70 -30'
board_profit_2 = '100 200 -100 50 -25 0'
board_profit_3 = '10 -10 20 -20 30 -30'

@pytest.mark.parametrize("current_position, dice_roll, net_money, board_profit, expected", [
    (1, 3, 500, board_profit_1, (4, 530)),
    (5, 3, 1000, board_profit_1, (8, 1070)),
    (8, 3, 300, board_profit_1, (1, 300)),
    (3, 10, 100, board_profit_1, (2, 120)),
    (10, 6, 200, board_profit_1, (6, 210)),
    (1, 2, 1000, board_profit_2, (3, 900)),
    (6, 5, 1500, board_profit_2, (5, 1475)),
    (3, 6, 100, board_profit_3, (3, 100)),  # Full loop back to start
    (1, 7, 0, board_profit_3, (2, -10)),
    (2, 4, 0, board_profit_3, (6, 0)),
])
def test_move_player_on_board(current_position, dice_roll, net_money, board_profit, expected):
    assert move_player_on_board(current_position, dice_roll, net_money, board_profit) == expected
