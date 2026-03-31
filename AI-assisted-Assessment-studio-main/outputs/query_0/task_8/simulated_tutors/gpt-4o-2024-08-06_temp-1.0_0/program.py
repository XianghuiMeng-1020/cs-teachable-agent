def run_lucky_number_game():
    # Open the file and read lucky numbers
    with open('lucky_numbers.txt', 'r') as file:
        lucky_numbers = [line.strip() for line in file]
    
    # Prompt user for input
    user_input = input("Please select a number between 1 and 50: ")
    
    # Check if user's input matches any lucky number
    if user_input in lucky_numbers:
        print("Congratulations! You selected a lucky number!")
    else:
        print("Sorry! Better luck next time.")

# Example usage
# This line would typically be in the main part of the application
# run_lucky_number_game()