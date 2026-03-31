def calculate_wealth(input_file, output_file):
    exchange_rates = {
        'Gold': 10,
        'Silver': 5,
        'Bronze': 1
    }

    wealth_data = {}

    with open(input_file, 'r') as infile:
        for line in infile:
            house, assets = line.split(':')
            house = house.strip()
            total_value = 0
            assets_list = assets.split(',')
            for asset in assets_list:
                metal, amount = asset.split('=')
                metal = metal.strip()
                amount = int(amount.strip())
                total_value += amount * exchange_rates[metal]
            wealth_data[house] = total_value

    with open(output_file, 'w') as outfile:
        for house, total in wealth_data.items():
            outfile.write(f'{house}: {total} Drachmaroons\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')