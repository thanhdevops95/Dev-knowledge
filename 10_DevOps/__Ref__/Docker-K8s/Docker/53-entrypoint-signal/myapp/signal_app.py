"""Demo app — in PID, bắt SIGTERM/SIGINT để chứng minh graceful shutdown."""
print("Docker - Bài 53 — ENTRYPOINT vs CMD + Signal Handling (PID 1)")
print("------------------------------------------------------------")
print("")

import os
import signal
import sys
import time


def handler(sig, frame):
    name = signal.Signals(sig).name
    print(f"[PID {os.getpid()}] Got signal {sig} ({name}), shutting down gracefully", flush=True)
    sys.exit(0)


signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

print(f"[PID {os.getpid()}] Running... waiting for signal", flush=True)
while True:
    time.sleep(1)
