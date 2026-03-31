def lottery_game():
    try:
        with open('lottery_numbers.txt', 'r') as file:
            content = file.read().strip()
            numbers = content.split(',')
            user_number = input("Enter your number: ").strip()
            if user_number.isdigit() and all(num.strip().isdigit() for num in numbers):
                if user_number in [num.strip() for num in numbers]:
                    print('You Win!')
                else:
                    print('Try Again next time!')
            else:
                print('Invalid input or file content')
    except Exception:
        print('Invalid input or file content')