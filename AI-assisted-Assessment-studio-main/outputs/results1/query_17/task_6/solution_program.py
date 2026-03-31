class Alien:
    def __init__(self, name, species, skills):
        self.name = name
        self.species = species
        self.skills = skills

    def has_skills_for_mission(self, mission_requirements):
        for skill, min_level in mission_requirements.items():
            if self.skills.get(skill, 0) < min_level:
                return False
        return True

def assign_mission(aliens, mission_requirements):
    eligible_aliens = []
    for alien in aliens:
        if alien.has_skills_for_mission(mission_requirements):
            eligible_aliens.append(alien)
    if not eligible_aliens:
        raise ValueError("No suitable aliens found")
    return eligible_aliens