def calculate_wealth(input_file, output_file):
    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    wealth = {}
    
    with open(input_file, 'r') as file:
        for line in file:
            house, assets = line.split(':')
            total_value = 0
            for asset in assets.strip().split(','):
                metal, amount = asset.split('=')
                metal = metal.strip()
                amount = int(amount.strip())
                total_value += conversion_rates[metal] * amount
            wealth[house.strip()] = total_value
    
    with open(output_file, 'w') as file:
        for house, total_value in wealth.items():
            file.write(f'{house}: {total_value} Drachmaroons\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')