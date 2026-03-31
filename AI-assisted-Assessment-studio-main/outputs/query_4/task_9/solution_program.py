def calculate_monopoly_profit(player_moves):
    total_profit = 0
    for property, profit in player_moves.items():
        total_profit += profit
    return total_profit
