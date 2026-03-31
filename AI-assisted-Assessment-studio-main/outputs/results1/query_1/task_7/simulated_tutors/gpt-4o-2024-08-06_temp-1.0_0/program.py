import random

def lucky_draw(cards, player_choice):
    # Shuffle the deck of cards
    random.shuffle(cards)
    
    # Check if the deck has less than five cards
    if len(cards) < 5:
        return False
    
    # Check the first five cards of the shuffled deck
    first_five = cards[:5]
    
    # Determine if player's choice is among the first five
    return player_choice in first_five
