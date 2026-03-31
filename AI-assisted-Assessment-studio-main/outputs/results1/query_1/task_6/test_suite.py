import pytest
from solution import check_dice_lottery_results

def test_check_dice_lottery_results():
    assert check_dice_lottery_results([(1, 6), (3, 4), (2, 2), (6, 6), (5, 6)]) == [True, True, False, True, False]
    assert check_dice_lottery_results([(5, 2), (1, 1), (3, 3), (4, 4)]) == [True, False, False, False]
    assert check_dice_lottery_results([(6, 5), (4, 2), (1, 5)]) == [True, False, False]
    assert check_dice_lottery_results([(2, 2), (7, 7), (1, 2)]) == [False, False, False]
    assert check_dice_lottery_results([(3, 3), (5, 6), (1, 1), (1, 4)]) == [False, True, False, False]