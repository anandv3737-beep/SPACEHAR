import time


class AlertManager:

    def __init__(self, max_alerts=50):

        self.alerts = []
        self.max_alerts = max_alerts

    def add(
        self,
        message,
        level="warning"
    ):

        alert = {
            "timestamp": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "message": message,
            "level": level
        }

        self.alerts.append(alert)

        if len(self.alerts) > self.max_alerts:

            self.alerts = self.alerts[
                -self.max_alerts:
            ]

        return alert

    def get_all(self):

        return list(reversed(self.alerts))

    def clear(self):

        self.alerts = []