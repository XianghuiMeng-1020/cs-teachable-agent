def determine_wielder_power(artifacts, power_requirements):
    total_wieldable = 0
    for artifact, required_power in artifacts:
        if any(power >= required_power for power in power_requirements):
            total_wieldable += 1
    return total_wieldable