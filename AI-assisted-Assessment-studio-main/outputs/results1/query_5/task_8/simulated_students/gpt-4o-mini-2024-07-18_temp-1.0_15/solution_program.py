def calculate_wealth():
    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    wealth = {}

    with open('mythology_ledger.txt', 'r') as file:
        for line in file:
            house, assets = line.split(':')
            house = house.strip()
            total_drachmaroons = 0
            for asset in assets.split(','):
                metal, amount = asset.split('=')
                metal = metal.strip()
                amount = int(amount.strip())
                total_drachmaroons += amount * conversion_rates[metal]
            wealth[house] = total_drachmaroons

    with open('mythology_wealth.txt', 'w') as outfile:
        for house, total in wealth.items():
            outfile.write(f'{house}: {total} Drachmaroons\n')

calculate_wealth()