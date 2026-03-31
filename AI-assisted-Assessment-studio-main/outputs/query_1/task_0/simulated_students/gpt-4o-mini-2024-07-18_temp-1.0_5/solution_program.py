def determine_wielder_power(artifacts, power_requirements):
    wieldable_artifacts = 0
    for artifact, required_power in artifacts:
        if any(power >= required_power for power in power_requirements):
            wieldable_artifacts += 1
    return wieldable_artifacts