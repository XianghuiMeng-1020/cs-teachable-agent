def dispatch_cargo(cargo_requests):
    total_requests = 0
    systems_with_cargo = 0

    for request in cargo_requests.values():
        if request > 0:
            total_requests += request
            systems_with_cargo += 1

    leftover_cargo = total_requests % systems_with_cargo if systems_with_cargo > 0 else 0

    return {'systems_with_cargo': systems_with_cargo, 'leftover_cargo': leftover_cargo}