def hydra_heads(heads_list, cuts_list):
    final_heads = []
    for heads, cuts in zip(heads_list, cuts_list):
        final_count = heads - cuts + (cuts * 2)
        final_heads.append(final_count)
    return final_heads