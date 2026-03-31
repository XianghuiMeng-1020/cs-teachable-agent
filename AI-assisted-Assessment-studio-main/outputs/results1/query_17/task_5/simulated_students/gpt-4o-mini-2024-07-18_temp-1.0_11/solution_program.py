class PhenomenaMonitor:
    def __init__(self):
        self.phenomena = []

    def add_phenomenon(self, phenomenon):
        self.phenomena.append(phenomenon)

    def get_phenomena_by_type(self, phenomenon_type):
        return [phenomena for phenomena in self.phenomena if phenomena['type'] == phenomenon_type]

    def get_severity_count(self):
        severity_count = {}
        for phenomena in self.phenomena:
            severity = phenomena['severity']
            if severity in severity_count:
                severity_count[severity] += 1
            else:
                severity_count[severity] = 1
        return severity_count

    def add_observation(self, phenomenon_index, note):
        try:
            self.phenomena[phenomenon_index]['observation_notes'].append(note)
        except IndexError:
            pass