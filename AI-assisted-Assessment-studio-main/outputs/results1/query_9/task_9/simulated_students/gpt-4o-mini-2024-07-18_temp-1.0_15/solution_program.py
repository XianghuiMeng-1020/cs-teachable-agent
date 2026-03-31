def analyze_mythical_creatures(creatures):
    total_stories = 0
    creature_count = {}
    origin_count = {}

    for creature in creatures:
        total_stories += creature['story_count']
        creature_count[creature['name']] = creature['story_count']
        origin = creature['origin']
        if origin in origin_count:
            origin_count[origin] += creature['story_count']
        else:
            origin_count[origin] = creature['story_count']

    return {
        'total_stories': total_stories,
        'creature_count': creature_count,
        'origin_count': origin_count
    }