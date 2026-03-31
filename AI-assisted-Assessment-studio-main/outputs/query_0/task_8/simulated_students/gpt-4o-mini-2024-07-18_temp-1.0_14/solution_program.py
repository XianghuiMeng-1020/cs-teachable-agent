def run_lucky_number_game():
    with open('lucky_numbers.txt', 'r') as file:
        lucky_numbers = file.read().splitlines()
        lucky_numbers = [int(num) for num in lucky_numbers]  # Convert strings to integers

    user_input = int(input('Please enter a number between 1 and 50: '))

    if user_input in lucky_numbers:
        print('Congratulations! You selected a lucky number!')
    else:
        print('Sorry! Better luck next time.')