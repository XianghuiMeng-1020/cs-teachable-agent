import random

def lucky_draw(cards, player_choice):
    if len(cards) < 5:
        return False
    shuffled_deck = random.sample(cards, len(cards))
    first_five_cards = shuffled_deck[:5]
    return player_choice in first_five_cards