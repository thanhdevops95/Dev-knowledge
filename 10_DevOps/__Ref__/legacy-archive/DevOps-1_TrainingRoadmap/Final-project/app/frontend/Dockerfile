# Frontend Dockerfile - Multi-stage build

# ----- Stage 1: Build -----
# Giai đoạn này dùng Node.js để build ứng dụng React.
FROM node:16-alpine AS build

WORKDIR /app

# Sao chép package.json và package-lock.json (nếu có)
COPY package*.json ./

# Cài đặt dependencies
RUN npm install

# Sao chép toàn bộ mã nguồn
COPY . .

# Build ứng dụng, tạo ra các file tĩnh trong thư mục /app/build
RUN npm run build

# ----- Stage 2: Serve -----
# Giai đoạn này dùng Nginx để phục vụ (serve) các file tĩnh đã được build ở stage 1.
FROM nginx:1.21-alpine

# Sao chép các file tĩnh từ stage 'build' vào thư mục web root của Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Expose cổng 80 mà Nginx lắng nghe mặc định
EXPOSE 80

# Khi container khởi động, Nginx sẽ tự động chạy.
CMD ["nginx", "-g", "daemon off;"]
