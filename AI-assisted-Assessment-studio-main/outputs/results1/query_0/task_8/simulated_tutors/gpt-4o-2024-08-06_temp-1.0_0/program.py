def lottery_game():
    try:
        # Read the file contents
        with open('lottery_numbers.txt', 'r') as file:
            content = file.read().strip()
            lottery_numbers = content.split(',')
        
        # Take user input
        user_input = input("Enter your number: ").strip()
        
        # Check if the file content is invalid (contains non-numeric values)
        if not all(num.strip().isdigit() for num in lottery_numbers):
            print('Invalid input or file content')
            return

        # Convert lottery numbers to integers
        lottery_numbers = [int(num.strip()) for num in lottery_numbers]

        # Validate the user input
        if not user_input.isdigit():
            print('Invalid input or file content')
            return

        user_number = int(user_input)

        # Use selection statements to determine win or loss
        if user_number in lottery_numbers:
            print('You Win!')
        else:
            print('Try Again next time!')

    except (FileNotFoundError, IOError, ValueError):
        # Catch file not found, I/O error, or invalid content
        print('Invalid input or file content')