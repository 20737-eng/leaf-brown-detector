from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "ไม่พบไฟล์ภาพ"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "ชื่อไฟล์ว่าง"}), 400

    # อ่านไฟล์จาก memory (ไม่ save ลง disk)
    file_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img is None:
        return jsonify({"error": "ไม่สามารถอ่านไฟล์ภาพได้"}), 400

    # แปลงเป็น HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # ช่วงสีน้ำตาล (ปรับได้)
    lower_brown = np.array([10, 50, 50])
    upper_brown = np.array([30, 255, 200])

    mask = cv2.inRange(hsv, lower_brown, upper_brown)

    brown_pixels = cv2.countNonZero(mask)
    total_pixels = img.shape[0] * img.shape[1]

    percent = round((brown_pixels / total_pixels) * 100, 2)

    return jsonify({
        "brown_percent": percent
    })

if __name__ == "__main__":
    app.run()
