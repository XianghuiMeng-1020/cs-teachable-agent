def hydra_heads(heads_list, cuts_list):
    final_heads_list = []
    for original_heads, cuts in zip(heads_list, cuts_list):
        # Each cut results in two more heads
        heads_lost = cuts
        heads_grown = cuts * 2
        final_heads = original_heads - heads_lost + heads_grown
        final_heads_list.append(final_heads)
    return final_heads_list

# Example usage
if __name__ == "__main__":
    print(hydra_heads([4, 3], [2, 0]))  # Output should be [8, 3]
    print(hydra_heads([10, 6], [3, 2]))  # Output should be [16, 8]
