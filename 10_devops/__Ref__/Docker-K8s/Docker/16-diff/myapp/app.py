print("Docker - Bài 16 — Diff - Xem thay đổi filesystem")
print("------------------------------------------------------------")
print("")
from flask import Flask
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    return f"Hello from MyApp v2.0 - {datetime.now()}"


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
