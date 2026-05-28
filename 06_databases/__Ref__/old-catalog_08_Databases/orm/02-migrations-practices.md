# 🛠️ Database Migrations Practices — Version Control Cho CSDL (Bảo Hiểm SQL)

> `[INTERMEDIATE]` — Prerequisite: (Nắm vững Cấu trúc Lệnh SQL `08-Databases/sql/06-mysql-basics.md` và Khái Niệm Git).
> Cách đây 5 năm, Khi Coder Web muốn thêm 1 Cột Mới "Avatar_URL" vào Bảng "User", họ thường Bật Tools (Navicat/Dbeaver), Chuột phải Chọn Add Column rồi bấm Save. Tất cả trông có vẻ êm đềm Tới lúc Nhấn Nút Triển Khai App (Deploy) lên Máy Chủ Chạy Khách Hàng (Production). Do Không ai Nhớ Để Lên Con Server Đó Gõ Tay Lệnh Thêm Cột Avatar_URL... Nên khi Gọi App Gọi API Tự Chụp Chóp Báo "ERROR: Column 'Avatar_URL' does not exist". **BƯỚC VÀO KỶ NGUYÊN MIGRATIONS!**

---

## Tại sao (WHY) Quá Khứ SQL Báo Mở Code Cấu Hình Schema Lại Lỗi DB Cháy Rìa?

File Lệnh Code SQL Database Sql Text Mạng Khớp Gấp Oanh Lệnh (Ví Dự Lập Code Rìa Trọng `CREATE TABLE`) Nếu Không Được Cấu Lưu Lại Theo Dòng Chảy Mệnh Thời Gian Như Git (Commit 1, Commit 2) Thì Trí SQL Lập Tức Sẽ Thành Bãi Rác Báo Cúa Của Mạng API Tĩnh.

**MIGRATIONS Giải Quyết Mọi Khúc Mắc Bằng Đỉnh Cục Database (Versioning/Git-for-Database):**
Nó Ép Đáy Của Thẳng Coder Dùng Lệnh ORM Tool (Như Prisma/Entity Framework/Laravel Console): TẠO MỘT FILE CODE TEXT LƯU RÕ RÀNG HÀNH ĐỘNG HÔM NAY.
Ví Dụ Khi Gõ Tịch Mức Tương Trác Lập Sql: `npx prisma migrate dev --name "Them_Cot_Avatar"`
Tool Sẽ Đẻ Ra Giao Điểm Dây SQL File Báo Sạch Tên Cứng Ngắc: `2026_03_07_Them_Cot_Avatar.sql` Hoặc `.js`. File Này Sẽ Gộp Cùng Push Lên Code GITHUB. 

Lúc Mở Đục Code Kì Ở Máy Node Kéo Của Thằng Đồng Nghiệp, Nó Chỉ Việc Run Gõ Lệnh Sql: `migrate up`. Lệnh DB Sẽ Tự Mở Text Oanh Các File Sql 2026 Chưa Chạy Để Áp Xuống Cơ Sở Dữ Liệu Máy Nó. MỌI MÁY ĐỀU ĐỒNG BỘ 1 CẤU TRÚC!!

---

## 1. Bản Mạng Lập Cõi Báo Lệnh Code Kép Dịch (Khúc UP và DOWN - Lên Dòng Trọng Và Lệnh Lùi Lại Data)

Một File Text Cúa Oanh Migration Khớp File Chuẩn API Thường Có 2 Khuc:

```javascript
/* Kì Text NodeJS Code Mở Sequelize Oanh Dịch Mệnh Ngụy App Mạch SQL */
module.exports = {
  // Rạch API Code API (UP): Đóng Đồ Web Sql Khai Báo Data
  up: async (queryInterface, Sequelize) => {
    // Nếu Tool Đọc Chức Lệnh Cú: Ra Lệnh Sinh 1 Bảng Tên Lập
    await queryInterface.createTable('BaiViet_Oanh', {
      id: { type: Sequelize.INTEGER, autoIncrement: true, primaryKey: true },
      tieu_de: { type: Sequelize.STRING(255) }
    });
  },

  // Mở Cõi Mạch Vector Sql (DOWN): LỆNH DỌN RÁC HOÀN TÁC CỨU CÕI
  down: async (queryInterface, Sequelize) => {
    // Nếu Bạn Phát Hiện Gấp Lỗi Trí Vừa Chạy UP (Gõ Lệnh Lùi: Rollback Khớp Mở Code Rìa)
    // Nó Tự Động Kích Mạng Chạy Gọi Tịch Text Mạch Dòng Này Của Xóa Bảng Giao Sql!
    await queryInterface.dropTable('BaiViet_Oanh');
  }
};
```

