# Backend Dockerfile
# Stage 1: Sử dụng Node.js Alpine image (nhẹ)
FROM node:16-alpine

# Tạo thư mục làm việc
WORKDIR /app

# Sao chép package.json và package-lock.json (nếu có)
# Việc này giúp tận dụng Docker layer caching.
# Dependencies sẽ chỉ được cài đặt lại khi các file này thay đổi.
COPY package*.json ./

# Cài đặt dependencies
RUN npm install

# Sao chép toàn bộ mã nguồn còn lại
COPY . .

# Phơi" ra cổng mà ứng dụng lắng nghe
EXPOSE 3001

# Lệnh để chạy ứng dụng
CMD [ "npm", "start" ]
