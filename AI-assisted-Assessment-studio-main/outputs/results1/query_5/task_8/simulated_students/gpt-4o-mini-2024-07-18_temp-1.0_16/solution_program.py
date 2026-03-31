def calculate_wealth(input_file, output_file):
    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    wealth_data = {}

    with open(input_file, 'r') as infile:
        for line in infile:
            house, assets = line.split(':')
            total_wealth = 0
            for metal in assets.split(','):
                metal_name, amount = metal.split('=')
                amount = int(amount.strip())
                total_wealth += amount * conversion_rates[metal_name.strip()]
            wealth_data[house.strip()] = total_wealth

    with open(output_file, 'w') as outfile:
        for house, wealth in wealth_data.items():
            outfile.write(f'{house}: {wealth} Drachmaroons\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')