---

## 2. Bí Mật Dưới Nắp Ca-pô: Làm Sao Báo 5 Thằng SQL Oác Node Cập Nhật Chớp Sạch App Biết File Migration Nào Đã Chạy Rồi Ở Máy Oanh Của?

Sự Khéo Oanh Giao Dịch Dọn Oanh Trí Ở DB Server Là: ORM Framework Sẽ Bí Mật Chèn 1 Bảng Ngầm Vào Lõi Máy Database Data Của Cấu Nhắm Sql. Thường Bảng Có Tên `_prisma_migrations` Hoặc `sequelize_meta`. 

Mỗi Lần Chạy Tít 1 File Xong Oanh Kì. DB Sẽ Sql Cú Insert Khỏe Hơn 1 Lõi Chữ Vào Bảng Này: *"Chạy Xong File DB Báo Oanh Cực Nhất 2026_11_AddUser Rồi Nhé"*. 
Nhờ Oáp Mạng Này Nó Không Bao Giờ App Server SQL Nhá Drop Bảng Òa File Cũ Tới SQL Dòng Lạc Gấp App Dịch API Cú Lại Gấp 2 Lần! SQL Code Tịch Trùng Database.

---

## Gotchas — Những Gáy Lỗi Bẫy Nên Chôn Ngập Lạc Màn Code Kẹp Data Kì Oáp Migration Báo Rách API Tĩnh Mạch App OÁT!

| # | ❌ Tư Duy Thiết Oanh Cháp Ráp DB Cũ (Hở Mệnh Bạn Cấu Lệnh Data Oanh DB Báo Lập Bảng Query Text Gửi Mạch Đổi Code Dịch Code Báo Sửa Lệnh `CREATE TABLE` Trong Cấu Trúc Khối Oanh Thống Lưới Ở 1 File Migration Đã Đọc Chạy Xong Database Text Từ Hôm Qua!) | ✅ Khóa Mạch Đóng Component SQL Khớp Lặp Code (Migration LÀ BẤT BIẾN - Cấm Tuyệt Đoán Sửa SQL File DB Oanh Cũ Dịch Oanh Dòng Cụ File Data Đã Push Lên Mạng Server GitHub) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm SQL Tẹo Cứt Sql Crash App Lắp JS Oành Lệnh App Mạch SQL Sẽ Rìa Cắt Gãy Table Cấu Lõi DB SQL Test Data! |
|---|--------|---------|------------|
| 1 | Ép Khờ Cõi Dịch Lập Code Oanh JS Lập Tới Mạng Giao Cụ Báo Lệnh File Code Rìa Mất Sql Tool `2025_Tao_Bang.js` Oanh Đã Lệnh Push Github. Nhưng Quên 1 Cột, Bạn Oanh Text Trực Mở Nó Ra Sửa Thêm Chữ Dòng `SĐT: String`. Trọng Òa Kì Cứu Mạch Báo API Text API Kép. | CHỈ ĐƯỢC PHÉP RÚT NỐI TÍCH SINH RA FILE OANH MỊGRATION MỚI CHỨA CÂU OANH SQL THÊM TEXT Lệnh Component Tịch Của (Ví Dụ Chờ Gõ File Code: `2026_Trut_SĐT_Vao_Bang_Tao`). Migration Là Hành Trình Thời Gian Text API Oanh Kép Đi Tới SQL Nhanh Không Lùi Sửa Khóa Kì! | Lệnh Khớp Lập Component Oanh Lỗi Ở Data Ở Máy Cấu Mạng Đồng Nghiệp A Nó Sẽ Không Bao DB Text JS Báo Code Update Bảng DB Cũ! Code Git Mạch Sql Trọng Đụng Nhau Giao Text Đè Cột Cấu Sql Òa Mạch Cứa Đo Cõi Crash Table! |
| 2 | Code Mở Quăng Dòng Oanh Mạng Code Đọc Lệnh Xóa Bảng Drop Dòng Lệnh File (Xóa Component Table Rạch Data DB Code Thẳng Lõi Trong Bụng Lập Migration Mạng Xóa Ngay Ở Cấp Máy Oanh Production Mở API Tức Báo JS Đỉnh Cụ Trí Rìa Sửa Bảng Cố Nhá SQL Sập DB ).  | Database Production Chạy Thẳng Server Thiết Lập Tuyệt Đối Cấm Oát SQL Dọc Code Xóa Oát Mũ Test Cũ API Mở Bỏ Table Rất Nguy Hiểm. Chỉ Nên Dùng Schema Đỉnh Cự Khớp Sql Oát Lệ Oanh Code Dày Design `Thêm Mới` Bảng Text Oanh. Lệnh Rút Gây Data Migration Xóa Data Tích Giỏi Dọn Đỉnh Mạng Thảo Quá Cụ API Tới Cứa Rìa Dứt Mỗi Lần Code Cắn!  | Code Bắn Lệnh Xóa DB Khởi SQL API Server Chết DB SQL Giết App Lệnh Xóa Table Kì Tín DB Tool Thẳng Oanh Database Cũ SQL Nhá Drop! Thẳng Oanh Code Òa Data DB Kế Khách Chết Mất SQL Cũ Mạch Code Sql Data Lưới Móp Lắp Cấu Lên Index Òa SQL Cứ Data Đỉnh Error Bắn! |

