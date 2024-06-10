import os
from flask import Flask, render_template, redirect, url_for, send_file, request, jsonify
from PIL import Image, ImageEnhance
import qrcode
import cv2
import numpy as np
import math
import mediapipe as mp
import requests
import json


# Initialize the Webcam and MediaPipe Hands
# cap = cv2.VideoCapture(0)
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands()
# thumbs_up_threshold = 0.05
# swipe_threshold = 0.05

app = Flask(__name__, static_url_path="/static")
ngrok_url = "https://9a30-58-65-153-188.ngrok-free.app/"
live_url = "http://192.168.55.32:5000/"

cloth_idx_on_top = 1


# def process_frame(frame):
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = hands.process(rgb_frame)

#     thumbs_up_detected = False
#     swipe_direction = "No Swipe"
#     open_palm_detected = False

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             # Thumbs-Up Detection
#             thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
#             index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
#             distance_thumb_index = math.sqrt(
#                 (thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2
#             )

#             if index_tip.y > thumb_tip.y and distance_thumb_index > thumbs_up_threshold:
#                 thumbs_up_detected = True

#             # Swipe Detection
#             distance = abs(index_tip.x - thumb_tip.x)

#             # Open Palm Detection
#             finger_tips = [
#                 hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
#                 hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
#                 hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
#                 hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
#                 hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP],
#             ]
#             # Calculate the Average Distance Between Each Fingertip
#             avg_distance = 0
#             count = 0
#             for i in range(len(finger_tips)):
#                 for j in range(i + 1, len(finger_tips)):
#                     avg_distance += math.sqrt(
#                         (finger_tips[i].x - finger_tips[j].x) ** 2
#                         + (finger_tips[i].y - finger_tips[j].y) ** 2
#                     )
#                     count += 1
#             if count > 0:
#                 avg_distance /= count

#             # Define a Threshold for Open Palm Detection
#             open_palm_threshold = 0.1

#             if avg_distance > open_palm_threshold:
#                 open_palm_detected = True

#             if distance > swipe_threshold:
#                 if index_tip.x < thumb_tip.x:
#                     swipe_direction = "Swipe Right"
#                 elif index_tip.x > thumb_tip.x:
#                     swipe_direction = "Swipe Left"

#     return {
#         "thumbs_up": "Thumbs up" if thumbs_up_detected else "None",
#         "swipe": swipe_direction,
#         "open_palm": "Open Palm" if open_palm_detected else "None",
#     }


# @app.route("/get_gesture")
# def get_gesture():
#     global cloth_idx_on_top
#     ret, frame = cap.read()
#     if not ret:
#         return jsonify({"gesture": "Error"})

#     gesture_result = process_frame(frame)
#     if gesture_result["swipe"] == "Swipe Right":
#         cloth_idx_on_top += 1
#         if cloth_idx_on_top == 11:
#             cloth_idx_on_top = 1
#     else:
#         cloth_idx_on_top -= 1
#         if cloth_idx_on_top == 0:
#             cloth_idx_on_top = 10

#     print('Running Function: "get_gesture"')

#     return jsonify(gesture_result)


def merge_images(
    background_path, overlay_path, output_path, scale_factor=1.2, y_offset_shift=-50
):
    background = cv2.imread(background_path)
    overlay = cv2.imread(overlay_path)
    overlay = cv2.resize(overlay, (0, 0), fx=scale_factor, fy=scale_factor)
    overlay_height, overlay_width, _ = overlay.shape
    x_offset = (background.shape[1] - overlay_width) // 2
    y_offset = (background.shape[0] - overlay_height) // 2 + y_offset_shift
    background[
        y_offset : y_offset + overlay_height, x_offset : x_offset + overlay_width
    ] = overlay
    cv2.imwrite(output_path, background)


