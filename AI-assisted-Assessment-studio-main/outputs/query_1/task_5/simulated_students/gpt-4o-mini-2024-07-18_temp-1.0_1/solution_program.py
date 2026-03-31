def hydra_heads(heads_list, cuts_list):
    final_heads = []
    for heads, cuts in zip(heads_list, cuts_list):
        remaining_heads = heads - cuts + (cuts * 2)
        final_heads.append(remaining_heads)
    return final_heads