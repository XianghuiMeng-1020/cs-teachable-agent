def determine_wielder_power(artifacts, power_requirements):
    total_wieldable_artifacts = 0
    for artifact, required_power in artifacts:
        for power in power_requirements:
            if power >= required_power:
                total_wieldable_artifacts += 1
                break  # Stop checking once we find a character who can wield it
    return total_wieldable_artifacts

# Test cases will automatically run using pytest if saved and executed in the appropriate environment.