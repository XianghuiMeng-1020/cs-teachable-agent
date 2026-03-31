def creature_balance(creature_weights_A, creature_weights_B):
    total_A = sum(creature_weights_A)
    total_B = sum(creature_weights_B)
    
    if total_A == total_B:
        return 'Balanced'
    elif total_A > total_B:
        return 'Side A'
    else:
        return 'Side B'