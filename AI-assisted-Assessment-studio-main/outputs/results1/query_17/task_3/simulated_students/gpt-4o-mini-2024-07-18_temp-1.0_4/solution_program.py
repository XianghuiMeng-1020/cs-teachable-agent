class Spaceship:
    def __init__(self, name, captain='Unknown'):
        self.name = name
        self.captain = captain
        self.missions = []

    def add_mission(self, mission_type):
        valid_missions = ['Reconnaissance', 'Transport', 'Combat']
        if mission_type not in valid_missions:
            raise ValueError('Invalid mission type')
        self.missions.append(mission_type)

    def get_missions_summary(self):
        summary = {
            'Reconnaissance': 0,
            'Transport': 0,
            'Combat': 0
        }
        for mission in self.missions:
            if mission in summary:
                summary[mission] += 1
        return summary