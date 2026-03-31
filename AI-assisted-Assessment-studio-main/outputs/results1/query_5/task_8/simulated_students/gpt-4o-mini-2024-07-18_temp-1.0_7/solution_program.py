def calculate_wealth(input_file, output_file):
    conversion_rates = {
        'Gold': 10,
        'Silver': 5,
        'Bronze': 1
    }

    wealth_data = {}

    with open(input_file, 'r') as infile:
        for line in infile:
            house, metals = line.strip().split(':')
            house = house.strip()
            metals = metals.strip().split(',')
            total_wealth = 0
            for metal in metals:
                metal_type, quantity = metal.split('=')
                metal_type = metal_type.strip()
                quantity = int(quantity.strip())
                total_wealth += quantity * conversion_rates[metal_type]
            wealth_data[house] = total_wealth

    with open(output_file, 'w') as outfile:
        for house, total in wealth_data.items():
            outfile.write(f'{house}: {total} Drachmaroons\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')