def dispatch_cargo(cargo_requests):
    total_requests = sum(cargo_requests.values())
    systems_with_requests = len([req for req in cargo_requests.values() if req > 0])
    leftover_cargo = total_requests - systems_with_requests
    return {'systems_with_cargo': systems_with_requests, 'leftover_cargo': leftover_cargo}