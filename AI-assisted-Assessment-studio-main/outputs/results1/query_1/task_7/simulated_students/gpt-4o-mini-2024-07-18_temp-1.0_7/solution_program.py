import random

def lucky_draw(cards, player_choice):
    if len(cards) < 5:
        return False
    shuffled_cards = random.sample(cards, len(cards))
    first_five = shuffled_cards[:5]
    return player_choice in first_five