def run_lucky_number_game():
    user_number = input("Choose a number between 1 and 50: ")
    with open('lucky_numbers.txt', 'r') as file:
        lucky_numbers = file.read().strip().split('\n')

    if user_number in lucky_numbers:
        print("Congratulations! You selected a lucky number!")
    else:
        print("Sorry! Better luck next time.")