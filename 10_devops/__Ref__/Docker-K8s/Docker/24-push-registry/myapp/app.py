print("Docker - Bài 24 — Push lên Registry")
print("------------------------------------------------------------")
print("")
import logging
import os
from datetime import datetime

import redis
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
APP_VERSION = os.getenv("APP_VERSION", "6.0")

r = redis.Redis(host="redis", port=6379, decode_responses=True)


@app.route("/")
def home():
    count = r.incr("visit_count")
    logging.info(f"Home accessed: count={count}")
    return (
        f"Hello from {APP_NAME} [{APP_ENV}] v{APP_VERSION} - "
        f"visitor #{count} - {datetime.now()}"
    )


@app.route("/health")
def health():
    return {"status": "ok"}


@app.route("/config")
def config():
    return {"name": APP_NAME, "env": APP_ENV, "version": APP_VERSION}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
