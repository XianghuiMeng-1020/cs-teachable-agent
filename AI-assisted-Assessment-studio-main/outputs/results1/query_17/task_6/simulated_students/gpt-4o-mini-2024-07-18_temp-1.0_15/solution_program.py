class Alien:
    def __init__(self, name, species, skills):
        self.name = name
        self.species = species
        self.skills = skills


def assign_mission(aliens, mission_requirements):
    suitable_aliens = []
    for alien in aliens:
        if all(alien.skills.get(skill, 0) >= level for skill, level in mission_requirements.items()):
            suitable_aliens.append(alien)
    if not suitable_aliens:
        raise ValueError('No suitable aliens found')
    return suitable_aliens