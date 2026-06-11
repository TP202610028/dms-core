from datetime import datetime

class SessionMetrics:

    def __init__(self):

        self.start_time = datetime.now()

        self.yawns = 0
        self.fatigue_events = 0
        self.microsleeps = 0
        self.distractions = 0
        self.vertical_distractions = 0
        self.face_missing_events = 0

        self.perclos_values = []
        self.risk_values = []

    def add_perclos(self, value):
        self.perclos_values.append(value)

    def add_risk(self, value):
        self.risk_values.append(value)
        
    def average_perclos(self):
        if not self.perclos_values:
            return 0

        return sum(self.perclos_values) / len(self.perclos_values)


    def average_risk(self):
        if not self.risk_values:
            return 0

        return sum(self.risk_values) / len(self.risk_values)
    
    def max_risk(self):
        if not self.risk_values:
            return 0

        return max(self.risk_values)
    
    def duration_seconds(self):
        return (
            datetime.now() - self.start_time
        ).total_seconds()