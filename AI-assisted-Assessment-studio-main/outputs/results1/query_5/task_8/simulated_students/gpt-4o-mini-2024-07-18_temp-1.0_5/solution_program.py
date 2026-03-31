def calculate_wealth():
    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    wealth_data = {}

    with open('mythology_ledger.txt', 'r') as file:
        for line in file:
            house, assets = line.strip().split(': ')
            total_wealth = 0
            for asset in assets.split(', '):
                metal, amount = asset.split('=')
                metal = metal.strip()
                amount = int(amount.strip())
                total_wealth += amount * conversion_rates[metal]
            wealth_data[house.strip()] = total_wealth

    with open('mythology_wealth.txt', 'w') as output_file:
        for house, total in wealth_data.items():
            output_file.write(f'{house}: {total} Drachmaroons\n')

calculate_wealth()