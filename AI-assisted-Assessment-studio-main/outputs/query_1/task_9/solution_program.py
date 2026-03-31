def guard_treasure(guards):
    safe_guards = []
    for guard in guards:
        name, corridor = guard
        if corridor % 2 != 0:
            safe_guards.append(name)
    return safe_guards