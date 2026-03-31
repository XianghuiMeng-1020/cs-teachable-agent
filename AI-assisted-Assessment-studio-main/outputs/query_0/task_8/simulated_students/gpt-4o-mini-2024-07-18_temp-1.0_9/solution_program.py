def run_lucky_number_game():
    # Read lucky numbers from file
    with open('lucky_numbers.txt', 'r') as file:
        lucky_numbers = {int(line.strip()) for line in file}

    # Get user's number input
    user_number = int(input('Please select a number between 1 and 50: '))

    # Check if user's number is a lucky number
    if user_number in lucky_numbers:
        print('Congratulations! You selected a lucky number!')
    else:
        print('Sorry! Better luck next time.')