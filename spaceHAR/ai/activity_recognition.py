from collections import deque
import math


class ActivityRecognizer:

    def __init__(self, window_size=15, min_frames=5):

        self.window_size = window_size
        self.min_frames = min_frames

        self.history = deque(maxlen=window_size)

        self.current_activity = "IDLE"
        self.confidence = 0.0

    def update(self, tracked_objects, detections):

        persons = [
            obj for obj in tracked_objects
            if obj["missing"] == 0
        ]

        bottles = [
            d for d in detections
            if d["class_name"] == "bottle"
        ]

        if not persons:

            self.history.append("IDLE")

            self.current_activity = "IDLE"
            self.confidence = 0.95

            return self._result()

        person = persons[0]

        movement = person["movement"]

        activity = "IDLE"
        confidence = 0.70

        if movement > 25:

            activity = "MOVE"
            confidence = 0.80

        elif movement > 10:

            activity = "APPROACH"
            confidence = 0.75

        if bottles:

            person_x, person_y = person["center"]

            closest_distance = float("inf")

            for bottle in bottles:

                bx, by = bottle["center"]

                distance = math.sqrt(
                    (person_x - bx) ** 2 +
                    (person_y - by) ** 2
                )

                closest_distance = min(
                    closest_distance,
                    distance
                )

            if closest_distance < 180:

                if movement > 12:

                    activity = "PICK"
                    confidence = 0.72

                else:

                    activity = "PLACE"
                    confidence = 0.68

        self.history.append(activity)

        stable_activity = self._stable_activity()

        self.current_activity = stable_activity

        return self._result(confidence)

    def _stable_activity(self):

        if len(self.history) < self.min_frames:
            return self.current_activity

        recent = list(self.history)[-self.min_frames:]

        counts = {}

        for activity in recent:
            counts[activity] = counts.get(activity, 0) + 1

        best_activity = max(
            counts,
            key=counts.get
        )

        if counts[best_activity] >= self.min_frames:

            return best_activity

        return self.current_activity

    def _result(self, confidence=None):

        if confidence is None:
            confidence = self.confidence

        self.confidence = confidence

        return {
            "activity": self.current_activity,
            "confidence": round(self.confidence, 3)
        }