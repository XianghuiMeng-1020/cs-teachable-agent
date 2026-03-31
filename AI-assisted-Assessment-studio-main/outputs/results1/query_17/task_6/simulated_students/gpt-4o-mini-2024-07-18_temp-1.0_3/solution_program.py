class Alien:
    def __init__(self, name, species, skills):
        self.name = name
        self.species = species
        self.skills = skills


def assign_mission(aliens, mission_requirements):
    suitable_aliens = []
    for alien in aliens:
        meets_requirements = True
        for skill, required_level in mission_requirements.items():
            alien_skill_level = alien.skills.get(skill, 0)
            if alien_skill_level < required_level:
                meets_requirements = False
                break
        if meets_requirements:
            suitable_aliens.append(alien)
    
    if not suitable_aliens:
        raise ValueError("No suitable aliens found")
    
    return suitable_aliens