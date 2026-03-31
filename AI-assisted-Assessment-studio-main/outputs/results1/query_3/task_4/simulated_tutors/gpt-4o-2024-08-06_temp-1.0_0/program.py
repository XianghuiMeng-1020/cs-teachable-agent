import random


def simulate_game(bet_number, bet_amount, probabilities):
    # Generate a random number based on probabilities
    numbers = list(probabilities.keys())
    probs = list(probabilities.values())
    drawn_number = random.choices(numbers, weights=probs, k=1)[0]
    
    # Check if bet matches drawn number
    if bet_number == drawn_number:
        return 2 * bet_amount
    else:
        return -bet_amount

# Example usage
if __name__ == "__main__":
    # Example probability dictionary
    prob_dict = {1: 0.1, 2: 0.1, 3: 0.1, 4: 0.1, 5: 0.1,
                 6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.1}
    # Simulate a bet on number 5 with bet amount of 10
    result = simulate_game(5, 10, prob_dict)
    print("Net Gain/Loss:", result)