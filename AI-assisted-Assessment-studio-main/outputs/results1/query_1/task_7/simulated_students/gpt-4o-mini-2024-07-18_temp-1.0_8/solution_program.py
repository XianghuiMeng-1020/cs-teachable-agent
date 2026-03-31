def lucky_draw(cards, player_choice):
    if len(cards) < 5:
        return False
    first_five_cards = cards[:5]
    return player_choice in first_five_cards