print("Docker - Bài 19 — Volume - Lưu trữ dữ liệu bền vững")
print("------------------------------------------------------------")
print("")
import logging
import os
from datetime import datetime

from flask import Flask

LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "MyApp")
APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "4.0")


@app.route("/")
def home():
    logging.info("Home page accessed")
    return f"Hello from {APP_NAME} [{APP_ENV}] v{APP_VERSION} - {datetime.now()}"


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/config")
def config():
    return {"name": APP_NAME, "env": APP_ENV, "version": APP_VERSION}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
