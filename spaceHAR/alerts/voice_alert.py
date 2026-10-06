import threading

import pyttsx3


class VoiceAlert:

    def __init__(self):

        self.enabled = True

    def speak(self, message):

        if not self.enabled:
            return

        thread = threading.Thread(
            target=self._speak,
            args=(message,),
            daemon=True
        )

        thread.start()

    def _speak(self, message):

        try:

            engine = pyttsx3.init()

            engine.say(message)

            engine.runAndWait()

            engine.stop()

        except Exception as error:

            print(
                f"Voice alert error: {error}"
            )

    def set_enabled(self, enabled):

        self.enabled = bool(enabled)