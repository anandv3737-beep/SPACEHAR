import cv2
import time
from pathlib import Path

from config import (
    RECORDINGS_DIR,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    FRAME_FPS
)


class VideoRecorder:

    def __init__(self, camera):
        self.camera = camera
        self.recording = False
        self.writer = None
        self.thread = None
        self.current_file = None

    def start(self):
        if self.recording:
            return self.current_file

        timestamp = time.strftime("%Y%m%d_%H%M%S")

        filename = f"spacehar_{timestamp}.mp4"
        filepath = Path(RECORDINGS_DIR) / filename

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        self.writer = cv2.VideoWriter(
            str(filepath),
            fourcc,
            FRAME_FPS,
            (FRAME_WIDTH, FRAME_HEIGHT)
        )

        if not self.writer.isOpened():
            self.writer = None
            return None

        self.current_file = str(filepath)
        self.recording = True

        import threading

        self.thread = threading.Thread(
            target=self._record_loop,
            daemon=True
        )

        self.thread.start()

        print(f"Recording started: {filepath}")

        return self.current_file

    def _record_loop(self):

        while self.recording:

            frame = self.camera.get_frame()

            if frame is not None and self.writer is not None:
                self.writer.write(frame)

            time.sleep(1 / FRAME_FPS)

    def stop(self):

        self.recording = False

        if self.thread is not None:
            self.thread.join(timeout=2)

        if self.writer is not None:
            self.writer.release()
            self.writer = None

        filepath = self.current_file
        self.current_file = None

        print("Recording stopped.")

        return filepath