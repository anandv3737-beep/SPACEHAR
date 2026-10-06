import math


class CentroidTracker:

    def __init__(self, max_distance=100, max_missing=15):

        self.next_id = 1
        self.objects = {}

        self.max_distance = max_distance
        self.max_missing = max_missing

    def update(self, detections):

        person_detections = [
            d for d in detections
            if d["class_name"] == "person"
        ]

        updated = {}

        used_ids = set()

        for detection in person_detections:

            cx, cy = detection["center"]

            best_id = None
            best_distance = float("inf")

            for object_id, obj in self.objects.items():

                if object_id in used_ids:
                    continue

                old_x, old_y = obj["center"]

                distance = math.sqrt(
                    (cx - old_x) ** 2 +
                    (cy - old_y) ** 2
                )

                if distance < best_distance:
                    best_distance = distance
                    best_id = object_id

            if (
                best_id is not None
                and best_distance <= self.max_distance
            ):

                object_id = best_id

            else:

                object_id = self.next_id
                self.next_id += 1

            previous = self.objects.get(object_id)

            if previous:

                old_x, old_y = previous["center"]

                dx = cx - old_x
                dy = cy - old_y

                movement = math.sqrt(dx * dx + dy * dy)

            else:

                dx = 0
                dy = 0
                movement = 0

            updated[object_id] = {
                "id": object_id,
                "center": (cx, cy),
                "bbox": detection["bbox"],
                "confidence": detection["confidence"],
                "movement": round(movement, 2),
                "velocity": {
                    "x": dx,
                    "y": dy
                },
                "moving": movement > 8,
                "missing": 0
            }

            used_ids.add(object_id)

        for object_id, obj in self.objects.items():

            if object_id not in updated:

                obj["missing"] += 1

                if obj["missing"] <= self.max_missing:
                    updated[object_id] = obj

        self.objects = updated

        return list(self.objects.values())