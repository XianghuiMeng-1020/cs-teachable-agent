def hydra_heads(heads_list, cuts_list):
    final_heads = []
    for original_heads, cuts in zip(heads_list, cuts_list):
        final_count = original_heads - cuts + 2 * cuts
        final_heads.append(final_count)
    return final_heads