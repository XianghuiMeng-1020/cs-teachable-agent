def lucky_draw(cards, player_choice):
    if len(cards) < 5:
        return False
    return player_choice in cards[:5]