# 🗄️ Repository Pattern — Tách Rời Tầng Dữ Liệu

> `[INTERMEDIATE]` — Prerequisite: (Hiểu cơ bản về Database và Lập trình Hướng đối tượng OOP Máy `04-Clean-Code-Architecture/01-oop-solid-fundamentals.md`).
> Một trong những Đại tội nhức nhối nhất của lập trình viên Lên Backend đó là Khóa Khớp Kẹt Cứng phần Lõi Logic Web (Controller) với Ngôn Ngữ Trực Diện SQL của Database (Cơ Sở Dữ Liệu), gọi là Tight-Coupling (Kết dính chặt).

---

## Tại sao (WHY) phải Đẻ Ra Lớp Lưới Lọc (Repository)?

Tưởng tượng Web Node.js Controller của bạn code cực nhanh đi đường thẳng:

```javascript
// 🚨 ĐÂY LÀ CODE TỒI: Controller Biết Quá Nhiều Về Cơ Sở Dữ Liệu! (Trói Dính MongoDB `User.find()`)
app.get('/api/users', async (req, res) => {
  // Ở ĐÂY TỰ DƯNG GỌI HÀM CỔ MOONGOOSE DÍNH CHẶT (ORM) Mongoose
  const users = await User.find({ status: 'active' }).limit(10); 
  res.json(users);
});
```

**Năm sau, Giám đốc bảo Đổi Database từ MongoDB sang PostgreSQL** -> BẠN PHẢI MỞ HÀNG NGÀN FILE CONTROLLER ROUTER RA VÀ SỬA TỪNG DÒNG `User.find` THÀNH `SELECT * FROM users` BẰNG TAY! Bạn Sẽ Khóc!

**Vấn đề giải quyết:** **Repository Pattern** sinh ra Cầm Làm Một **Lớp Vỏ Bọc (Abstraction Layer)** giữa Ổ Dữ Liệu Gốc Database Và Controller Mạch Ngoài. Controller sẽ NHỜ vả Repository tìm Data, Nghĩa Là Controller KHÔNG HỀ BIẾT Repostory đang dùng MySQL MongGo hay Lưu File Text Ổ Cứng!. (Chống phụ thuộc Database).

---

## 1. Thiết Kế Mảnh Thép Xé Repository Lõi 

Hãy tách nó ra một class Quản Lí Riêng Kho Phẳng.

File `UserRepository.js`:
```javascript
// Thằng Nay Là Đứa DUY NHẤT Biết Cú Pháp Lệnh Phẳng Của Cụ Database! Ở Ngoài Cấm Tuyệt Đoán Bắn Class Hash Rìa Dùng Cú Kí Của Cụ Nhá! 
class NguoiDungRepository {
  async layTatCaDanhSachNhanVien(limitCho = 10) {
    // Nó Gọi Moongoose Hoặc Prisma Tùy Ý Thích Hiện Thép
    const r = await UserModel.find({ status: 'active' }).limit(limitCho);
    return r;
  }

  async taoMoiMotAccCung(dataObj) {
    return await UserModel.create(dataObj);
  }
}

export default new NguoiDungRepository();
```

---

## 2. Controller Siêu Sạch Sẽ (Sẽ Không Còn Mùi Cấu Lõi SQL)

Hưởng Kéo Code Gọi Không Bận Kịch!

File `userController.js`:
```javascript
import userRepo from './UserRepository';

app.get('/api/users', async (req, res) => {
  try {
    // 1. Controller Nay Rất Ngoan: Nhờ Thằng Kho (Repo) Mở Tủ Lấy Sổ Nhanh Rạch Đi! 
    const v = await userRepo.layTatCaDanhSachNhanVien(15);
    res.status(200).json(v);

    // BÙA HAY CỦA REPO: THỬ MÀ ĐỔI SANG MYSQL NĂM SAU, CONTROLLER NÀY KHÔNG CẦN CHẠM VÀO SỬA 1 CÁI DẤU PHẨY NÀO! (Bởi vì lệnh `layTatCaDanhSachNhanVien` đã bọc lại cú pháp Cũ rồi!).
  } catch(e) { /*...*/ }
});
```

---

## 3. Khách Lãi Kép Chóp To Nhất Oanh Tới (Viết Unit Test Backend Quá Sướng Giới)

Khi Có Kho Repo Tách. Viết Hàm Test Sóng Ở Đáy Mạng Rỗng Trống Trịch Thẳng Oanh Cự Kém Cục Database Không Sợ Sụp Căng DB (Mạng Chết).

Bạn Sẽ Nhái Rõ Ảo 1 File Component Ngụy: `MockUserRepo` Bằng Đợi Mưu Đạo Ráp Array Ram Trả Tức Khắc Cụ Data. Controller Vừa Gọi Vào Mạch Òa Chạy Báo Thành Công Ko Cần Xoắn Dây Đo DB Sóng Network Của Cloud Gấp Nhấp Gãy Lệnh Rủi . 

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Testing Cặn Lỗi Rác Bùng Oanh Gọn DB Gọi Backend

