def determine_winner(alice_rolls, bob_rolls):
    alice_score = 0
    bob_score = 0
    for roll in alice_rolls:
        alice_score += int(roll) * 2
    for roll in bob_rolls:
        bob_score += int(roll) * 2
    if alice_score > bob_score:
        return "Alice"
    elif bob_score > alice_score:
        return "Bob"
    return "Draw"