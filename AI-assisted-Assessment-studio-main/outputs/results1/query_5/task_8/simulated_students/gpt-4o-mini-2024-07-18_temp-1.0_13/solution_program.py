def calculate_wealth():
    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    house_wealth = {}
    
    with open('mythology_ledger.txt', 'r') as infile:
        for line in infile:
            house, assets = line.split(': ')
            metals = assets.split(', ')
            total_value = 0
            for metal in metals:
                metal_type, amount = metal.split('=')
                amount = int(amount)
                total_value += amount * conversion_rates[metal_type]
            house_wealth[house] = total_value
    
    with open('mythology_wealth.txt', 'w') as outfile:
        for house, wealth in house_wealth.items():
            outfile.write(f'{house}: {wealth} Drachmaroons\n')

calculate_wealth()