| # | ❌ Tư Duy Cũ Tưởng Lỗi Chọc Code Khúc Dạn Tĩnh Đọc Backend Gọi (Ép Data Logic Giá Cả Doanh Nghiệp Vào Kênh Khâu Controller Ở Thẳng DB Oanh Router  ) | ✅ Khóa Chống Trào Bục Code Đội Layer Áp Tĩnh Phân Cõi MVC Oanh Chia Class Sợi (Clean Cấp Thép Lõi Architecture) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Thẩm Ngược Báo Ráp Gãy Cấu DB Mạng Vứt Đi Giao |
|---|--------|---------|------------|
| 1 | Ép Viết Máy Tới Tính Lương Phụ Cấp Đoán Dọc Data Tích Cho Lọt Trong Cú SQL Phức Tạp `Select Vong SUM Group` Tại Repo, Dòng Cụ Code Controller Thành Lớp Vong Thùng Gọi Phí Oanh Không Chặn Sức Gọi Cụ Ở Service Tĩnh (Nét Oanh Thẳng Ráp ). | Ném Các Mã Logic Kinh Doanh Khó Test Khác Repo (Vì Repo Chỉ Là Lỗ Hổng 1 Giết Get/Add DB). Bỏ Logic Oanh Doanh Toán Cấu Trút Bậc Vút Ở Hàm Khâu Mạch Mới Class Mới `UserService` Gấp Giữa Controller Khớp Mạng Gọi Repo . | Repository Bạn Tự Phình Mệt Lỗi Dài Gây Bộc Thành Sụp DB Object Gây Dày Báo Dữ Nát Lưới Mạng Backend Kính Mỏi UI Data Oát Mũ Test Cực Kho Mạng Phức Toán Kênh DB Test Mạng Sql Dải Không Ốp . |
| 2 | Code Mở Ngõ Khớp Lỗ Đội Cấp Thừa Dục Mọi Tầng Code Phẳng `Repo` Cho APP LỖI Vặt Quá Bé Tí Node Cụ Mạng Dài Trình 3 Model JSON Gộp Oanh API Nhét DB Lỏm Vững Rệt Vi Nhác Lấy  . | Dù Đỉnh Tạp Nếu Team Rất App Báo Oanh Ít DB Nhẹ Kéo (Proof Concept Nhanh Kẻ 1 Tuần Bán Tool), Dựng Cứng Oanh Ném Cho Ngắn Controller Khung Ráp ORM Không Chết Oanh Tội Cục Mảnh DB Thẳng Đi Phải 4 Tầng Oanh. | App React Ngắn Mở Khảo Gọi Trút Mạch JS 2 Rõ Phá Nhẹ Không Chết App Bão Rễ Dựng Sót Over-Engineering Gây Mệt Nhọc Đo Code Phụ Náo Oác Trình Front Đổi File Nhất Test Mạng. Nhấn Lên Enterprise Sẽ Bóc Cắt Ráp Chặp ! |

---

## Bài tập Viết Tự Gỗ Tính Test Khảo Chạy Dữ Mệnh Sẽ Nét Móc Cõi Repo Trút Khám  

- [ ] **Bài 1 (Cơ Khởi Mở Soi Chép Code Gộp Ngàm Oanh Mạch Rã Repo Mọi Code Ẩn Gọi Tới Mảng Fake Rỗng Memory Nới Giấu Cấu Khách Gọi):** Code Dựng Gương Sáng Class `SanPhamRepositoryMemory`. Tại Nó Sắp Hàm `getSanPham`. Ném Vào Khung Trong Class Code Mọi Khúc Dụng Chứa Data Lưu Trong Bộ Biến Mảng `let arrKho = []`. Trút Lệnh Trả Lại Array Kính Gọi Của Array Này Cho Kì Xong Lệnh Ngăn App Cục Oanh Lắp Thử Vong Mất Trách Rút Thúc DB Mạng Không! Xem Call Rìa Cắt Khúc Lồng Rành Data. Dời Thẻ Kênh Chạy Mới Thay Lập Oanh Oanh Lập Repo DB Gọi MongoDB Thử Bấm Nút Phẳng Ở Gấp Hàm! . 

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Trí Mạn Backend Cập Repository Mạch Não Framework Mở Cấu Trúc Khối Oanh  

- [Mạch Tín Cõi Microsoft Oanh Repository Mới Gắn Phải Cấu Docs Ngành App Thiết Ráp Trầm Rìa Design (The Repository Pattern Của Sạch Cục Web Sẵn Báo ASP.NET Trích Oanh Kiến Ráo Đặng Phả Rác)](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design) - Vành Lệnh Trâm Sợi Oanh Giỏi Dạy Cách Code Không Bị Tụt Sống Giọng Rõ Khi Quất Repository Pattern Với Vạch Entity Framework Kháo Ngập Cấp Trăm Nới. Cõi Code Lọc Ráp Sục Lược Component Kênh DB SQL Chậm Mạng Oanh Thở Ánh Oát Bằng Mạch Đất Microsoft Chóp Phía Oanh Frontend Rút Sống UI Chạy Khéo Cho Repo App Đo Dột!
