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
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
thumbs_up_threshold = 0.05
swipe_threshold = 0.05

app = Flask(__name__, static_url_path="/static")
ngrok_url = "https://7721-139-135-32-235.ngrok-free.app"


def process_frame(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    thumbs_up_detected = False
    swipe_direction = "No Swipe"
    open_palm_detected = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Thumbs-up detection
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            distance_thumb_index = math.sqrt(
                (thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2
            )

            if index_tip.y > thumb_tip.y and distance_thumb_index > thumbs_up_threshold:
                thumbs_up_detected = True

            # Swipe detection (assuming only one hand is in the frame)
            distance = abs(index_tip.x - thumb_tip.x)

            # Open palm detection
            finger_tips = [
                hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP],
            ]
            # Calculate the average distance between each fingertip
            avg_distance = 0
            count = 0
            for i in range(len(finger_tips)):
                for j in range(i + 1, len(finger_tips)):
                    avg_distance += math.sqrt(
                        (finger_tips[i].x - finger_tips[j].x) ** 2
                        + (finger_tips[i].y - finger_tips[j].y) ** 2
                    )
                    count += 1
            if count > 0:
                avg_distance /= count

            # Define a threshold for open palm detection
            open_palm_threshold = 0.1  # Adjust as needed based on your observations

            if avg_distance > open_palm_threshold:
                open_palm_detected = True

            if distance > swipe_threshold:
                if index_tip.x < thumb_tip.x:
                    swipe_direction = "Swipe Right"
                elif index_tip.x > thumb_tip.x:
                    swipe_direction = "Swipe Left"

    return {
        "thumbs_up": "Thumbs up" if thumbs_up_detected else "None",
        "swipe": swipe_direction,
        "open_palm": "Open Palm" if open_palm_detected else "None",
    }


@app.route("/get_gesture")
def get_gesture():
    ret, frame = cap.read()
    if not ret:
        return jsonify({"gesture": "Error"})

    gesture_result = process_frame(frame)
    return jsonify(gesture_result)


def upscale(image_filename):
    global ngrok_url

    # The URL of the API endpoint
    url = "https://api.claid.ai/v1-beta1/image/edit"

    # The header should contain your authorization token and content type
    headers = {
        "Authorization": "Bearer e4f0525e211d4e4aa74a4534160d3f21",
        "Content-Type": "application/json",
    }

    # The payload as a dictionary
    payload = {
        "input": f"{ngrok_url}/static/result/{image_filename}",
        "operations": {
            "resizing": {"width": 800, "height": 800, "fit": "crop"},
            "adjustments": {"hdr": 60, "sharpness": 40},
        },
        "output": {"format": {"type": "jpeg", "quality": 90}},
    }

    # Making the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code == 200:
        print("Image has been successfully edited.")
        # Assuming the API returns a URL to the edited image or similar
        edited_image_url = response.json().get("tmp_url")
        print("Edited image URL:", edited_image_url)
    else:
        print("Failed to edit image. Status code:", response.status_code)
        print("Response:", response.text)

    upscale_url = response.json()["data"]["output"]["tmp_url"]

    return upscale_url


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
    os.makedirs(static_dir, exist_ok=True)
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

    scale_factor = 1.2
    y_offset_shift = -50
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
    upscale_url = upscale(image_filename)

    r = requests.get(upscale_url)
    f = open("hello.jpeg", "wb")
    f.write(r.content)

    img = generate_qr_code(image_filename)
    # NOTE: Uncomment the Below Line
    # i += 1
    return render_template("qr_code.html", i=str(i))


@app.route("/images/<filename>")
def images(filename):
    return render_template("images.html", filename=filename)


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/trigger/<key>")
def trigger(key):
    if key == "n":
        return redirect(url_for("home"))
    elif key == "p":
        return redirect(url_for("qr_code"))
    else:
        return redirect(url_for("robot"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
