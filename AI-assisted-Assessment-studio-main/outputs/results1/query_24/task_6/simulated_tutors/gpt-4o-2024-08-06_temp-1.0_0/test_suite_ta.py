from program import *
import pytest
from program import roll_dice

def test_roll_dice_single_roll():
    assert roll_dice('2d6') == [12]

def test_roll_dice_multiple_rolls():
    assert roll_dice('2d6,3d4') == [12, 12]

    
def test_roll_dice_invalid_format():
    assert roll_dice('2x6') == 'Invalid roll format'


def test_roll_dice_mixed_valid_invalid():
    assert roll_dice('2d6,3x4') == 'Invalid roll format'


def test_roll_dice_zero_dice_sides():
    assert roll_dice('0d6') == 'Invalid number of dice or sides'
    assert roll_dice('2d0') == 'Invalid number of dice or sides'
    assert roll_dice('-1d6') == 'Invalid number of dice or sides'
    assert roll_dice('2d-6') == 'Invalid number of dice or sides'
    