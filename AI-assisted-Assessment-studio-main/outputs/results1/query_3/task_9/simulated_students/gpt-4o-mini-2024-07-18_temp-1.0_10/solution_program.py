def calculate_payout(bets, winning_number):
    payouts = {}
    for bet in bets:
        player = bet['player']
        bet_type = bet['bet_type']
        amount = bet['amount']

        if player not in payouts:
            payouts[player] = 0

        if bet_type == 'number':
            if winning_number == bet['amount']:
                payouts[player] += amount * 35
        elif bet_type == 'even':
            if winning_number % 2 == 0 and winning_number != 0:
                payouts[player] += amount * 2
        elif bet_type == 'odd':
            if winning_number % 2 != 0:
                payouts[player] += amount * 2

    return payouts