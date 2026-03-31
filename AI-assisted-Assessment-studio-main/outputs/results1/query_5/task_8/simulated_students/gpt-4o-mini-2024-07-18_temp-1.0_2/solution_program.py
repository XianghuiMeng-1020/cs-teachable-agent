def convert_assets_to_drachmaroon(house_data):
    total_wealth = {}
    conversion_rates = {
        'Gold': 10,
        'Silver': 5,
        'Bronze': 1
    }
    for house, assets in house_data.items():
        total_value = 0
        for metal, amount in assets.items():
            total_value += amount * conversion_rates[metal]
        total_wealth[house] = total_value
    return total_wealth

with open('mythology_ledger.txt', 'r') as file:
    house_data = {}
    for line in file:
        house_name, assets = line.strip().split(':')
        assets_dict = {}
        for asset in assets.split(','):
            metal, amount = asset.split('=')
            assets_dict[metal.strip()] = int(amount.strip())
        house_data[house_name.strip()] = assets_dict

result = convert_assets_to_drachmaroon(house_data)

with open('mythology_wealth.txt', 'w') as file:
    for house, wealth in result.items():
        file.write(f'{house}: {wealth} Drachmaroons\n')