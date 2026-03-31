def determine_winner(alice_rolls, bob_rolls):
    alice_score = sum(int(digit) * 2 for digit in alice_rolls)
    bob_score = sum(int(digit) * 2 for digit in bob_rolls)
    if alice_score > bob_score:
        return "Alice"
    elif bob_score > alice_score:
        return "Bob"
    else:
        return "Draw"