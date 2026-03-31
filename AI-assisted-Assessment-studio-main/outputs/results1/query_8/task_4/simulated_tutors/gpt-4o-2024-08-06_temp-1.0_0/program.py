def mythological_judgment(creature, action):
    judgments = {
        "zeus": {
            "help": "Blessing granted",
        },
        "cerberus": {
            "steal": "Growling disapproval",
        },
        "aphrodite": {
            "love": "Heart's desire fulfilled",
        }
    }
    
    # Default judgments
    default_judgments = {
        "zeus": "Storms befall you",
        "cerberus": "Pass freely",
    }
    
    # Check for special judgments first
    if creature in judgments and action in judgments[creature]:
        return judgments[creature][action]
    # Check for default judgments
    elif creature in default_judgments:
        return default_judgments[creature]
    else:
        return "No judgment found"
