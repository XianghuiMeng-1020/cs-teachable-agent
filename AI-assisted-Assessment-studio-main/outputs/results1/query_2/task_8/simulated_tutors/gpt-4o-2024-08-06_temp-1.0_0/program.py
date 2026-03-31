def save_lottery_results(file_name, results):
    """
    Saves the list of lottery results into the specified file.

    :param file_name: The name of the file to write to.
    :param results: A list of 7-digit alphanumeric strings representing winning ticket numbers.
    """
    with open(file_name, 'w') as file:
        for ticket_number in results:
            file.write(f"{ticket_number}\n")


def check_ticket(file_name, ticket_number):
    """
    Checks whether a given ticket number is among the winning results in the specified file.

    :param file_name: The name of the file to read the winning results from.
    :param ticket_number: The ticket number to check.
    :return: True if the ticket number is a winner, False otherwise.
    """
    ticket_number = ticket_number.strip()  # Strip any unnecessary whitespace
    with open(file_name, 'r') as file:
        winning_numbers = file.read().splitlines()
        winning_numbers = [num.upper() for num in winning_numbers]
        return ticket_number.upper() in winning_numbers
