import time


class SequenceValidator:

    def __init__(self, experiment):

        self.experiment = experiment

        self.steps = experiment.get("steps", [])

        self.current_index = 0

        self.completed_steps = []

        self.violations = []

        self.last_activity = None

        self.last_event_time = 0

    def process(self, activity):

        now = time.time()

        if not activity:
            return self.status()

        if activity == self.last_activity:
            return self.status()

        self.last_activity = activity

        if self.current_index >= len(self.steps):
            return self.status()

        expected = self.steps[self.current_index]

        expected_activity = expected.get("activity")

        if activity == expected_activity:

            step_record = {
                "step": expected.get("name"),
                "activity": activity,
                "timestamp": now
            }

            self.completed_steps.append(step_record)

            self.current_index += 1

            self.last_event_time = now

            return self.status(
                event="STEP_COMPLETED",
                valid=True
            )

        if activity == "IDLE":
            return self.status()

        violation = {
            "expected": expected_activity,
            "received": activity,
            "timestamp": now
        }

        self.violations.append(violation)

        return self.status(
            event="SEQUENCE_VIOLATION",
            valid=False
        )

    def status(self, event=None, valid=None):

        total = len(self.steps)

        completed = self.current_index

        if total > 0:
            progress = int((completed / total) * 100)
        else:
            progress = 0

        current_step = None
        next_step = None

        if self.current_index < total:

            current_step = self.steps[
                self.current_index
            ]

        if self.current_index + 1 < total:

            next_step = self.steps[
                self.current_index + 1
            ]

        return {
            "current_step": current_step,
            "next_step": next_step,
            "completed_steps": self.completed_steps,
            "violations": self.violations,
            "progress": progress,
            "finished": self.current_index >= total,
            "event": event,
            "valid": valid
        }

    def reset(self):

        self.current_index = 0
        self.completed_steps = []
        self.violations = []
        self.last_activity = None
        self.last_event_time = 0