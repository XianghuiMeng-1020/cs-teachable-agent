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
    creature_judgment = judgments.get(creature)
    if creature_judgment:
        return creature_judgment.get(action, creature_judgment['default'])
    return "No judgment found"