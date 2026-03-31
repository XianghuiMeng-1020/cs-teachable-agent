def calculate_wealth():
    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    wealth_dict = {}
    
    with open('mythology_ledger.txt', 'r') as infile:
        for line in infile:
            line = line.strip()
            house, assets = line.split(':')
            total_wealth = 0
            asset_items = assets.split(', ')
            for item in asset_items:
                metal, amount = item.split('=')
                amount = int(amount)
                total_wealth += conversion_rates[metal] * amount
            wealth_dict[house] = total_wealth
    
    with open('mythology_wealth.txt', 'w') as outfile:
        for house, total in wealth_dict.items():
            outfile.write(f'{house}: {total} Drachmaroons\n')

calculate_wealth()