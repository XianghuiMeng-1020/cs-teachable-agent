def creature_balance(creature_weights_A, creature_weights_B):
    # Calculate the total weights on side A and B using arithmetic operators and list functions.
    total_A = sum(creature_weights_A)  # sum up list A
    total_B = sum(creature_weights_B)  # sum up list B
    
    # Use selection statements to determine which side is heavier or if balanced.
    if total_A > total_B:
        return 'Side A'
    elif total_B > total_A:
        return 'Side B'
    else:
        return 'Balanced'

# Examples to test the function
print(creature_balance([5, 10, 5], [7, 13]))  # 'Balanced'
print(creature_balance([10, 20], [5, 5]))     # 'Side A'
print(creature_balance([5, 8], [10, 5]))     # 'Side A'
print(creature_balance([12, 15], [25, 3]))   # 'Side B'
print(creature_balance([7, 8], [9, 6]))      # 'Balanced'