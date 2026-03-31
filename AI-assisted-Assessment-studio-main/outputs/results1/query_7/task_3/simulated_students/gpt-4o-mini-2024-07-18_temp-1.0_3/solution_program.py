def filter_mythical_creatures(input_filename, output_filename, status):
    with open(input_filename, 'r') as file:
        creatures = file.readlines()

    filtered_creatures = [creature.split(':')[0] for creature in creatures if creature.strip().endswith(status)]

    with open(output_filename, 'w') as outfile:
        for creature in filtered_creatures:
            outfile.write(f"{creature}\n")