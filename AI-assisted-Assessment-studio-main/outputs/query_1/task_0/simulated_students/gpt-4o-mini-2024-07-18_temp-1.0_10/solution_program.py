def determine_wielder_power(artifacts, power_requirements):
    count = 0
    for artifact in artifacts:
        required_power = artifact[1]
        if any(character_power >= required_power for character_power in power_requirements):
            count += 1
    return count