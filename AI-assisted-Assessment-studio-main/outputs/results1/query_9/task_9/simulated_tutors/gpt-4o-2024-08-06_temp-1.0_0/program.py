def analyze_mythical_creatures(creatures):
    # Initialize variables to store the total number of stories, creature counts, and origin counts
    total_stories = 0
    creature_count = {}
    origin_count = {}

    # Iterate over each creature in the list
    for creature in creatures:
        # Extract creature details
        name = creature['name']
        story_count = creature['story_count']
        origin = creature['origin']

        # Update the total number of stories
        total_stories += story_count

        # Update the count of stories per creature
        if name in creature_count:
            creature_count[name] += story_count
        else:
            creature_count[name] = story_count

        # Update the count of stories per origin
        if origin in origin_count:
            origin_count[origin] += story_count
        else:
            origin_count[origin] = story_count

    # Return the results as a dictionary
    return {
        'total_stories': total_stories,
        'creature_count': creature_count,
        'origin_count': origin_count
    }