def lucky_draw(cards, player_choice):
    if len(cards) < 5:
        return False
    shuffled_cards = cards[:5]
    for card in shuffled_cards:
        if card == player_choice:
            return True
    return False