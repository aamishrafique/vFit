from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, static_url_path="/static")


@app.route("/")
def robot():
    return render_template("robot.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/trigger/<key>")
def trigger(key):
    if key == "n":
        return redirect(url_for("home"))
    else:
        return redirect(url_for("robot"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
