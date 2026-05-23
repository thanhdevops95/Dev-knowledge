FROM python:3.11-slim

# curl cần cho HEALTHCHECK (image slim không có sẵn)
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Tạo user không có quyền sudo
RUN useradd --create-home --shell /bin/bash --uid 1001 appuser

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

# Chuyển ownership và đổi user — mọi bước sau chạy bằng appuser
RUN mkdir -p /app/logs && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -fsS http://localhost:5000/health || exit 1

CMD ["python", "app.py"]
