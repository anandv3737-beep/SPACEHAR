import atexit
import json
import threading
import time

from flask import (
    Flask,
    Response,
    jsonify,
    render_template
)

from config import HOST, PORT, DEBUG

from video.camera import CameraManager
from video.streamer import generate_frames
from video.recorder import VideoRecorder

from ai.detector import ObjectDetector
from ai.tracker import CentroidTracker
from ai.activity_recognition import ActivityRecognizer
from ai.pipeline import AIPipeline
from ai.sequence_validator import SequenceValidator

from experiment.logger import ExperimentLogger
from experiment.session import ExperimentSession

from alerts.alert_manager import AlertManager
from alerts.voice_alert import VoiceAlert


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
    template_folder="dashboard/templates",
    static_folder="dashboard/static"
)


# ============================================================
# LOAD EXPERIMENT
# ============================================================

def load_experiment():

    with open(
        "experiment/experiment.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


experiment = load_experiment()


# ============================================================
# COMPONENTS
# ============================================================

camera = CameraManager()

recorder = VideoRecorder(camera)

detector = ObjectDetector()

tracker = CentroidTracker()

recognizer = ActivityRecognizer(
    window_size=15,
    min_frames=5
)

pipeline = AIPipeline(
    camera,
    detector,
    tracker,
    recognizer
)

validator = SequenceValidator(
    experiment
)

logger = ExperimentLogger()

session = ExperimentSession()

alerts = AlertManager()

voice = VoiceAlert()


# ============================================================
# STATE
# ============================================================

experiment_running = False

state_lock = threading.Lock()

last_logged_activity = None


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# CAMERA START
# ============================================================

@app.route("/api/start", methods=["POST"])
def start_camera():

    success = camera.start()

    if not success:

        return jsonify({
            "success": False,
            "message": "Unable to start camera."
        }), 500

    pipeline.start()

    return jsonify({
        "success": True,
        "message": "Camera and AI pipeline started."
    })


# ============================================================
# CAMERA STOP
# ============================================================

@app.route("/api/stop", methods=["POST"])
def stop_camera():

    pipeline.stop()

    camera.stop()

    return jsonify({
        "success": True,
        "message": "Camera and AI pipeline stopped."
    })


# ============================================================
# VIDEO STREAM
# ============================================================

@app.route("/video_feed")
def video_feed():

    return Response(
        generate_frames(camera),
        mimetype=(
            "multipart/x-mixed-replace; "
            "boundary=frame"
        )
    )


# ============================================================
# STATUS
# ============================================================

@app.route("/api/status")
def status():

    ai_result = pipeline.get_result()

    sequence = validator.status()

    current_step = sequence.get(
        "current_step"
    )

    next_step = sequence.get(
        "next_step"
    )

    return jsonify({

        "camera": {
            "running": camera.running
        },

        "recording": {
            "running": recorder.recording,
            "file": recorder.current_file
        },

        "experiment": {
            "running": experiment_running,
            "name": experiment.get("name"),
            "progress": sequence.get(
                "progress",
                0
            ),
            "current_step": current_step,
            "next_step": next_step,
            "finished": sequence.get(
                "finished",
                False
            )
        },

        "ai": ai_result,

        "session": session.info(),

        "alerts": len(
            alerts.get_all()
        )
    })


# ============================================================
# START EXPERIMENT
# ============================================================

@app.route(
    "/api/experiment/start",
    methods=["POST"]
)
def start_experiment():

    global experiment_running
    global last_logged_activity

    with state_lock:

        validator.reset()

        session.start()

        experiment_running = True

        last_logged_activity = None

    if not camera.running:

        success = camera.start()

        if not success:

            return jsonify({
                "success": False,
                "message": "Camera could not start."
            }), 500

    pipeline.start()

    recording_file = recorder.start()

    logger.log(
        "SYSTEM",
        1.0,
        "EXPERIMENT_STARTED",
        {
            "session_id":
                session.session_id,
            "recording":
                recording_file
        }
    )

    return jsonify({
        "success": True,
        "message": "Experiment started.",
        "session": session.info()
    })


# ============================================================
# STOP EXPERIMENT
# ============================================================

@app.route(
    "/api/experiment/stop",
    methods=["POST"]
)
def stop_experiment():

    global experiment_running

    with state_lock:

        experiment_running = False

    recording_file = recorder.stop()

    session_info = session.stop()

    logger.log(
        "SYSTEM",
        1.0,
        "EXPERIMENT_STOPPED",
        {
            "session_id":
                session_info["session_id"],
            "recording":
                recording_file
        }
    )

    return jsonify({
        "success": True,
        "message": "Experiment stopped.",
        "session": session_info
    })


# ============================================================
# PROCESS CURRENT AI ACTIVITY
# ============================================================

@app.route(
    "/api/process_activity",
    methods=["POST"]
)
def process_activity():

    global last_logged_activity

    if not experiment_running:

        return jsonify({
            "success": False,
            "message": "Experiment is not running."
        })

    result = pipeline.get_result()

    activity = result.get(
        "activity",
        "IDLE"
    )

    confidence = result.get(
        "confidence",
        0.0
    )

    validation = validator.process(
        activity
    )

    event = validation.get(
        "event"
    )

    if event == "STEP_COMPLETED":

        logger.log(
            activity,
            confidence,
            "STEP_COMPLETED",
            {
                "validation": validation,
                "session_id":
                    session.session_id
            }
        )

        alerts.add(
            f"Step completed: {activity}",
            "success"
        )

        voice.speak(
            f"{activity} step completed"
        )

    elif event == "SEQUENCE_VIOLATION":

        logger.log(
            activity,
            confidence,
            "SEQUENCE_VIOLATION",
            {
                "validation": validation,
                "session_id":
                    session.session_id
            }
        )

        alerts.add(
            f"Sequence violation. "
            f"Expected next step.",
            "danger"
        )

        voice.speak(
            "Sequence violation detected"
        )

    elif (
        activity != "IDLE"
        and activity != last_logged_activity
    ):

        logger.log(
            activity,
            confidence,
            "ACTIVITY",
            {
                "session_id":
                    session.session_id
            }
        )

        last_logged_activity = activity

    if validation.get("finished"):

        alerts.add(
            "Experiment sequence completed.",
            "success"
        )

    return jsonify({
        "success": True,
        "activity": activity,
        "confidence": confidence,
        "validation": validation
    })


# ============================================================
# EVENTS
# ============================================================

@app.route("/api/events")
def events():

    return jsonify(
        logger.get_events(50)
    )


# ============================================================
# ALERTS
# ============================================================

@app.route("/api/alerts")
def get_alerts():

    return jsonify(
        alerts.get_all()
    )


# ============================================================
# CLEAR ALERTS
# ============================================================

@app.route(
    "/api/alerts/clear",
    methods=["POST"]
)
def clear_alerts():

    alerts.clear()

    return jsonify({
        "success": True
    })


# ============================================================
# RESET EXPERIMENT
# ============================================================

@app.route(
    "/api/experiment/reset",
    methods=["POST"]
)
def reset_experiment():

    global last_logged_activity

    validator.reset()

    last_logged_activity = None

    alerts.clear()

    return jsonify({
        "success": True,
        "message": "Experiment state reset."
    })


# ============================================================
# SHUTDOWN
# ============================================================

def shutdown():

    print("Shutting down SpaceHAR...")

    try:
        recorder.stop()
    except Exception:
        pass

    try:
        pipeline.stop()
    except Exception:
        pass

    try:
        camera.stop()
    except Exception:
        pass


atexit.register(shutdown)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("")
    print("====================================")
    print("        SPACEHAR AI SYSTEM")
    print("====================================")
    print("")
    print(
        f"Open: http://localhost:{PORT}"
    )
    print(
        f"LAN: http://<YOUR-IP>:{PORT}"
    )
    print("")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
        threaded=True
    )