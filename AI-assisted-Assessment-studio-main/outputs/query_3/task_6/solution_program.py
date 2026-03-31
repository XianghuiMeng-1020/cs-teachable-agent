def dispatch_cargo(cargo_requests):
    total_cargo = sum(cargo_requests.values())
    systems_with_demand = {system for system, demand in cargo_requests.items() if demand > 0}
    cargo_distributed = min(total_cargo, len(systems_with_demand))
    leftover_cargo = total_cargo - len(systems_with_demand)
    if leftover_cargo < 0:
        leftover_cargo = 0
    return {'systems_with_cargo': cargo_distributed, 'leftover_cargo': leftover_cargo}