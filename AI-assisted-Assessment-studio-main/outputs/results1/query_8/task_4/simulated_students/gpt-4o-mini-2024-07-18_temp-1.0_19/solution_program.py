def mythological_judgment(creature, action):
    judgments = {
        'Zeus': {
            'help': "Blessing granted",
            'default': "Storms befall you"
        },
        'Cerberus': {
            'steal': "Growling disapproval",
            'default': "Pass freely"
        },
        'Aphrodite': {
            'love': "Heart's desire fulfilled"
        }
    }

    if creature in judgments:
        if action in judgments[creature]:
            return judgments[creature][action]
        else:
            return judgments[creature].get('default', "No judgment found")
    return "No judgment found"