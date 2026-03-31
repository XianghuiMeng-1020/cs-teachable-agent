def dispatch_cargo(cargo_requests):
    total_cargo = sum(cargo_requests.values())
    systems_with_cargo = sum(1 for request in cargo_requests.values() if request > 0)
    leftover_cargo = total_cargo - systems_with_cargo
    return {'systems_with_cargo': systems_with_cargo, 'leftover_cargo': leftover_cargo}