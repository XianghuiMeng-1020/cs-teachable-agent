def calculate_wealth(input_file, output_file):
    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}

    with open(input_file, 'r') as infile:
        houses = infile.readlines()

    wealth_report = []
    for house in houses:
        name, assets = house.split(': ')
        total_wealth = 0
        metals = assets.split(', ')
        for metal in metals:
            metal_name, quantity = metal.split('=')
            metal_name = metal_name.strip()
            quantity = int(quantity.strip())
            total_wealth += quantity * conversion_rates[metal_name]
        wealth_report.append(f'{name}: {total_wealth} Drachmaroons')

    with open(output_file, 'w') as outfile:
        for report in wealth_report:
            outfile.write(report + '\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')