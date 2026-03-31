def dispatch_cargo(cargo_requests):
    total_cargo = sum(cargo_requests.values())
    systems_with_cargo = 0
    leftover_cargo = 0

    for demand in cargo_requests.values():
        if demand > 0:
            systems_with_cargo += 1

    leftover_cargo = total_cargo - systems_with_cargo

    return {'systems_with_cargo': systems_with_cargo, 'leftover_cargo': leftover_cargo}