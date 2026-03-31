def lucky_draw(cards, player_choice):
    if len(cards) < 5:
        return False
    shuffled_cards = cards[:5]  # We just need the first five cards
    return player_choice in shuffled_cards