def calculate_payout(bets, winning_number):
    payouts = {}
    for bet in bets:
        player = bet['player']
        bet_type = bet['bet_type']
        amount = bet['amount']
        payout = 0

        if bet_type == 'number':
            if winning_number == bet.get('number'):  # Condition for number bet
                payout = amount * 35
        elif bet_type == 'even':
            if winning_number % 2 == 0 and winning_number != 0:
                payout = amount * 2
        elif bet_type == 'odd':
            if winning_number % 2 == 1:
                payout = amount * 2

        payouts[player] = payouts.get(player, 0) + payout

    return payouts