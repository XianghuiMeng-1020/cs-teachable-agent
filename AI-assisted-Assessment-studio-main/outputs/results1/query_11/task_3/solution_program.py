def vegetable_counter(order):
    total_vegetables = {}
    for item in order:
        dish, veggies = item.split(": ")
        for v in veggies.split(", "):
            vegetable, quantity = v.split("=")
            if vegetable in total_vegetables:
                total_vegetables[vegetable] += int(quantity)
            else:
                total_vegetables[vegetable] = int(quantity)
    result = [f"{veg}={total_vegetables[veg]}" for veg in sorted(total_vegetables.keys())]
    return str(result)