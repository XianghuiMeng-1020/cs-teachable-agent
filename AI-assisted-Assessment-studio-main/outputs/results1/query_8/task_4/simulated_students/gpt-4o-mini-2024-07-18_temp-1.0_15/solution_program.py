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

    return judgments.get(creature, {}).get(action, judgments.get(creature, {}).get('default', 'No judgment found'))