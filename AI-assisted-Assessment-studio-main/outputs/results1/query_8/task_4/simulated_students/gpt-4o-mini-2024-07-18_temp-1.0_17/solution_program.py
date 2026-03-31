def mythological_judgment(creature, action):
    judgments = {
        'Zeus': {
            'help': 'Blessing granted',
            'default': 'Storms befall you'
        },
        'Cerberus': {
            'steal': 'Growling disapproval',
            'default': 'Pass freely'
        },
        'Aphrodite': {
            'love': 'Heart's desire fulfilled',
            'default': 'No judgment found'
        }
    }

    if creature in judgments:
        return judgments[creature].get(action, judgments[creature]['default'])
    else:
        return 'No judgment found'