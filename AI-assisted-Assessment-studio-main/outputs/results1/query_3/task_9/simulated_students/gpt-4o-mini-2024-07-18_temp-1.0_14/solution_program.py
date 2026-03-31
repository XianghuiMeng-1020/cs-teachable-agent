def calculate_payout(bets, winning_number):
    payouts = {}
    for bet in bets:
        player = bet['player']
        bet_type = bet['bet_type']
        amount = bet['amount']
        payout = 0

        if bet_type == 'number' and winning_number == bet.get('number', -1):
            payout = amount * 35
        elif bet_type == 'even' and winning_number % 2 == 0 and winning_number != 0:
            payout = amount * 2
        elif bet_type == 'odd' and winning_number % 2 != 0:
            payout = amount * 2

        if player in payouts:
            payouts[player] += payout
        else:
            payouts[player] = payout

    return payouts