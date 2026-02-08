from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "ไม่พบไฟล์ภาพ"})

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "ชื่อไฟล์ว่าง"})

    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    img = cv2.imread(filepath)
    if img is None:
        return jsonify({"error": "ไม่สามารถอ่านไฟล์ภาพได้"})

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_brown = np.array([10, 50, 50])
    upper_brown = np.array([30, 255, 200])

    mask = cv2.inRange(hsv, lower_brown, upper_brown)

    brown_pixels = cv2.countNonZero(mask)
    total_pixels = img.shape[0] * img.shape[1]
    percent = round((brown_pixels / total_pixels) * 100, 2)

    return jsonify({"brown_percent": percent})

# ❗ สำคัญ: ห้ามใส่ port ตายตัว
if __name__ == "__main__":
    app.run()
