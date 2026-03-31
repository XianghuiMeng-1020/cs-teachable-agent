def save_lottery_results(file_name, results):
    with open(file_name, 'w') as file:
        for result in results:
            file.write(result + '\n')


def check_ticket(file_name, ticket_number):
    with open(file_name, 'r') as file:
        winning_results = file.read().strip().split('\n')
    return ticket_number in winning_results