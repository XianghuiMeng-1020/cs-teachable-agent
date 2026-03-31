def calculate_wealth(input_file, output_file):
    exchange_rates = {
        'Gold': 10,
        'Silver': 5,
        'Bronze': 1
    }
    wealth_data = {}
    with open(input_file, 'r') as file:
        for line in file:
            house, assets = line.split(': ')
            total_value = 0
            for asset in assets.split(', '):
                metal, amount = asset.split('=')
                amount = int(amount)
                total_value += amount * exchange_rates[metal]
            wealth_data[house] = total_value
    with open(output_file, 'w') as file:
        for house, total in wealth_data.items():
            file.write(f'{house}: {total} Drachmaroons\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')