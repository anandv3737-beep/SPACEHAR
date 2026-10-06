import json
import time
from pathlib import Path

from config import LOGS_DIR


class ExperimentLogger:

    def __init__(self):

        self.log_file = Path(
            LOGS_DIR
        ) / "experiment_log.json"

        self.events = []

        self._load()

    def _load(self):

        if not self.log_file.exists():

            self.events = []

            return

        try:

            with open(
                self.log_file,
                "r",
                encoding="utf-8"
            ) as file:

                self.events = json.load(file)

        except Exception:

            self.events = []

    def log(
        self,
        activity,
        confidence=0.0,
        event_type="ACTIVITY",
        details=None
    ):

        event = {
            "timestamp": time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "event_type": event_type,
            "activity": activity,
            "confidence": confidence,
            "details": details or {}
        }

        self.events.append(event)

        self._save()

        return event

    def _save(self):

        self.log_file.parent.mkdir(
            exist_ok=True
        )

        with open(
            self.log_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.events,
                file,
                indent=4
            )

    def get_events(self, limit=50):

        return self.events[-limit:]

    def clear(self):

        self.events = []

        self._save()