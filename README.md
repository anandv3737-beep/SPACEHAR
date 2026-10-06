🚀 SpaceHAR
AI-Powered Human Activity Recognition System for Autonomous Space Experiment Monitoring
SpaceHAR is an AI-powered prototype designed to monitor astronaut activities during scientific experiments using local camera feeds and edge AI processing. The system recognizes people and relevant objects, tracks experiment activities, validates whether predefined experiment steps are performed in the correct order, and provides alerts when an incorrect or skipped step is detected. It also provides a real-time mission-control dashboard, experiment logging, video monitoring, and local video recording. The prototype is designed with an offline-first architecture so that the core monitoring pipeline can operate without continuous cloud connectivity.

🎯 Problem Statement
During space missions, astronauts may perform complex scientific experiments where every step must be completed correctly and in the required sequence.

Communication delays between spacecraft and ground stations can make continuous real-time supervision difficult.

SpaceHAR aims to provide an onboard AI-assisted monitoring system that can:

Monitor astronaut activities using local camera feeds
Detect people and relevant experiment objects
Recognize experiment-related activities
Validate the predefined experiment sequence
Identify skipped or incorrect steps
Suggest the next experiment step
Provide voice alerts
Generate timestamped experiment logs
Store experiment video locally
Operate using local edge processing
💡 Proposed Solution
SpaceHAR combines computer vision, activity recognition, sequence validation, and a web-based mission dashboard.

System Flow
                    CAMERA
                       │
                       ▼
              ┌─────────────────┐
              │ Video Processing│
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ YOLO Detection  │
              │ Person / Object │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Activity        │
              │ Recognition     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Sequence        │
              │ Validator       │
              └────────┬────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Correct       Warning     Next Step
          │            │            │
          ▼            ▼            ▼
       Logging     Voice Alert   Dashboard
                       │
                       ▼
                Local Monitoring
                Current Prototype

The current Review 1 version demonstrates a controlled Sample Transfer Experiment.

Experiment Sequence
1. Pick Sample
       ↓
2. Move Sample
       ↓
3. Place Sample
       ↓
4. Activate Device
       ↓
5. Record Observation

The system validates whether activities occur according to this predefined sequence.

✨ Key Features
1. 🎥 Live Camera Monitoring

The system can access a local camera and display the live video feed through the web dashboard.

Features:

Local camera input
Browser-based live feed
Camera status monitoring
Visual telemetry interface
2. 🤖 AI Object Detection

SpaceHAR uses the YOLO object detection framework for real-time object detection.

The current prototype detects objects such as:

Person
Bottle
Other objects supported by the selected YOLO model

The detected objects are passed to the activity recognition module.

3. 🧠 Activity Recognition

The current Review 1 implementation contains a prototype activity recognition layer.

It uses detected objects and internal activity state to provide an initial classification of experiment-related activities.

Current prototype activities:

pick_sample
move_sample
place_sample
activate_device
record_observation

Note: This is currently a prototype activity classifier and is not yet a fully trained astronaut Human Activity Recognition model.

4. 🔄 Sequence Validation

The sequence validator compares the detected activity with the expected experiment step.

It can identify:

Correct step
Skipped step
Repeated step
Out-of-sequence activity
Experiment completion

Example:

Expected:
Pick Sample

Detected:
Move Sample

Result:
⚠ Step skipped
5. ➡️ Next-Step Recommendation

After completing a correct experiment step, SpaceHAR determines the next expected activity.

Example:

Completed:
Pick Sample

Next:
Move Sample

The next step is displayed on the dashboard.

6. 🔊 Voice Alerts

The system provides voice feedback using local text-to-speech.

Example alerts:

"Next experiment step is Move Sample."

"Warning. Incorrect experiment sequence."

"Warning. Experiment step skipped."

Voice alerts are generated locally.

7. 📝 Experiment Logging

The system generates timestamped experiment events.

Example:

{
    "timestamp": "2026-09-13T21:10:25",
    "detected_activity": "pick_sample",
    "expected_activity": "pick_sample",
    "status": "correct",
    "message": "pick_sample completed successfully."
}

The log is stored locally as:

experiment_log.json
8. 📹 Local Video Recording

SpaceHAR includes a prototype local video recording system.

Recorded experiment videos are stored in:

recordings/

Example:

recordings/
└── experiment_20260913_211500.mp4
9. 🖥️ Mission Control Dashboard

The project includes a modern web-based dashboard containing:

Mission status
Live camera feed
AI status
Detected objects
Recognized activity
Experiment progress
Procedure timeline
Current step
Next step
System telemetry
Activity logs
Prototype activity controls
🧪 Prototype Activity Test Console

The dashboard contains development controls for testing the sequence validation system.

Available test activities:

01  Pick Sample
02  Move Sample
03  Place Sample
04  Activate Device
05  Record Observation

These controls are clearly separated from the AI detection pipeline and are intended for prototype validation and demonstration.

🛠️ Technology Stack
Backend
Python
Flask
Computer Vision
OpenCV
YOLO / Ultralytics
AI / Activity Recognition
Python-based activity recognition prototype
Planned custom Human Activity Recognition model
Voice
pyttsx3
Frontend
HTML5
CSS3
JavaScript
Data
JSON-based experiment configuration
JSON-based experiment logs
📁 Project Structure
SpaceHAR/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── ai/
│   ├── detector.py
│   ├── activity_recognition.py
│   ├── sequence_validator.py
│   └── next_step.py
│
├── alerts/
│   └── voice_alert.py
│
├── experiment/
│   ├── experiment.json
│   └── logger.py
│
├── video/
│   ├── camera.py
│   ├── recorder.py
│   └── streamer.py
│
├── dashboard/
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── style.css
│       └── script.js
│
├── dataset/
│   └── README.md
│
├── models/
│   └── README.md
│
└── docs/
    └── REVIEW1.md
⚙️ Installation
Requirements
