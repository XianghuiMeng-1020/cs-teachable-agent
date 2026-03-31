def analyze_mythical_creatures(creatures):
    total_stories = 0
    creature_count = {}
    origin_count = {}

    for creature in creatures:
        name = creature['name']
        story_count = creature['story_count']
        origin = creature['origin']

        total_stories += story_count
        creature_count[name] = story_count

        if origin not in origin_count:
            origin_count[origin] = 0
        origin_count[origin] += story_count

    return {
        'total_stories': total_stories,
        'creature_count': creature_count,
        'origin_count': origin_count,
    }