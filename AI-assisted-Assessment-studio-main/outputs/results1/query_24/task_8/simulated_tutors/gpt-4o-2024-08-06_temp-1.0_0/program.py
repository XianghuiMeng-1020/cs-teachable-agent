def update_leaderboard(score_entries):
    leaderboard = {}
    for entry in score_entries:
        try:
            player, score = entry.split(",")
            score = int(score)  # Convert score to an integer
            if player in leaderboard:
                leaderboard[player] += score
            else:
                leaderboard[player] = score
        except ValueError:
            # Skip entry if split() fails or score cannot be converted to int
            continue
    return leaderboard

# Test cases
# (Ideally, these would be run using a framework like pytest as shown in the test suite)
entries_basic = [
    "Alice,10",
    "Bob,15",
    "Alice,5",
    "Charlie,20"
]
print(update_leaderboard(entries_basic))  # Output: {"Alice": 15, "Bob": 15, "Charlie": 20}

entries_malformed = [
    "Alice,10",
    "Bob,15",
    "Alice-5",
    "Charlie,20a",
    "David,30"
]
print(update_leaderboard(entries_malformed))  # Output: {"Alice": 10, "Bob": 15, "David": 30}

entries_empty = []
print(update_leaderboard(entries_empty))  # Output: {}

entries_no_valid = [
    "Alice-Ten",
    "Bob-Fifteen",
    "AliceFifteen",
    "Charlie:Twenty"
]
print(update_leaderboard(entries_no_valid))  # Output: {}

entries_large_numbers = [
    "Alice,1000000",
    "Bob,-5000",
    "Alice,2000000",
    "Charlie,0"
]
print(update_leaderboard(entries_large_numbers))  # Output: {"Alice": 3000000, "Bob": -5000, "Charlie": 0}