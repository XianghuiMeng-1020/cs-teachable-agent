def calculate_payout(bets, winning_number):
    payout_dict = {}
    for bet in bets:
        player = bet['player']
        bet_type = bet['bet_type']
        amount = bet['amount']
        payout = 0
        if bet_type == "number":
            if amount == winning_number:
                payout = amount * 35
        elif bet_type == "even":
            if winning_number != 0 and winning_number % 2 == 0:
                payout = amount * 2
        elif bet_type == "odd":
            if winning_number % 2 != 0:
                payout = amount * 2
        payout_dict[player] = payout
    return payout_dict