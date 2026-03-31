def determine_wielder_power(artifacts, power_requirements):
    count = 0
    for artifact, required_power in artifacts:
        for power in power_requirements:
            if power >= required_power:
                count += 1
                break
    return count