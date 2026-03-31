def check_maintenance(distances):
    results = []  # Initialize an empty list to store results
    for distance in distances:
        if distance % 1000 == 0:
            results.append("Check required")  # Add "Check required" if distance is a multiple of 1000
        else:
            results.append("No check needed")  # Add "No check needed" otherwise
    return results

# Testing the function
print(check_maintenance([1000, 1450, 3000, 3200]))  # ["Check required", "No check needed", "Check required", "No check needed"]