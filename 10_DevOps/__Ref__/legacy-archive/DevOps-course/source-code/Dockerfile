# Dockerfile - Hướng dẫn Docker cách đóng gói ứng dụng
# Image này dùng Python 3.11 trên Alpine Linux (nhẹ nhất)

FROM python:3.11-alpine

# Metadata về image
LABEL maintainer="DevOps Course"
LABEL description="The Counter App - Flask + Redis"

# Tạo thư mục làm việc
WORKDIR /app

# Copy file requirements trước (tận dụng Docker layer caching)
COPY requirements.txt .

# Cài đặt dependencies
# --no-cache-dir: Không lưu cache để giảm kích thước image
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code vào container
COPY . .

# Expose port 5000 (Flask mặc định)
EXPOSE 5000

# Biến môi trường mặc định
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

# Health check - Docker sẽ tự động kiểm tra app có sống không
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Command để chạy khi container start
# Dùng python thay vì flask run để production-ready hơn
CMD ["python", "app.py"]
