def dispatch_cargo(cargo_requests):
    total_cargo = sum(cargo_requests.values())
    systems_with_cargo = 0
    total_requested = 0

    for request in cargo_requests.values():
        if request > 0:
            systems_with_cargo += 1
            total_requested += request

    leftover_cargo = total_cargo - total_requested

    return {
        'systems_with_cargo': systems_with_cargo,
        'leftover_cargo': leftover_cargo
    }