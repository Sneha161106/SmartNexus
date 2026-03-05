from flask import Flask, render_template, request, jsonify, Response
import os
import cv2
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Global source for camera/video
video_source = 0


# ------------------------------
# Dashboard
# ------------------------------
@app.route("/")
def home():
    return render_template("dashboard.html")


# ------------------------------
# Upload Video
# ------------------------------
@app.route("/upload", methods=["POST"])
def upload_video():

    global video_source

    if "video" not in request.files:
        return "No file uploaded"

    file = request.files["video"]

    if file.filename == "":
        return "No selected file"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)

    file.save(filepath)

    video_source = filepath

    return render_template("dashboard.html")


# ------------------------------
# Start Webcam
# ------------------------------
@app.route("/camera")
def camera():

    global video_source

    video_source = 0

    return render_template("dashboard.html")


# ------------------------------
# Video Streaming
# ------------------------------
def generate_frames():

    cap = cv2.VideoCapture(video_source)

    while True:

        success, frame = cap.read()

        if not success:
            break

        ret, buffer = cv2.imencode('.jpg', frame)

        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# ------------------------------
# Incident API (for dashboard)
# ------------------------------
@app.route("/incidents")
def incidents():

    try:
        df = pd.read_csv("incident_log.csv")
        return jsonify(df.to_dict(orient="records"))

    except:
        return jsonify([])


# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)