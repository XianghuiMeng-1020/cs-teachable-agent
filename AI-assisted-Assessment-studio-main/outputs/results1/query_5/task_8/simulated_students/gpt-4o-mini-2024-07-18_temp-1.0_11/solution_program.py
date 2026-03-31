def calculate_wealth(input_file, output_file):
    conversion_rates = {
        'Gold': 10,
        'Silver': 5,
        'Bronze': 1
    }
    house_wealth = {}

    with open(input_file, 'r') as file:
        for line in file:
            house, assets = line.strip().split(': ')
            total_value = 0
            for asset in assets.split(', '):
                metal, amount = asset.split('=')
                amount = int(amount)
                total_value += amount * conversion_rates[metal]
            house_wealth[house] = total_value

    with open(output_file, 'w') as file:
        for house, wealth in house_wealth.items():
            file.write(f'{house}: {wealth} Drachmaroons\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')