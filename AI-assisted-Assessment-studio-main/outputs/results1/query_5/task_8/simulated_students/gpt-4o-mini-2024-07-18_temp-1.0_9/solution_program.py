def convert_assets_to_drachmaroons(input_file, output_file):
    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    results = []

    with open(input_file, 'r') as file:
        for line in file:
            house_data = line.strip().split(':')
            house_name = house_data[0]
            assets = house_data[1].split(',')
            total_value = 0

            for asset in assets:
                metal, amount = asset.split('=')
                total_value += conversion_rates[metal.strip()] * int(amount.strip())

            results.append(f'{house_name}: {total_value} Drachmaroons')

    with open(output_file, 'w') as file:
        file.write('\n'.join(results) + '\n')

convert_assets_to_drachmaroons('mythology_ledger.txt', 'mythology_wealth.txt')