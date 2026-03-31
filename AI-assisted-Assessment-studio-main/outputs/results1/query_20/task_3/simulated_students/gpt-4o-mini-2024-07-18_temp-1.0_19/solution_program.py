def determine_winner(alice_rolls, bob_rolls):
    alice_score = sum(2 * int(die) for die in alice_rolls)
    bob_score = sum(2 * int(die) for die in bob_rolls)
    if alice_score > bob_score:
        return "Alice"
    elif bob_score > alice_score:
        return "Bob"
    else:
        return "Draw"