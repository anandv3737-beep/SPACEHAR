class ActivityModel:

    """
    Interface for the future trained HAR model.

    Phase 2 currently uses the temporal
    rule-based recognizer.

    A trained ML/DL model can later replace
    this class without changing the rest
    of the application.
    """

    def __init__(self):

        self.model_loaded = False

    def load(self, model_path):

        # Future trained model loading
        self.model_loaded = True

    def predict(self, sequence):

        if not self.model_loaded:

            return {
                "activity": "UNKNOWN",
                "confidence": 0.0
            }

        # Future ML prediction

        return {
            "activity": "UNKNOWN",
            "confidence": 0.0
        }