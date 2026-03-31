class PhenomenaMonitor:
    def __init__(self):
        self.phenomena = []

    def add_phenomenon(self, phenomenon):
        self.phenomena.append(phenomenon)

    def get_phenomena_by_type(self, phenomenon_type):
        return [phenomenon for phenomenon in self.phenomena if phenomenon['type'] == phenomenon_type]

    def get_severity_count(self):
        severity_count = {}
        for phenomenon in self.phenomena:
            severity = phenomenon.get('severity')
            if severity:
                if severity not in severity_count:
                    severity_count[severity] = 0
                severity_count[severity] += 1
        return severity_count

    def add_observation(self, phenomenon_index, note):
        try:
            self.phenomena[phenomenon_index]['observation_notes'].append(note)
        except IndexError as e:
            print(f"Error: {e}. Phenomenon index {phenomenon_index} is out of range.")

# Example usage
monitor = PhenomenaMonitor()
monitor.add_phenomenon({"type": "Aurora", "severity": "low", "observation_notes": []})
print(monitor.get_phenomena_by_type("Aurora"))
monitor.add_observation(0, "A brilliant display of light.")
print(monitor.get_phenomena_by_type("Aurora"))
print(monitor.get_severity_count())