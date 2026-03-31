def calculate_monopoly_profit(player_moves):
    total_profit = 0
    for profit in player_moves.values():
        total_profit += profit
    return total_profit