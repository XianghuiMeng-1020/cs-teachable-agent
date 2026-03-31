class PhenomenaMonitor:
    def __init__(self):
        self.phenomena_list = []

    def add_phenomenon(self, phenomenon):
        self.phenomena_list.append(phenomenon)

    def get_phenomena_by_type(self, phenomenon_type):
        return [phenomenon for phenomenon in self.phenomena_list if phenomenon['type'] == phenomenon_type]

    def get_severity_count(self):
        severity_count = {}
        for phenomenon in self.phenomena_list:
            severity = phenomenon['severity']
            if severity in severity_count:
                severity_count[severity] += 1
            else:
                severity_count[severity] = 1
        return severity_count

    def add_observation(self, phenomenon_index, note):
        try:
            self.phenomena_list[phenomenon_index]['observation_notes'].append(note)
        except IndexError:
            pass