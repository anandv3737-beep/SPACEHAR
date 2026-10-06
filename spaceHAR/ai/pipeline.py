import threading
import time


class AIPipeline:

    def __init__(self, camera, detector, tracker, recognizer):

        self.camera = camera
        self.detector = detector
        self.tracker = tracker
        self.recognizer = recognizer

        self.running = False
        self.thread = None

        self.lock = threading.Lock()

        self.latest_result = {
            "activity": "IDLE",
            "confidence": 0.0,
            "detections": [],
            "tracks": []
        }

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()

        print("AI pipeline started.")

    def _loop(self):

        while self.running:

            frame = self.camera.get_frame()

            if frame is None:
                time.sleep(0.1)
                continue

            try:

                detections = self.detector.detect(frame)

                tracks = self.tracker.update(
                    detections
                )

                activity_result = (
                    self.recognizer.update(
                        tracks,
                        detections
                    )
                )

                result = {
                    "activity": activity_result["activity"],
                    "confidence": activity_result["confidence"],
                    "detections": detections,
                    "tracks": tracks
                }

                with self.lock:
                    self.latest_result = result

            except Exception as error:

                print(
                    f"AI pipeline error: {error}"
                )

            time.sleep(0.05)

    def get_result(self):

        with self.lock:

            return {
                "activity": self.latest_result["activity"],
                "confidence": self.latest_result["confidence"],
                "detections": list(
                    self.latest_result["detections"]
                ),
                "tracks": list(
                    self.latest_result["tracks"]
                )
            }

    def stop(self):

        self.running = False

        if self.thread is not None:
            self.thread.join(timeout=2)

        print("AI pipeline stopped.")