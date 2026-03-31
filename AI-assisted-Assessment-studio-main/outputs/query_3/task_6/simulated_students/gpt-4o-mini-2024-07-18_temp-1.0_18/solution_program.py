def dispatch_cargo(cargo_requests):
    total_requested = sum(cargo_requests.values())
    systems_with_demand = sum(1 for request in cargo_requests.values() if request > 0)
    leftover_cargo = total_requested - systems_with_demand  
    return {'systems_with_cargo': systems_with_demand, 'leftover_cargo': max(leftover_cargo, 0)}