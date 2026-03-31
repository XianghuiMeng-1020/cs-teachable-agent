def determine_wielder_power(artifacts, power_requirements):
    capable_artifacts = 0
    for artifact in artifacts:
        artifact_name, required_power = artifact
        for power in power_requirements:
            if power >= required_power:
                capable_artifacts += 1
                break
    return capable_artifacts