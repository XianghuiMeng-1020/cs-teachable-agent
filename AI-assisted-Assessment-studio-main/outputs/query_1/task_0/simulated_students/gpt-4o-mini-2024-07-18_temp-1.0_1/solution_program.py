def determine_wielder_power(artifacts, power_requirements):
    total_wieldable_artifacts = 0
    for artifact in artifacts:
        artifact_name, required_power = artifact
        for power in power_requirements:
            if power >= required_power:
                total_wieldable_artifacts += 1
                break
    return total_wieldable_artifacts