def calculate_wealth(input_file, output_file):
    conversion_rates = {'Gold': 10, 'Silver': 5, 'Bronze': 1}
    wealth_data = {}
    
    with open(input_file, 'r') as infile:
        for line in infile:
            house, assets = line.split(': ')
            total_value = 0
            assets = assets.split(', ')
            
            for asset in assets:
                metal, amount = asset.split('=')
                amount = int(amount)
                total_value += amount * conversion_rates[metal]
            
            wealth_data[house] = total_value
    
    with open(output_file, 'w') as outfile:
        for house, total in wealth_data.items():
            outfile.write(f'{house}: {total} Drachmaroons\n')

calculate_wealth('mythology_ledger.txt', 'mythology_wealth.txt')