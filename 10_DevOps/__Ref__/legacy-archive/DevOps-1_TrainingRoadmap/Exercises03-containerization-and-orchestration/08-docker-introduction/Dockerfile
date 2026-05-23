# 1. Chọn một image gốc. 'alpine' là một phiên bản rất nhẹ của Node.js
FROM node:16-alpine

# 2. Tạo một thư mục làm việc bên trong image để chứa code
WORKDIR /app

# 3. Sao chép file package.json và package-lock.json (nếu có)
# Dấu * là để bắt cả hai file. Việc copy file này trước giúp tận dụng cache của Docker,
# chỉ cài lại dependencies khi file package.json thay đổi.
COPY package*.json ./

# 4. Chạy lệnh để cài đặt dependencies
RUN npm install

# 5. Sao chép toàn bộ mã nguồn còn lại của dự án vào thư mục làm việc
COPY . .

# 6. Mở cổng 8080 của container để cho phép kết nối từ bên ngoài
EXPOSE 8080

# 7. Lệnh mặc định sẽ được thực thi khi container khởi động
CMD [ "node", "app.js" ]
