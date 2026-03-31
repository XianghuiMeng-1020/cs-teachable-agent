def calculate_score(controlled_territories, developed_territories):
    # Initial score
    score = 0
    
    # Iterate over the controlled territories
    for territory in controlled_territories:
        # Check if the territory is developed
        if territory in developed_territories:
            score += 8  # Full points for developed
        else:
            score += 5  # Deduction for not developed
    
    return score

# Example usage
if __name__ == "__main__":
    print(calculate_score("AAA", "AAA"))  # Output should be 24
    print(calculate_score("ABC", "AB"))   # Output should be 21
    print(calculate_score("XYZ", ""))    # Output should be 15
    print(calculate_score("MNPQ", "PQ")) # Output should be 18
    print(calculate_score("", ""))       # Output should be 0