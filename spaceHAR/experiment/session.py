import time
import uuid


class ExperimentSession:

    def __init__(self):

        self.session_id = None
        self.start_time = None
        self.end_time = None
        self.active = False

    def start(self):

        self.session_id = str(
            uuid.uuid4()
        )

        self.start_time = time.time()
        self.end_time = None
        self.active = True

        return self.info()

    def stop(self):

        self.end_time = time.time()
        self.active = False

        return self.info()

    def info(self):

        return {
            "session_id": self.session_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "active": self.active
        }