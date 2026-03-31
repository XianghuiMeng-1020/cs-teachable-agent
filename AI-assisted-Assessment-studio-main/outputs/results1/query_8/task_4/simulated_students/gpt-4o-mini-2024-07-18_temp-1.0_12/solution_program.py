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
        if action in judgments[creature]:
            return judgments[creature][action]
        else:
            if action != "help" and creature == "Zeus":
                return judgments[creature]["other"]
            if action != "steal" and creature == "Cerberus":
                return judgments[creature]["other"]
    return "No judgment found"