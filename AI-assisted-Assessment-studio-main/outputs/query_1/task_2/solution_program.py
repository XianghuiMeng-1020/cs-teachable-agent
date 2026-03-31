def creature_balance(creature_weights_A, creature_weights_B):
    total_A = 0
    total_B = 0
    for weight in creature_weights_A:
        total_A += weight
    for weight in creature_weights_B:
        total_B += weight
    if total_A == total_B:
        return 'Balanced'
    elif total_A > total_B:
        return 'Side A'
    else:
        return 'Side B'