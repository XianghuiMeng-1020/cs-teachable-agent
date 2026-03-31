def guard_treasure(guards):
    return [name for name, corridor in guards if corridor % 2 == 1]