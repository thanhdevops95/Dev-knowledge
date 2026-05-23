print("Docker - Bài 51 — .dockerignore + USER + HEALTHCHECK")
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

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True, socket_connect_timeout=2)


@app.route("/")
def home():
    try:
        count = r.incr("visit_count")
    except redis.exceptions.RedisError:
        count = "N/A (redis offline)"
    logging.info(f"Home accessed: count={count}")
    return f"Hello! You are visitor #{count}"


@app.route("/health")
def health():
    # Healthcheck KHÔNG cần Redis — chỉ kiểm tra web service alive
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
