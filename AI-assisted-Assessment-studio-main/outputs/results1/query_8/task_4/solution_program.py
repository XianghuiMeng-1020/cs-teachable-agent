def mythological_judgment(creature, action):
    judgments = {
        "zeus": {
            "help": "Blessing granted",
            "other": "Storms befall you"
        },
        "cerberus": {
            "steal": "Growling disapproval",
            "other": "Pass freely"
        },
        "aphrodite": {
            "love": "Heart's desire fulfilled"
        }
    }
    if creature in judgments:
        if action in judgments[creature]:
            return judgments[creature][action]
        elif "other" in judgments[creature]:
            return judgments[creature]["other"]
    return "No judgment found"