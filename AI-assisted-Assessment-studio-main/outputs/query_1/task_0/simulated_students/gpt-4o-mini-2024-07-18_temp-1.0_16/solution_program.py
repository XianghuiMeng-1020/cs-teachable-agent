def determine_wielder_power(artifacts, power_requirements):
    count = 0
    for artifact, required_power in artifacts:
        if any(power >= required_power for power in power_requirements):
            count += 1
    return count