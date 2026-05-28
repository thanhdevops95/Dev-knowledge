print("Docker - Bài 21 — Network - Giao tiếp giữa các container")
print("------------------------------------------------------------")
print("")
import logging
import os

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

r = redis.Redis(host="redis", port=6379, decode_responses=True)


@app.route("/")
def home():
    count = r.incr("visit_count")
    logging.info(f"Home accessed: count={count}")
    return f"Hello! You are visitor #{count}"


@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
