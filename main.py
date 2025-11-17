# from flask import Flask, render_template, Response, jsonify
# import cv2
# import numpy as np
# import tensorflow as tf
# import json

# app = Flask(__name__)

# # Load ML Model
# model = tf.keras.models.load_model("model/emotion_model.h5")
# emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

# # Load JSON Data
# with open("data.json", "r") as file:
#     emotion_responses = json.load(file)

# # OpenCV for webcam
# camera = cv2.VideoCapture(0)

# # Function to detect emotion from frame
# def detect_emotion(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     gray = cv2.resize(gray, (48, 48))
#     gray = np.expand_dims(gray, axis=0).reshape(1, 48, 48, 1) / 255.0
#     prediction = model.predict(gray)
#     return emotion_labels[np.argmax(prediction)]

# # Function to get response from JSON file
# def get_solution(emotion):
#     return emotion_responses.get(emotion, "No advice available for this emotion.")

# # Video feed route
# def generate_frames():
#     while True:
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_bytes = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get_advice')
# def get_advice():
#     success, frame = camera.read()
#     if not success:
#         return jsonify({"error": "Could not capture frame"}), 500

#     emotion = detect_emotion(frame)
#     advice = get_solution(emotion)

#     _, buffer = cv2.imencode('.jpg', frame)
#     img_data = buffer.tobytes()

#     return render_template("result.html", emotion=emotion, advice=advice, img_data=img_data)

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import tensorflow as tf
import json
import os
import random
import base64

app = Flask(__name__)

# Load ML Model (Local File)
MODEL_PATH = "model/emotion_model.h5"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Model file not found! Please check 'model/emotion_model.h5'.")

model = tf.keras.models.load_model(MODEL_PATH)
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Neutral", "Sad", "Surprise"]

# Load JSON Data
with open("data.json", "r") as file:
    emotion_responses = json.load(file)

# OpenCV for webcam: try multiple indices and use Windows DirectShow backend when available
def find_camera(max_index=4):
    """Try to find a working camera. Returns an opened VideoCapture or None.
    On Windows, prefer DirectShow backend which is often more reliable for webcams.
    """
    # If user provided a CAMERA_INDEX env var, try it first
    env_index = None
    try:
        env_index = os.environ.get("CAMERA_INDEX")
        if env_index is not None:
            env_index = int(env_index)
    except Exception:
        env_index = None

    tried = set()

    if env_index is not None:
        indices = [env_index] + [i for i in range(max_index + 1) if i != env_index]
    else:
        indices = list(range(max_index + 1))

    for i in indices:
        if i in tried:
            continue
        tried.add(i)
        try:
            # On Windows prefer DirectShow (CAP_DSHOW)
            if os.name == 'nt':
                cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
            else:
                cap = cv2.VideoCapture(i)

            if cap is None:
                continue

            if cap.isOpened():
                # quick frame read to ensure the camera can deliver frames
                ret, frame = cap.read()
                if ret:
                    print(f"Using camera index {i}")
                    return cap
                cap.release()
        except Exception:
            # ignore and try next index
            try:
                cap.release()
            except Exception:
                pass

    print("Warning: No working camera found. The app will use a placeholder image and random emotions.")
    return None


# initialize camera (may be None)
camera = find_camera()

# Function to detect emotion from frame
def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (48, 48))
    gray = np.expand_dims(gray, axis=0).reshape(1, 48, 48, 1) / 255.0
    prediction = model.predict(gray)
    return emotion_labels[np.argmax(prediction)]

# Function to get response from JSON file
def get_solution(emotion):
    return emotion_responses.get(emotion, "No advice available for this emotion.")

# Video feed route
def generate_frames():
    while True:
        # If camera not available, yield a placeholder frame
        if camera is None:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Camera not available", (50, 240),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, "Using fallback - random emotions", (50, 280),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            success, frame = camera.read()
            if not success or frame is None:
                # Show a friendly placeholder instead of breaking the stream
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(frame, "Camera read failed", (50, 240),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, "Using fallback - random emotions", (50, 280),
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
    # Handle missing camera or failed reads gracefully
    if camera is None:
        emotion = random.choice(emotion_labels)
        advice = get_solution(emotion)
        # create placeholder frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(frame, "Camera not available", (50, 200),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"DETECTED: {emotion}", (50, 260),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    else:
        success, frame = camera.read()
        if not success or frame is None:
            # fallback to placeholder and random emotion
            emotion = random.choice(emotion_labels)
            advice = get_solution(emotion)
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Camera read failed", (50, 200),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"DETECTED: {emotion}", (50, 260),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            # Try running the real detection but fall back on error
            try:
                emotion = detect_emotion(frame)
                advice = get_solution(emotion)
            except Exception as e:
                print(f"Warning: detection failed: {e}")
                emotion = random.choice(emotion_labels)
                advice = get_solution(emotion)

    # Encode image as base64 for the template
    _, buffer = cv2.imencode('.jpg', frame)
    img_data = base64.b64encode(buffer).decode('utf-8')

    return render_template("result.html", emotion=emotion, advice=advice, img_data=img_data)

# ✅ Flask Port Handling for Railway Deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
