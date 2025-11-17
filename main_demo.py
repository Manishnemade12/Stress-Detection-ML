from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import json
import os
import random
import base64

app = Flask(__name__)

# Demo emotion labels (same as original)
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

# Load JSON Data
with open("data.json", "r") as file:
    emotion_responses = json.load(file)

# Global camera variable
camera = None

def get_camera():
    """Get camera instance with error handling"""
    global camera
    if camera is None or not camera.isOpened():
        try:
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                # Try different camera indices
                for i in range(1, 5):
                    camera = cv2.VideoCapture(i)
                    if camera.isOpened():
                        print(f"Camera found at index {i}")
                        break
                else:
                    print("No camera found")
                    return None
        except Exception as e:
            print(f"Camera error: {e}")
            return None
    return camera

# Demo function to simulate emotion detection
def detect_emotion_demo(frame):
    # For demo purposes, return a random emotion
    return random.choice(emotion_labels)

# Function to get response from JSON file
def get_solution(emotion):
    return emotion_responses.get(emotion, "No advice available for this emotion.")

# Video feed route
def generate_frames():
    while True:
        cam = get_camera()
        if cam is None:
            # Create a placeholder frame when camera is not available
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Camera not available", (200, 240), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, "DEMO MODE - Random Emotion Detection", (150, 280), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            success, frame = cam.read()
            if not success:
                # Create a placeholder frame when camera read fails
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, "Camera read failed", (200, 240), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, "DEMO MODE - Random Emotion Detection", (150, 280), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                # Add text overlay to show it's a demo
                cv2.putText(frame, "DEMO MODE - Random Emotion Detection", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_advice')
def get_advice():
    cam = get_camera()
    
    if cam is None:
        # Create a demo result without camera
        emotion = random.choice(emotion_labels)
        advice = get_solution(emotion)
        
        # Create a placeholder image
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, "Camera not available", (200, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"DEMO: {emotion}", (250, 250), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "Random emotion generated", (150, 300), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    else:
        success, frame = cam.read()
        if not success:
            # Create a demo result with camera read failure
            emotion = random.choice(emotion_labels)
            advice = get_solution(emotion)
            
            # Create a placeholder image
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Camera read failed", (200, 200), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"DEMO: {emotion}", (250, 250), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, "Random emotion generated", (150, 300), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        else:
            # Use demo emotion detection with real camera
            emotion = detect_emotion_demo(frame)
            advice = get_solution(emotion)

            # Add demo text to frame
            cv2.putText(frame, f"DEMO: {emotion}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Encode image as base64 for HTML display
    _, buffer = cv2.imencode('.jpg', frame)
    img_data = base64.b64encode(buffer).decode('utf-8')

    return render_template("result.html", emotion=emotion, advice=advice, img_data=img_data)

# Flask Port Handling
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting demo application on port {port}")
    print("Note: This is a demo version with random emotion detection")
    print("For full functionality, install TensorFlow and use main.py")
    app.run(host="0.0.0.0", port=port, debug=True)
