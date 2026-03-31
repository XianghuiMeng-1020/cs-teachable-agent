def calculate_wealth(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    house_values = []
    for line in lines:
        house_name, assets = line.split(': ')
        gold = silver = bronze = 0
        for asset in assets.split(', '):
            metal, amount = asset.split('=')
            amount = int(amount)
            if metal == 'Gold':
                gold = amount
            elif metal == 'Silver':
                silver = amount
            elif metal == 'Bronze':
                bronze = amount
        total_wealth = (gold * 10) + (silver * 5) + bronze
        house_values.append(f'{house_name}: {total_wealth} Drachmaroons')

    with open(output_file, 'w') as file:
        for house_value in house_values:
            file.write(house_value + '\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')