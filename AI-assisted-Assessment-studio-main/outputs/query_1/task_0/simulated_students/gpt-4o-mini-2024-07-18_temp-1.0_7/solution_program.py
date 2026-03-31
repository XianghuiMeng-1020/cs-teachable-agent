def determine_wielder_power(artifacts, power_requirements):
    total_wieldable_artifacts = 0
    for artifact, required_power in artifacts:
        if any(character_power >= required_power for character_power in power_requirements):
            total_wieldable_artifacts += 1
    return total_wieldable_artifacts