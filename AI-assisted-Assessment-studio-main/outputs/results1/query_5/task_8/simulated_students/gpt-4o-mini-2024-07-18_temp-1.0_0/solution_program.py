def calculate_wealth(input_file, output_file):
    exchange_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    results = []

    with open(input_file, 'r') as infile:
        for line in infile:
            house, assets = line.split(':')
            total_wealth = 0
            for asset in assets.split(','):
                metal, quantity = asset.split('=')
                quantity = int(quantity.strip())
                total_wealth += quantity * exchange_rates[metal.strip()]
            results.append(f'{house.strip()}: {total_wealth} Drachmaroons')

    with open(output_file, 'w') as outfile:
        for result in results:
            outfile.write(result + '\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')