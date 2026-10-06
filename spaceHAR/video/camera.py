import cv2
import threading
import time

from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    FRAME_FPS
)


class CameraManager:
    def __init__(self):
        self.camera = None
        self.latest_frame = None
        self.running = False
        self.lock = threading.Lock()
        self.thread = None

    def start(self):
        if self.running:
            return True

        self.camera = cv2.VideoCapture(CAMERA_INDEX)

        if not self.camera.isOpened():
            print("ERROR: Unable to open camera.")
            return False

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        self.camera.set(cv2.CAP_PROP_FPS, FRAME_FPS)

        self.running = True

        self.thread = threading.Thread(
            target=self._capture_loop,
            daemon=True
        )

        self.thread.start()

        print("Camera started successfully.")

        return True

    def _capture_loop(self):
        frame_delay = 1 / FRAME_FPS

        while self.running:

            if self.camera is None:
                break

            success, frame = self.camera.read()

            if not success:
                print("WARNING: Failed to read camera frame.")
                time.sleep(0.1)
                continue

            with self.lock:
                self.latest_frame = frame.copy()

            time.sleep(frame_delay)

    def get_frame(self):
        with self.lock:
            if self.latest_frame is None:
                return None

            return self.latest_frame.copy()

    def get_jpeg(self):
        frame = self.get_frame()

        if frame is None:
            return None

        success, buffer = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 80]
        )

        if not success:
            return None

        return buffer.tobytes()

    def stop(self):
        self.running = False

        if self.thread is not None:
            self.thread.join(timeout=2)

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        with self.lock:
            self.latest_frame = None

        print("Camera stopped.")

    def restart(self):
        self.stop()
        time.sleep(0.5)
        return self.start()