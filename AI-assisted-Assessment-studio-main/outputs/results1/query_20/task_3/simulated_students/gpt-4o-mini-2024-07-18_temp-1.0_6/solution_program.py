def determine_winner(alice_rolls, bob_rolls):
    alice_score = sum(int(roll) * 2 for roll in alice_rolls)
    bob_score = sum(int(roll) * 2 for roll in bob_rolls)
    if alice_score > bob_score:
        return "Alice"
    elif bob_score > alice_score:
        return "Bob"
    else:
        return "Draw"