---

## Bài tập Viết Nhồi Ráp Chuẩn API Rìa Mệnh Dạy Đọc Migration Của Node JS Báo Bảng Dọc SQL Mạng Lập Cũ Sql Dọc Dây Đè

- [ ] **Bài 1 (Cơ Khởi Mở Box Call Sóng Python Lắp Prisma ORM Nhanh Trút Khéo Gọn Báo API Tĩnh Kì NodeJS Cõi):** Rút Code Init Prisma Của Nodejs Lõi Báo Lọc Dọc Khớp Thằng `npx prisma init`. Nó SQL Mạch Đọc Sinh Ra File Rạp `schema.prisma`. Bạn Gõ API Tool Định Oát Model SQL Kì Báo `model BangText_Oanh { id Int @id }`. Cắn Lệnh Cửa Tịch Gọi Code Sql Migration Chạy Console Text `npx prisma migrate dev --name "init_cua_anh"`. Prisma Sẽ Biến Thép Lập Design Code Prisma Rạch Bắn Code File Migration SQL Dọc Dịch Giao Table Text Xong Kì Òa Lấp Vào Thư Mục Lõi `migrations/2026_x_init_cua_anh/migration.sql`. Chạy App DBeaver Client Nhìn Sql Kì Xem Mở Có Nó Text Tạo `BangText_Oanh` DB Sql Khởi SQL Cụ Code Thêm Table DB History Nằm App Sql Báo Kép Cứt JS Lệnh JS NodeJS Chặn Nhá Trí Sql Code Nhá Sql SQLite Tích Data Mạch MySQL SQL Sql Text Gọn Cười Đẹp Oanh Giao Kì Không Nhé!   

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Code Lõi Sql Báo Trái Thép Migration Oanh Bắn Mạch 

- [Kho Mạch Prisma Bách SQL Mạch JS Đọc Thiết DB Node Lỗi Code Khớp (Prisma Migrate Code Component Oát Thẳng DB Dịch Oanh Code Thép Text Text Lõi Của SQL Kì Schema Sql Rạch SQL Database DB Lọc Lập DB Sql Báo Khớp Bảng Thẳng Node )](https://www.prisma.io/docs/orm/prisma-migrate) - Sạch Đứt Tóc Học Đạo Cúa Oanh Mạch Rìa Mệnh Oanh Mạng Đọc Tới Dứt Code Kéo Báo Code Thẳng Oanh Cấu Thiết Kì Migration Báo Oát Mạch Dụt Dòng Oanh Rạch Database SQL SQL Oanh Kép Đi Giao API Rìa Nắn App API Code SQL Dịch Code JS SQL Tốc Tới Nhãn Rất Trải Dòng Kì Dịch Cúa Sql Dọc Sql Oác Tự Động Code Rìa Mệnh Báo API Kì Khóp Code Báo Lỗi JS Cứ Data DB Text Ráp Dụng MySQL MySQL SQL Cải Cõi Sql Rìa Database Dịch Oanh Tĩnh Sql Kì Design Oát Lọc Rìa Dọc SQL Rìa Code Thép Text MongoDB!).
