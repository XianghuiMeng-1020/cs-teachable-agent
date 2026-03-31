def guard_treasure(guards):
    # Initialize a list to hold names of guards in odd corridors
    odd_corridor_guards = []
    
    # Iterate over each guard and their corridor number
    for guard, corridor in guards:
        # Check if the corridor number is odd
        if corridor % 2 != 0:
            # If it's odd, add the guard's name to the list
            odd_corridor_guards.append(guard)
    
    # Return the list of guards blocking odd-numbered corridors
    return odd_corridor_guards

# Example usage
if __name__ == "__main__":
    guards = [("Athena", 1), ("Hermes", 2), ("Apollo", 3), ("Artemis", 4)]
    print(guard_treasure(guards))