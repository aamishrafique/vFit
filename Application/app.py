import os
from flask import Flask, render_template, redirect, url_for, send_file, request
from PIL import Image, ImageEnhance
import qrcode
import cv2
import numpy as np

app = Flask(__name__, static_url_path="/static")
ngrok_url = "https://7721-139-135-32-235.ngrok-free.app"


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
# def generate_qr_code(filename):
#     global ngrok_url
#     data = f"{ngrok_url}/images/{filename}"
#     static_dir = os.path.join(os.path.dirname(__file__), "static", "qr_code")
#     os.makedirs(static_dir, exist_ok=True)
#     img.save(os.path.join(static_dir, f"{i}.png"))
#     return img


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


# @app.route("/download/<int:filename>")
# def download(filename):
#     path = f"static/template/{filename}.png"
#     download_name = f"result_{filename}.png"
#     return send_file(path, as_attachment=True, download_name=download_name)


@app.route("/download/<int:filename>")
def download(filename):
    path = f"static/template/{filename}.png"
    download_name = f"result_{filename}.png"
    return send_file(path, as_attachment=True, download_name=download_name)


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

    img = generate_qr_code(image_filename)
    # NOTE: Uncomment the Below Line
    # i += 1
    return render_template("qr_code.html", i=str(i))


@app.route("/images/<filename>")
def images(filename):
    print(f"\n\n\n\n", filename)
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
