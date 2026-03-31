def lottery_game():
    try:
        with open('lottery_numbers.txt', 'r') as file:
            lottery_numbers = file.read().strip().split(',')
        user_number = input('Enter your lottery number: ').strip()
        if user_number in lottery_numbers:
            print('You Win!')
        else:
            print('Try Again next time!')
    except (FileNotFoundError, IOError):
        print('Invalid input or file content')
    except Exception:
        print('Invalid input or file content')

lottery_game()