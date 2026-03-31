def summarize_observations():
    try:
        # Initialize dictionary to store unique observations for each spaceship
        spaceship_observations = {}

        # Read the input file
        with open('spaceship_logs.txt', 'r') as file:
            for line in file:
                # Parse each line
                line = line.strip()
                spaceship_name, planet_name, observation = line.split(':')

                # Create a unique key based on spaceship and planet
                key = (spaceship_name, planet_name)

                # Initialize the set for observations if not already present
                if key not in spaceship_observations:
                    spaceship_observations[key] = set()

                # Add observation to the set
                spaceship_observations[key].add(observation)

        # Prepare the summary data
        summary = {}
        for (spaceship_name, _), observations in spaceship_observations.items():
            if spaceship_name not in summary:
                summary[spaceship_name] = 0
            summary[spaceship_name] += len(observations)

        # Write the summary to the output file
        with open('summary.txt', 'w') as file:
            for spaceship_name, count in summary.items():
                file.write(f"{spaceship_name}:{count}\n")

    except Exception as e:
        # Handle exceptions by creating an empty summary.txt file
        with open('summary.txt', 'w') as file:
            pass

# Example function call
# summarize_observations()