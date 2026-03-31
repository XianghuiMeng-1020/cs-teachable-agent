def dispatch_cargo(cargo_requests):
    # Sum up all requests to get the total cargo available
    total_cargo = sum(cargo_requests.values())
    systems_with_demand = 0
    leftover_cargo = 0

    # Count systems with demand and calculate leftover cargo
    for system, demand in cargo_requests.items():
        if demand > 0:
            systems_with_demand += 1

    # If there's leftover cargo, it must be zero because total cargo matches the demand
    leftover_cargo = 0 if total_cargo == sum(cargo_requests.values()) else total_cargo - systems_with_demand

    return {
        'systems_with_cargo': systems_with_demand,
        'leftover_cargo': leftover_cargo
    }