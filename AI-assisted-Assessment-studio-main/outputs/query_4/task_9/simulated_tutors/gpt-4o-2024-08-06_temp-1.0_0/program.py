def calculate_monopoly_profit(player_moves):
    # Initialize total profit variable
    total_profit = 0
    
    # Iterate over all property values using a for loop
    for property_name, profit_or_loss in player_moves.items():
        # Sum up all the gains and losses
        total_profit += profit_or_loss
    
    return total_profit

# Test scenarios
def test_example_case():
    player_moves = {
        'Boardwalk': 200,
        'Park Place': -150,
        'Baltic Avenue': -50,
        'Reading Railroad': 100,
        'Go': 200
    }
    assert calculate_monopoly_profit(player_moves) == 300

def test_all_positive():
    player_moves = {
        'Broadway': 100,
        'Fifth Avenue': 200,
        'Main Street': 150
    }
    assert calculate_monopoly_profit(player_moves) == 450

def test_all_negative():
    player_moves = {
        'Water Works': -100,
        'Electric Company': -50,
        'Ventnor Avenue': -200
    }
    assert calculate_monopoly_profit(player_moves) == -350

def test_mixed_values_case1():
    player_moves = {
        'Indiana Avenue': 50,
        'Marvin Gardens': 100,
        'St. James Place': -70
    }
    assert calculate_monopoly_profit(player_moves) == 80

def test_zero_result():
    player_moves = {
        'Oriental Avenue': 100,
        'Vermont Avenue': -100
    }
    assert calculate_monopoly_profit(player_moves) == 0

# Run tests
test_example_case()
test_all_positive()
test_all_negative()
test_mixed_values_case1()
test_zero_result()