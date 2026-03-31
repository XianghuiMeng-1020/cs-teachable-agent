def determine_wielder_power(artifacts, power_requirements):
    wieldable_count = 0
    for artifact, required_power in artifacts:
        for character_power in power_requirements:
            if character_power >= required_power:
                wieldable_count += 1
                break
    return wieldable_count