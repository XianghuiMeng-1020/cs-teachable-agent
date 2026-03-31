def calculate_wealth():
    input_filename = 'mythology_ledger.txt'
    output_filename = 'mythology_wealth.txt'

    exchange_rates = {
        'Gold': 10,
        'Silver': 5,
        'Bronze': 1
    }

    try:
        with open(input_filename, 'r') as f:
            lines = f.readlines()

        with open(output_filename, 'w') as f:
            for line in lines:
                house, assets = line.split(':')
                assets = assets.strip()
                assets_items = assets.split(', ')

                total_drachmaroons = 0

                for asset in assets_items:
                    metal, amount_str = asset.split('=')
                    amount = int(amount_str)
                    if metal in exchange_rates:
                        total_drachmaroons += amount * exchange_rates[metal]

                f.write(f'{house}: {total_drachmaroons} Drachmaroons\n')
    except FileNotFoundError:
        print("Input file not found!")