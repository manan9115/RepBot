# RepBot Backend API

This is the Flask backend API that integrates the RepBot project for real-time exercise tracking using MediaPipe and OpenCV.

## Features

- Real-time pose detection using MediaPipe
- Exercise rep counting (Bicep Curls, Squats, Lateral Raises)
- Form validation using ML models (local model + enhanced validation)
- Video streaming to frontend
- RESTful API endpoints for stats and control

## Prerequisites

- Python 3.8 or higher
- Webcam/Camera connected to your computer
- RTX 2050 GPU (optional, for enhanced performance)

## Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Backend

Start the Flask server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### GET `/`
Health check endpoint. Returns API status.

### GET `/video_feed`
Video streaming endpoint. Returns MJPEG stream of processed video with pose detection.

### POST `/api/start_camera`
Starts the camera and begins processing frames.

### POST `/api/stop_camera`
Stops the camera and releases resources.

### POST `/api/reset_counters`
Resets all exercise counters to zero.

### GET `/api/get_stats`
Returns current exercise statistics:
```json
{
  "status": "success",
  "data": {
    "bicep_count": 0,
    "squat_count": 0,
    "lateral_count": 0,
    "current_exercise": "None",
    "accuracy": 85.5,
    "feedback": "Correct Form",
    "form_correct": true,
    "form_confidence": 92.3
  }
}
```

### POST `/api/set_exercise`
Sets the current exercise type.
Request body:
```json
{
  "exercise": "bicep"  // Options: "bicep", "squat", "lateral", "none"
}
```

## Exercise Detection

The system automatically detects exercises based on movement patterns:
- **Bicep Curl**: Detected when arm angle goes from >160° to <30°
- **Squat**: Detected when leg angle goes from >160° to <90°
- **Lateral Raise**: Detected when arm angle goes from >80° to <40°

## Form Validation

Form validation uses:
1. Angle-based rules for each exercise type
2. Local ML model (if `exercise_form_model.pkl` exists)
3. Confidence scoring for form correctness

## Troubleshooting

### Camera not working
- Ensure your camera is connected and not being used by another application
- Check camera permissions in your OS settings
- Try changing the camera index in `app.py` (currently set to 0)

### Model files not found
- The system will work without model files using angle-based validation
- To use ML model, ensure `exercise_form_model.pkl` and `scaler.pkl` are in the backend directory

### Performance issues
- Reduce frame processing rate by increasing sleep time in `capture_camera()`
- Lower MediaPipe model complexity in pose initialization
- Use GPU acceleration if available (requires CUDA setup)

## Notes

- The backend runs on port 5000 by default
- CORS is enabled for all origins (adjust in production)
- Video streaming uses MJPEG format for compatibility


