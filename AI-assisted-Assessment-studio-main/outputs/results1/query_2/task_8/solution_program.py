def save_lottery_results(file_name, results):
    with open(file_name, 'w') as file:
        for result in results:
            file.write(f"{result}\n")


def check_ticket(file_name, ticket_number):
    with open(file_name, 'r') as file:
        winning_numbers = [line.strip() for line in file]
        return ticket_number in winning_numbers