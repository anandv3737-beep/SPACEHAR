class ActivityModel:

    """
    Future trained Human Activity Recognition model.

    Phase 2 currently uses the rule-based temporal
    recognizer in ai/activity_recognition.py.

    This class provides a clean interface for replacing
    the rule-based system with a trained model later.
    """

    def __init__(self, model_path=None):

        self.model_path = model_path
        self.loaded = False

    def load(self):

        if not self.model_path:
            return False

        # Future:
        # Load TensorFlow / PyTorch / ONNX model here.

        self.loaded = False

        return self.loaded

    def predict(self, sequence):

        if not self.loaded:

            return {
                "activity": "UNKNOWN",
                "confidence": 0.0
            }

        return {
            "activity": "UNKNOWN",
            "confidence": 0.0
        }