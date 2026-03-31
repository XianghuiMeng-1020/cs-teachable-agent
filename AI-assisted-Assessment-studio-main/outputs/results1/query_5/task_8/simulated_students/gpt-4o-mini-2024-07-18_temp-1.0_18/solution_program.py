def calculate_wealth(input_file, output_file):
    exchange_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    house_wealth = {}

    with open(input_file, 'r') as infile:
        for line in infile:
            house, assets = line.split(':')
            total_value = 0
            asset_list = assets.split(', ')
            for asset in asset_list:
                metal, amount = asset.split('=')
                amount = int(amount)
                total_value += amount * exchange_rates[metal]
            house_wealth[house.strip()] = total_value

    with open(output_file, 'w') as outfile:
        for house, wealth in house_wealth.items():
            outfile.write(f'{house}: {wealth} Drachmaroons\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')