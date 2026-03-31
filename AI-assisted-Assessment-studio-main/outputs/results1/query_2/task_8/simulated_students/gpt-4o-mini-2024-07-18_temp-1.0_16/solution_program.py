def save_lottery_results(file_name, results):
    with open(file_name, 'w') as file:
        for ticket in results:
            file.write(ticket + '\n')


def check_ticket(file_name, ticket_number):
    with open(file_name, 'r') as file:
        winning_tickets = file.read().strip().split('\n')
    return ticket_number in winning_tickets