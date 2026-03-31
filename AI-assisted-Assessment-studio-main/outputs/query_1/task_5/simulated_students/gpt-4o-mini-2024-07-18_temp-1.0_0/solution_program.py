def hydra_heads(heads_list, cuts_list):
    final_heads = []
    for original_heads, cuts in zip(heads_list, cuts_list):
        heads_after_cuts = original_heads - cuts + (cuts * 2)
        final_heads.append(heads_after_cuts)
    return final_heads