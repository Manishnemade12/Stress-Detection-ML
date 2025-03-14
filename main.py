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

# OpenCV for webcam
camera = cv2.VideoCapture(0)

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
        success, frame = camera.read()
        if not success:
            break
        else:
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
    success, frame = camera.read()
    if not success:
        return jsonify({"error": "Could not capture frame"}), 500

    emotion = detect_emotion(frame)
    advice = get_solution(emotion)

    _, buffer = cv2.imencode('.jpg', frame)
    img_data = buffer.tobytes()

    return render_template("result.html", emotion=emotion, advice=advice, img_data=img_data)

# ✅ Flask Port Handling for Railway Deployment
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
