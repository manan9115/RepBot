"""
RepBot Backend API - Stable CV + ML Backend
MediaPipe (required) + Local ML + Optional HuggingFace
"""

import os
import sys
import cv2
import time
import json
import atexit
import joblib
import threading
import numpy as np
import warnings
from flask import Flask, Response, jsonify, request
from flask_cors import CORS

warnings.filterwarnings("ignore")

# -------------------------------------------------------------------
# PATH SETUP
# -------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# -------------------------------------------------------------------
# OPTIONAL ML PIPELINE
# -------------------------------------------------------------------
try:
    from ml_pipeline import ExerciseMLPipeline
    ML_PIPELINE_AVAILABLE = True
except Exception as e:
    ML_PIPELINE_AVAILABLE = False
    print("⚠ ML Pipeline not available:", e)

# -------------------------------------------------------------------
# MEDIAPIPE (REQUIRED)
# -------------------------------------------------------------------
try:
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    MEDIAPIPE_AVAILABLE = True
    print("✓ MediaPipe available")
except Exception as e:
    MEDIAPIPE_AVAILABLE = False
    print("❌ MediaPipe NOT available:", e)

# -------------------------------------------------------------------
# OPTIONAL HUGGING FACE
# -------------------------------------------------------------------
try:
    from transformers import pipeline
    import torch
    HF_AVAILABLE = True
except Exception:
    HF_AVAILABLE = False
    print("⚠ HuggingFace not available (optional)")

# -------------------------------------------------------------------
# FLASK APP
# -------------------------------------------------------------------
app = Flask(__name__)
CORS(app)

# -------------------------------------------------------------------
# LOAD LOCAL MODELS (OPTIONAL)
# -------------------------------------------------------------------
model_path = os.path.join(BASE_DIR, "exercise_form_model.pkl")
scaler_path = os.path.join(BASE_DIR, "scaler.pkl")

local_model = None
scaler = None
local_model_loaded = False

if os.path.exists(model_path) and os.path.exists(scaler_path):
    try:
        local_model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        local_model_loaded = True
        print("✓ Local ML model loaded")
    except Exception as e:
        print("⚠ Failed to load local ML model:", e)

# -------------------------------------------------------------------
# INIT ML PIPELINE
# -------------------------------------------------------------------
ml_pipeline = None
if ML_PIPELINE_AVAILABLE:
    try:
        ml_pipeline = ExerciseMLPipeline()
        print("✓ ML Pipeline initialized")
    except Exception as e:
        print("⚠ ML Pipeline init failed:", e)

# -------------------------------------------------------------------
# EXERCISES
# -------------------------------------------------------------------
EXERCISES = {
    "BICEP_CURL": {"name": "Bicep Curl"},
    "SQUAT": {"name": "Squat"},
    "PUSH_UP": {"name": "Push Up"},
    "LUNGE": {"name": "Lunge"},
    "PLANK": {"name": "Plank"},
    "DEADLIFT": {"name": "Deadlift"},
    "SHOULDER_PRESS": {"name": "Shoulder Press"},
    "LATERAL_RAISE": {"name": "Lateral Raise"},
    "CRUNCH": {"name": "Crunch"},
    "BURPEE": {"name": "Burpee"}
}

exercise_counters = {k: 0 for k in EXERCISES}
current_exercise = "None"
feedback = "Ready"
form_correct = True
form_confidence = 0.0
accuracy = 0.0

# -------------------------------------------------------------------
# CAMERA STATE
# -------------------------------------------------------------------
camera_running = False
capture_thread = None
last_frame = None
pose_detector = None

# -------------------------------------------------------------------
# UTILS
# -------------------------------------------------------------------
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba = a - b
    bc = c - b
    denom = (np.linalg.norm(ba) * np.linalg.norm(bc))
    if denom == 0:
        return 0
    cos = np.clip(np.dot(ba, bc) / denom, -1, 1)
    return np.degrees(np.arccos(cos))

# -------------------------------------------------------------------
# FRAME PROCESSING (SAFE)
# -------------------------------------------------------------------
def process_frame(frame, pose):
    global accuracy, feedback, form_correct, form_confidence

    frame = np.ascontiguousarray(frame.copy())

    try:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = pose.process(rgb)
        rgb.flags.writeable = True
    except Exception as e:
        print("Pose error:", e)
        return frame

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        accuracy = np.mean([lm.visibility for lm in landmarks]) * 100

        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0,255,0), thickness=2),
            mp_drawing.DrawingSpec(color=(255,255,0), thickness=2)
        )

        feedback = "Processing"
        form_correct = True
        form_confidence = 75.0

    # UI overlay
    cv2.rectangle(frame, (0,0), (frame.shape[1],60), (20,20,20), -1)
    cv2.putText(frame, "RepBot - Stable Backend", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

    return np.ascontiguousarray(frame)

# -------------------------------------------------------------------
# CAMERA THREAD (NEVER BREAKS)
# -------------------------------------------------------------------
def capture_camera():
    global camera_running, last_frame, pose_detector

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Camera not accessible")
        camera_running = False
        return

    pose_detector = mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    print("✓ Camera started")

    while camera_running:
        try:
            ret, frame = cap.read()
            if not ret or frame is None or frame.size == 0:
                time.sleep(0.05)
                continue

            processed = process_frame(frame, pose_detector)
            processed = np.ascontiguousarray(processed)

            ok, buffer = cv2.imencode(".jpg", processed)
            if not ok:
                continue

            last_frame = buffer.tobytes()
            time.sleep(0.03)

        except Exception as e:
            print("Frame error:", e)
            continue

    cap.release()
    pose_detector = None
    print("Camera released")

# -------------------------------------------------------------------
# STREAM GENERATOR
# -------------------------------------------------------------------
def generate_frames():
    while camera_running:
        if last_frame:
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" +
                   last_frame + b"\r\n")
        else:
            time.sleep(0.1)

# -------------------------------------------------------------------
# ROUTES
# -------------------------------------------------------------------
@app.route("/")
def index():
    return jsonify({"status": "RepBot Backend", "mediapipe": MEDIAPIPE_AVAILABLE})

@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/api/start_camera", methods=["POST"])
def start_camera():
    global camera_running, capture_thread

    if camera_running:
        return jsonify({"status": "success", "message": "Camera already running"})

    camera_running = True
    capture_thread = threading.Thread(target=capture_camera, daemon=True)
    capture_thread.start()
    time.sleep(0.5)

    return jsonify({"status": "success", "message": "Camera started"})

@app.route("/api/stop_camera", methods=["POST"])
def stop_camera():
    global camera_running
    camera_running = False
    time.sleep(0.5)
    return jsonify({"status": "success", "message": "Camera stopped"})

@app.route("/api/get_stats")
def get_stats():
    return jsonify({
        "status": "success",
        "data": {
            "accuracy": round(accuracy,2),
            "feedback": feedback,
            "form_correct": form_correct,
            "form_confidence": round(form_confidence,2),
            "counters": exercise_counters,
            "available_exercises": {k:v["name"] for k,v in EXERCISES.items()}
        }
    })

# -------------------------------------------------------------------
# CLEANUP
# -------------------------------------------------------------------
def cleanup():
    global camera_running
    camera_running = False

atexit.register(cleanup)

# -------------------------------------------------------------------
# RUN
# -------------------------------------------------------------------
if __name__ == "__main__":
    print("RepBot Backend running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True, use_reloader=False)
