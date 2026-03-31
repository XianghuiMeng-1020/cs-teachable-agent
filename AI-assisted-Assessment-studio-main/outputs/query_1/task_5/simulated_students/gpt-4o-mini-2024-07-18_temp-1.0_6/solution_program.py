def hydra_heads(heads_list, cuts_list):
    final_heads = []
    for original_heads, cuts in zip(heads_list, cuts_list):
        final_head_count = original_heads - cuts + (cuts * 2)
        final_heads.append(final_head_count)
    return final_heads