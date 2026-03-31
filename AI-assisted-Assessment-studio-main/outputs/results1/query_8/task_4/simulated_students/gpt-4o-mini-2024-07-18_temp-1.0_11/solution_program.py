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
            'love': "Heart's desire fulfilled",
            'default': "No judgment found"
        }
    }

    creature_judgments = judgments.get(creature, None)
    if creature_judgments:
        return creature_judgments.get(action, creature_judgments['default'])
    return "No judgment found"