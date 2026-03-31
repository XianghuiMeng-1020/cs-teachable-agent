def hydra_heads(heads_list, cuts_list):
    final_heads = []
    for heads, cuts in zip(heads_list, cuts_list):
        final_heads.append(heads - cuts + 2 * cuts)
    return final_heads