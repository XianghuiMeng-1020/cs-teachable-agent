def calculate_wealth():
    conversion_rates = {
        'Gold': 10,
        'Silver': 5,
        'Bronze': 1
    }
    house_wealth = {}

    with open('mythology_ledger.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            house_name = parts[0]
            assets = parts[1].split(',')

            total_value = 0
            for asset in assets:
                metal, amount = asset.split('=')
                metal = metal.strip()
                amount = int(amount.strip())
                total_value += amount * conversion_rates[metal]

            house_wealth[house_name] = total_value

    with open('mythology_wealth.txt', 'w') as output_file:
        for house, wealth in house_wealth.items():
            output_file.write(f'{house}: {wealth} Drachmaroons\n')

calculate_wealth()