from flask import Flask, render_template, request, jsonify
import os
import pose_detection  # Ensure your pose_detection module is imported

app = Flask(__name__)

# Ensure this directory is created for saving uploaded videos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video_file = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, 'uploaded_video.mp4')
    video_file.save(video_path)

    reps_count = pose_detection.detect_movement(video_path)  # Call your detection function
    
    return jsonify({'reps_count': reps_count})

if __name__ == '__main__':
    app.run(debug=True)
