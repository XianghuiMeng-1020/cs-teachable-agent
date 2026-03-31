def dispatch_cargo(cargo_requests):
    total_cargo = sum(cargo_requests.values())
    systems_with_cargo = 0
    leftover_cargo = 0
    if total_cargo > 0:
        for request in cargo_requests.values():
            if request > 0:
                systems_with_cargo += 1
                leftover_cargo += request
        leftover_cargo = total_cargo - leftover_cargo
    return {'systems_with_cargo': systems_with_cargo, 'leftover_cargo': leftover_cargo}