i = 1
background = cv2.imread(
    os.path.join(os.path.dirname(__file__), "static", "images", "template.png")
)
os.makedirs(os.path.join(os.path.dirname(__file__), "static", "result"), exist_ok=True)
os.makedirs(
    os.path.join(os.path.dirname(__file__), "static", "template"), exist_ok=True
)
os.makedirs(os.path.join(os.path.dirname(__file__), "static", "qr_code"), exist_ok=True)


# Function to Generate the QR Code
def generate_qr_code(filename):
    global ngrok_url
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = f"{ngrok_url}/images/{filename}"
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    static_dir = os.path.join(os.path.dirname(__file__), "static", "qr_code")
    img.save(os.path.join(static_dir, f"{i}.png"))
    return img


@app.route("/")
def robot():
    return render_template("robot.html")


@app.route("/qr_code")
def qr_code():
    global i
    global ngrok_url
    image_filename = f"{i}.jpg"

    scale_factor = 1.9
    y_offset_shift = -100
    global background
    overlay = cv2.imread(
        os.path.join(os.path.dirname(__file__), "static", "result", image_filename)
    )
    overlay = cv2.resize(overlay, (0, 0), fx=scale_factor, fy=scale_factor)
    overlay_height, overlay_width, _ = overlay.shape
    x_offset = (background.shape[1] - overlay_width) // 2
    y_offset = (background.shape[0] - overlay_height) // 2 + y_offset_shift
    background[
        y_offset : y_offset + overlay_height, x_offset : x_offset + overlay_width
    ] = overlay
    cv2.imwrite(
        os.path.join(os.path.dirname(__file__), "static", "template", image_filename),
        background,
    )

    img = generate_qr_code(image_filename)
    # NOTE: Uncomment the Below Line
    i += 1
    return render_template("qr_code.html", i=str(i - 1))


@app.route("/images/<filename>")
def images(filename):
    return render_template("images.html", filename=filename)


@app.route("/home")
def home():
    global cloth_idx_on_top
    return render_template("home.html", cloth_idx_on_top=cloth_idx_on_top)


def get_vFit(cloth_file):
    global live_url
    image_filename = f"{i}.jpg"
    path_to_save = os.path.join(
        os.path.dirname(__file__), "static", "result", image_filename
    )
    response = requests.get(live_url + "/snap")
    with open(path_to_save, "wb") as file:
        file.write(response.content)

    print('Running Route: "get_vFit"')
    print(f"Image Name: {image_filename}")
    vFit_url = "https://f88b-2407-d000-a-223c-5555-7179-37b2-1b48.ngrok-free.app/"
    r = requests.post(vFit_url, files={"imageUpload": open(path_to_save, "rb")})
    fit = requests.get(vFit_url + f"try_api?cloth={cloth_file}")

    with open(path_to_save, "wb") as file:
        file.write(fit.content)


@app.route("/get_current_index", methods=["POST"])
def get_current_index():
    print('Running Route "get_current_index"')
    global cloth_idx_on_top
    data = request.get_json()
    currentIndex = data.get("currentIndex", None)
    cloth_idx_on_top = currentIndex
    response = {"message": "success"}
    return jsonify(response)


@app.route("/trigger/<key>")
def trigger(key):
    global cloth_idx_on_top
    if key == "n":
        return redirect(url_for("home"))
    elif key == "p":
        dict_map = {
            1: "00000_00.jpg",
            2: "00001_00.jpg",
            3: "00003_00.jpg",
            4: "00005_00.jpg",
            5: "00007_00.jpg",
            6: "00009_00.jpg",
            7: "00010_00.jpg",
            8: "00015_00.jpg",
            9: "00019_00.jpg",
            10: "00029_00.jpg",
            11: "00030_00.jpg",
        }
        print(f"Current Cloth Index: {cloth_idx_on_top}")
        get_vFit(dict_map[cloth_idx_on_top])
        return redirect(url_for("qr_code"))
    else:
        return redirect(url_for("robot"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
