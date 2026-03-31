def calculate_winnings(tosses):
    # Initialize a variable to hold total winnings
    total = 0
    
    # Loop over each character in the string of tosses
    for toss in tosses:
        # Selection statement to determine winnings or loss
        if toss == 'H':
            total += 2  # Add $2 for heads
        elif toss == 'T':
            total -= 1  # Subtract $1 for tails
    
    # Return the final calculated total
    return total

# Example usage
if __name__ == "__main__":
    example_tosses = "HTHTTHH"
    print(calculate_winnings(example_tosses))  # Should output 5