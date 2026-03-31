def lottery_game():
    try:
        with open('lottery_numbers.txt', 'r') as file:
            lottery_numbers = file.read().strip().split(',')
            lottery_numbers = [number.strip() for number in lottery_numbers]

        user_number = input('Enter your chosen number: ').strip()

        if user_number in lottery_numbers:
            print('You Win!')
        else:
            print('Try Again next time!')
    except:
        print('Invalid input or file content')

lottery_game()