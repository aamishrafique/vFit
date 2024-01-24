import os
from flask import Flask, render_template, redirect, url_for, send_file, request
import qrcode

app = Flask(__name__, static_url_path="/static")

i = 1


# Function to Generate the QR Code
def generate_qr_code(data):
    global i
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
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


@app.route("/download/<int:filename>")
def download(filename):
    path = f"static/result/{filename}.png"
    download_name = f"result_{filename}.png"
    return send_file(path, as_attachment=True, download_name=download_name)


@app.route("/qr_code")
def qr_code():
    global i
    image_filename = f"{i}.png"
    ngrok_url = "https://4d5d-182-191-88-42.ngrok-free.app"
    data = f"{ngrok_url}/static/result/{image_filename}"
    # data = f"{request.url_root}static/result/{image_filename}"
    img = generate_qr_code(data)
    i += 1
    return render_template("qr_code.html", i=str(i - 1))


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
