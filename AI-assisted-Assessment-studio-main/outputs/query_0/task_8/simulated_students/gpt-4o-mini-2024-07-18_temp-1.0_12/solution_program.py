def run_lucky_number_game():
    with open('lucky_numbers.txt', 'r') as file:
        lucky_numbers = {int(line.strip()) for line in file}
    user_input = int(input('Enter a number between 1 and 50: '))

    if user_input in lucky_numbers:
        print('Congratulations! You selected a lucky number!')
    else:
        print('Sorry! Better luck next time.')