def calculate_payout(bets, winning_number):
    payouts = {}
    for bet in bets:
        player = bet['player']
        bet_type = bet['bet_type']
        amount = bet['amount']
        payout = 0

        if bet_type == 'number':
            if winning_number == amount:
                payout = 35 * bet['amount']
        elif bet_type == 'even':
            if winning_number % 2 == 0 and winning_number != 0:
                payout = 2 * bet['amount']
        elif bet_type == 'odd':
            if winning_number % 2 != 0:
                payout = 2 * bet['amount']

        if player in payouts:
            payouts[player] += payout
        else:
            payouts[player] = payout

    return payouts