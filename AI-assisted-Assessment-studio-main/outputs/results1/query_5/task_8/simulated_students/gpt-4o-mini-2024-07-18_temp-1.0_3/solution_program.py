def calculate_wealth(input_file, output_file):
    exchange_rates = {
        'Gold': 10,
        'Silver': 5,
        'Bronze': 1
    }

    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    results = []
    for line in lines:
        house, assets = line.split(':')
        total_wealth = 0
        assets = assets.strip().split(', ')
        for asset in assets:
            metal, amount = asset.split('=')
            amount = int(amount)
            total_wealth += exchange_rates[metal] * amount
        results.append(f'{house.strip()}: {total_wealth} Drachmaroons')

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(results) + '\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')