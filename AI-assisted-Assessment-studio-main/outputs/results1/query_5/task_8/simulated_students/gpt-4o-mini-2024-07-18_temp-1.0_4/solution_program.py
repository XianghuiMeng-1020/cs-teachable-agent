def calculate_wealth():
    # Conversion rates
    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    wealth = {}

    with open('mythology_ledger.txt', 'r') as infile:
        for line in infile:
            # Split house name and assets
            house, assets = line.split(':')
            total_value = 0
            # Split assets and calculate total value
            asset_items = assets.split(',')
            for item in asset_items:
                metal, value = item.split('=')
                metal = metal.strip()
                value = int(value.strip())
                # Calculate wealth
                total_value += value * conversion_rates[metal]
            wealth[house.strip()] = total_value

    with open('mythology_wealth.txt', 'w') as outfile:
        for house, total in wealth.items():
            outfile.write(f'{house}: {total} Drachmaroons\n')

calculate_wealth()