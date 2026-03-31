def lottery_game():
    try:
        with open('lottery_numbers.txt', 'r') as f:
            lottery_numbers = f.read().strip().split(',')
    except (FileNotFoundError, IOError):
        print('Invalid input or file content')
        return

    user_number = input('Enter your chosen number: ').strip()

    if user_number in lottery_numbers:
        print('You Win!')
    else:
        print('Try Again next time!')

lottery_game()