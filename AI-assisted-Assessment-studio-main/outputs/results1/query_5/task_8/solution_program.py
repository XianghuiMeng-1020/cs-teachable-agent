def calculate_wealth():
    with open('mythology_ledger.txt', 'r') as input_file:
        houses = input_file.readlines()

    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    results = []

    for house in houses:
        name, assets = house.strip().split(': ')
        assets = assets.split(', ')
        total_drachmaroons = 0

        for asset in assets:
            metal, quantity = asset.split('=')
            total_drachmaroons += int(quantity) * conversion_rates[metal]

        results.append(f"{name}: {total_drachmaroons} Drachmaroons")

    with open('mythology_wealth.txt', 'w') as output_file:
        for result in results:
            output_file.write(result + '\n')
