def dispatch_cargo(cargo_requests):
    total_cargo = sum(cargo_requests.values())
    systems_with_cargo = 0
    leftover_cargo = total_cargo

    for system, request in cargo_requests.items():
        if request > 0:
            systems_with_cargo += 1
            leftover_cargo -= 1  # Each system receives at least one unit if they have a request

    leftover_cargo = max(leftover_cargo, 0)

    return {'systems_with_cargo': systems_with_cargo, 'leftover_cargo': leftover_cargo}