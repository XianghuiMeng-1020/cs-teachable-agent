def lottery_game():
    try:
        with open('lottery_numbers.txt', 'r') as file:
            content = file.read().strip()
            lottery_numbers = content.split(',')
    except:
        print('Invalid input or file content')
        return

    user_number = input('Enter your lottery number: ').strip()

    if user_number in lottery_numbers:
        print('You Win!')
    else:
        print('Try Again next time!')

lottery_game()