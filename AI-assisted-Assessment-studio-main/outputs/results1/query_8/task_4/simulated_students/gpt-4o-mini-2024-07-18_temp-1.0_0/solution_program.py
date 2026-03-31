def mythological_judgment(creature, action):
    judgments = {
        "Zeus": {
            "help": "Blessing granted",
            "other": "Storms befall you"
        },
        "Cerberus": {
            "steal": "Growling disapproval",
            "other": "Pass freely"
        },
        "Aphrodite": {
            "love": "Heart's desire fulfilled"
        }
    }

    if creature in judgments:
        if creature == "Zeus" and action == "help":
            return judgments[creature][action]
        elif creature == "Zeus":
            return judgments[creature]["other"]
        elif creature == "Cerberus" and action == "steal":
            return judgments[creature][action]
        elif creature == "Cerberus":
            return judgments[creature]["other"]
        elif creature == "Aphrodite" and action == "love":
            return judgments[creature][action]

    return "No judgment found"