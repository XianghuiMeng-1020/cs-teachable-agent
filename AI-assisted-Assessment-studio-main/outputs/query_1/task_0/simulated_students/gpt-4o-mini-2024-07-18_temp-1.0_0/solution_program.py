def determine_wielder_power(artifacts, power_requirements):
    total_wieldable_artifacts = 0
    for artifact_name, required_power in artifacts:
        if any(power >= required_power for power in power_requirements):
            total_wieldable_artifacts += 1
    return total_wieldable_artifacts