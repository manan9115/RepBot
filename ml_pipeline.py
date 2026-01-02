"""
ML Pipeline for Exercise Analysis
Uses MediaPipe for pose extraction and Hugging Face models for exercise analysis
"""
import numpy as np
from collections import deque
import json

# Try to import torch (optional)
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None
    print("⚠ PyTorch not available (optional)")

# Try to import Hugging Face transformers
try:
    from transformers import AutoModel, AutoTokenizer, AutoFeatureExtractor
    from transformers import pipeline
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("⚠ Hugging Face transformers not available (optional)")

class ExerciseMLPipeline:
    """ML Pipeline for exercise form analysis and rep counting"""
    
    def __init__(self):
        self.device = "cuda" if TORCH_AVAILABLE and torch is not None and torch.cuda.is_available() and HF_AVAILABLE else "cpu"
        self.pose_history = deque(maxlen=30)  # Store last 30 frames
        self.rep_counters = {}
        self.exercise_states = {}
        
        # Initialize Hugging Face model for exercise analysis
        if HF_AVAILABLE and TORCH_AVAILABLE:
            try:
                # Use a lightweight transformer for sequence classification
                # We'll use pose features as input
                self.model_name = "microsoft/swin-tiny-patch4-window7-224"
                self.feature_extractor = None
                # For now, we'll use rule-based + local model, but structure is ready for HF
                self.hf_model_ready = False
                print("✓ ML Pipeline initialized (HF transformers available)")
            except Exception as e:
                print(f"⚠ HF model initialization failed: {e}")
                self.hf_model_ready = False
        else:
            self.hf_model_ready = False
            if not TORCH_AVAILABLE:
                print("✓ ML Pipeline initialized (using local models - PyTorch not required)")
            else:
                print("✓ ML Pipeline initialized (HF transformers not available, using local models)")
    
    def extract_pose_features(self, landmarks):
        """Extract normalized pose features from MediaPipe landmarks"""
        if landmarks is None:
            return None
        
        try:
            features = []
            
            # Extract key joint positions (normalized 0-1)
            key_joints = [
                'LEFT_SHOULDER', 'RIGHT_SHOULDER',
                'LEFT_ELBOW', 'RIGHT_ELBOW',
                'LEFT_WRIST', 'RIGHT_WRIST',
                'LEFT_HIP', 'RIGHT_HIP',
                'LEFT_KNEE', 'RIGHT_KNEE',
                'LEFT_ANKLE', 'RIGHT_ANKLE',
                'NOSE'
            ]
            
            import mediapipe as mp
            mp_pose = mp.solutions.pose
            
            for joint_name in key_joints:
                try:
                    landmark = landmarks[mp_pose.PoseLandmark[joint_name].value]
                    features.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
                except:
                    features.extend([0.0, 0.0, 0.0, 0.0])
            
            # Calculate key angles
            angles = self._calculate_key_angles(landmarks)
            features.extend(angles)
            
            return np.array(features, dtype=np.float32)
        except Exception as e:
            print(f"Error extracting pose features: {e}")
            return None
    
    def _calculate_key_angles(self, landmarks):
        """Calculate key joint angles for exercise analysis"""
        import mediapipe as mp
        mp_pose = mp.solutions.pose
        
        angles = []
        
        try:
            # Helper function to calculate angle
            def angle_between_points(a, b, c):
                a = np.array([a.x, a.y])
                b = np.array([b.x, b.y])
                c = np.array([c.x, c.y])
                ba = a - b
                bc = c - b
                cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
                cosine = np.clip(cosine, -1.0, 1.0)
                return np.degrees(np.arccos(cosine))
            
            # Left arm angle (bicep)
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
            angles.append(angle_between_points(left_shoulder, left_elbow, left_wrist))
            
            # Right arm angle
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]
            angles.append(angle_between_points(right_shoulder, right_elbow, right_wrist))
            
            # Left leg angle (squat)
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
            left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            angles.append(angle_between_points(left_hip, left_knee, left_ankle))
            
            # Right leg angle
            right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
            right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
            right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
            angles.append(angle_between_points(right_hip, right_knee, right_ankle))
            
            # Torso angle
            nose = landmarks[mp_pose.PoseLandmark.NOSE.value]
            angles.append(angle_between_points(nose, left_shoulder, left_hip))
            
        except Exception as e:
            angles = [0.0] * 5
        
        return angles
    
    def analyze_exercise_form(self, pose_features, exercise_type, local_model=None, scaler=None):
        """Analyze exercise form using ML models"""
        if pose_features is None:
            return {
                'form_correct': False,
                'confidence': 0.0,
                'feedback': 'No pose detected',
                'score': 0.0
            }
        
        # Use local model if available
        if local_model is not None and scaler is not None:
            try:
                # Extract angle features for local model
                angle_features = pose_features[-5:] if len(pose_features) >= 5 else pose_features
                if len(angle_features) < 2:
                    angle_features = np.array([0.0, 0.0])
                
                # Scale and predict
                scaled = scaler.transform([angle_features[:2]])  # bicep and squat angles
                prediction = local_model.predict(scaled)[0]
                proba = local_model.predict_proba(scaled)[0]
                
                form_correct = prediction == 1
                confidence = float(proba[1] if form_correct else proba[0]) * 100
                
                feedback = self._generate_feedback(exercise_type, pose_features, form_correct)
                
                return {
                    'form_correct': form_correct,
                    'confidence': confidence,
                    'feedback': feedback,
                    'score': confidence / 100.0
                }
            except Exception as e:
                print(f"Local model prediction error: {e}")
        
        # Fallback to rule-based analysis
        return self._rule_based_analysis(pose_features, exercise_type)
    
    def _rule_based_analysis(self, pose_features, exercise_type):
        """Rule-based form analysis as fallback"""
        if len(pose_features) < 5:
            return {
                'form_correct': False,
                'confidence': 0.0,
                'feedback': 'Insufficient pose data',
                'score': 0.0
            }
        
        # Extract angles (last 5 values)
        angles = pose_features[-5:] if len(pose_features) >= 5 else [0.0] * 5
        bicep_angle = angles[0] if len(angles) > 0 else 0
        squat_angle = angles[2] if len(angles) > 2 else 0
        
        form_correct = True
        feedback = "Correct Form"
        confidence = 85.0
        
        if exercise_type == "BICEP_CURL":
            if not (30 < bicep_angle < 160):
                form_correct = False
                feedback = "Keep elbow stable, maintain proper range of motion"
                confidence = 40.0
        elif exercise_type == "SQUAT":
            if not (90 < squat_angle < 160):
                form_correct = False
                feedback = "Go deeper, thighs should be parallel to ground"
                confidence = 45.0
        
        return {
            'form_correct': form_correct,
            'confidence': confidence,
            'feedback': feedback,
            'score': confidence / 100.0
        }
    
    def _generate_feedback(self, exercise_type, pose_features, form_correct):
        """Generate specific feedback based on exercise type and form"""
        if form_correct:
            return "Correct Form - Keep it up!"
        
        if len(pose_features) < 5:
            return "Adjust your position for better detection"
        
        angles = pose_features[-5:] if len(pose_features) >= 5 else [0.0] * 5
        bicep_angle = angles[0] if len(angles) > 0 else 0
        squat_angle = angles[2] if len(angles) > 2 else 0
        
        feedback_tips = {
            "BICEP_CURL": [
                "Keep your elbow close to your body",
                "Control the weight, don't swing",
                "Full range of motion - extend and contract fully"
            ],
            "SQUAT": [
                "Keep your back straight",
                "Go deeper - thighs parallel to ground",
                "Push through your heels when standing"
            ],
            "PUSH_UP": [
                "Keep your body in a straight line",
                "Lower your chest to the ground",
                "Push up with control"
            ]
        }
        
        if exercise_type in feedback_tips:
            import random
            return random.choice(feedback_tips[exercise_type])
        
        return "Focus on proper form and control"




