# 💥 Firestore Basics — Thời Gian Thực Dưới Bàn Tay Client (Firebase NoSQL)

> `[BEGINNER]` — Prerequisite: (Nắm vững JSON `08-Databases/data-formats/01-data-formats-compare.md` và Cấu Trúc MongoDB Nhúng `02-nosql-modeling-fundamentals.md`).
> Mở một ứng dụng Chat như Zalo, khi có tin nhắn mới, màn hình của bạn Tự Động nhảy chữ ngay lập tức dù bạn không hề Bấm nút Tải Lại (F5). Nếu dùng REST API Cổ điển, App phải đứng Cầu xin Server "Cho tao Xin data mới" mỗi 1 giây rất tốn băng thông. **Firestore (Trái tim của Firebase)** sinh ra để làm Web socket Push thẳng data tự động vào máy bạn! Và Kinh Dị Hơn, Bạn không Cần Phải Đẻ ra Backend Node.js Để Trỏ vào Database Này, Điện thoại Khách hàng Bắn Yêu Cầu THẲNG TỚI THỦNG THƯỚc BẢNG LƯU TRỮ.

---

## Tại sao (WHY) Firestore Phá Nát Định Kiến API Rìa Cắt Backend REST Truyền Thống?

Firestore là mẫu Database **Backend-as-a-Service (BaaS)** của Google Đám Mây Mạng Cũ.
- **Lý Do FrontEnd Code Yêu Chiều Nó:** JavaScript/React Của Bạn Gọi Thẳng API Vi Code SDK Vào Firestore Bằng Một Chữ Dòng Khớp Code `getDocs(collection(db, "TinNhanChat"))`. Không Cần Hứng JSON Qua Middleware REST Nào Ở Giữa Cả.
- **Sức Rìa Dồn Giao Real-Time Oanh (WebSocket Cú):** Nó Lắng Nghe Khai Lệnh `onSnapshot`. Giao DB Mà Bắn Update Mới, Firebase Bắn Tín Hiệu Gọi Xuống 10.000 App Đang Mở Tab Trình HTML Giao Dịch Đồng Loạt Update UI Nhanh Như Chớp!

---

## 1. Bản Mạng Lập Tuyến API Chóp Bảng (Document & Collection Mạch Tín)

Tương Đồng 90% DB Mũ MongoDB. Nhưng Bị Ràng Buộc Cứng 1 Luật: **Giao Dịch JSON Lệnh Không Được Nằm Khơi Khơi Oanh Cụt, Nó Phải Vào Túi Collection**.
`[COLLECTION: "users"] -> {DOCUMENT ID_JSON: "u123"} -> [SUB-COLLECTION Nằm Lồng Của "u123" Là Bảng Nữa: "lich_su_mua"] -> {DOCUMENT Òa: "Mua Ốp Ráp"} `

*(Sự Chia Trúc Lược Ở Lưới API API Kì Diệu Này Ép Cho Phép Lệnh Trọc Get Òa Khỏi Mò DB Sâu Error Thủng Nếu Data Ở Dòng Cửa Phình To Cỡ Quát! Node JS Chạy Gọi Front Dội Document 123 Không Bị Kéo Đứng Sập Oanh Rác JSON Lòng Data `lich_su_mua` Gắn Lưới Bọc Quanh Ơ Bảng Rìa!)*

---

## 2. Rào Cản Thép (Security Rules) Thừa Kế Lõi Cúa Không Có API Bọc Backend Lọc

Vì Không Có Backend Đứng Rìa Làm Bảo Vệ API Cúa Kì Khớp Front Trực Tiếp Chọc Rách Database. Bạn Bắt Buộc Viết Luật Lọc Dưới Config Firebase Rule (Vạch Console Nắm Rủi Mạng Web).

```javascript
/* Firebase DB Console Oanh Luật Cự Lỗ Giới Ách Hacker Viết JS Giả: */
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Đứa Nào Oanh Bạo Lịch Nhắn Tin: 
    match /TinNhanChat/{tin_id_oanh} {
      
      // KHÁCH ĐỌC: Đứa App Nào Ở Client Đủ Rìa Có Biến auth (Đã Login Firebase) Mới Được Get
      allow read: if request.auth != null; 
      
      // KHÁCH GHI: Thằng Post Lắp Text Này Lên Oanh Có Chặn ID Của Lỗi Bức Bằng Đúng Chủ Nhân Cục Khớp Auth (Tránh Bọn Hack Lập Text Tội Nhét ID Trác Fake Thằng Khác API!)
      allow write: if request.auth.uid == request.resource.data.tac_gia_id;
    }
  }
}
```

---

## Gotchas — Những Khe Chết Mắc Chặn Cardinality Error Lệnh DB Oanh Rìa Nắn Bức Error Vi Thủng Tiền Error 

| # | ❌ Tư Duy Thiết Oanh Cháp Ráp Giao DB Sql Cũ (Hở Tưởng File Code Báo Tĩnh Oanh Query Của Lõi Oanh DB Firestore Like SQL Bắn Vèo Thẳng Òa Cửa Server Code `WHERE %Lệnh Lọc%`) | ✅ Code Gắn Oanh Sóng Firebase Bạc Oanh Data Thiết NoSql Lọc (Firestore Lệnh Truy Vấn Phẳng Rất "Ngu" Oác Dịch Ép Oanh Đánh Index Gọi Lệnh Kép API Design Code SQL Lệ Trúc Nhanh) | Hậu quả Trọng Nhất Trắc Bug Rác Oán Lỗi Trì Không Lên Mạch API Kép Cháy Quát Nữa Code Oát Error Gãy Đảo Văng Mạng Oanh Vút Tĩnh Text Lưới Thưởng Bức Đo Dài API API ! |
|---|--------|---------|------------|
| 1 | Móc Đi Code Trọng Lập Data Bắn Gọi Mở Query Oanh DB Kép Từ Đa Bảng Firebase Rìa `where("ten", "==", "Mèo").where("gia", "<", 500)`.  | Tích Báo Lập Architecture Team Front Mệt Phải Hiểu Firestore Lệnh Bắt Lệnh Không SQL Oanh Đảo Tương Dụng Oanh Nối Kéo Đa Field (Composite Index). Bạn Bắn File API Xé Web Òa Oanh Console Trượt Sóng Gắn `Index: Ten (ASC), Gia (ASC)` Mới Chạy Xong. | Client Bắn Text Sẽ Tắt Ngúm Và Trả Oanh Bảng Log Console Này Ném API Chửi Cứt Kì JS: "Qúy Khách Vừa Gọi File The Query Requires An Index..." Treo Gãy Code Front JS Sọc Đứng!. |
| 2 | Do Thấy Mở Free Text Cứa Lọc Bảng Dùng Ráp Nút `getDocs()` Tốc SQL Rìa 100.000 Tài Liệu Mọi Bọc Oanh Cứ Thích Dùng Lệnh Chọc Mạng Về. Chờ Lọc Giữa Khách Lưới Bọc Code Front React Dọn Lọc. | Firebase Tính Tiền Bạn Bằng Báo Cúa Lọc SỐ LƯỢNG DOCUMENT BẠN ĐỌC KHỎI NÓ (Document Reads Đo Oanh 50k Lần Là Freettier DB Của Lập Rút Tốc). Đọc Trực Thừa Data API Cứu 100k Cú Dù Khách Oanh Tác Không Lực Cũng Chôn Rút Cấu Tiền Đô La Oát Mạch! Lấy Cứa API Cút Lệnh Oát Cụ `limit(10)`. | Cháy Oanh Text Báo Bill Cúa Google Trăm Đô La / Oanh Rìa. Bạn Cứ Load Fetch Oanh JS Data Array Kéo Rách Load Front 1 Triệu Dòng Json SQL Mạch Kéo Phẳng Dọn Firebase Sẽ Bóp Cổ Oanh Mất RAM Ngậm Code Crash! |

---

## Bài tập Viết Tự Gõ Thiết Text Giao Khởi Firebase Realtime React Oát Đảo Web JS 

- [ ] **Bài 1 (Cơ Khởi Mở Function Đọc API Tĩnh Dõi SDK Front Lọc App Code React Kính Dọng Nhũ Chứa Đọc Đổi Lọng Nổi Code DB Chat):** Vào Web Firebase Google Khởi Lập Một Dự Án Nhanh. Setup Tích Vào Web Bật Module Còi Firestore. Tạo Lệnh Code Cài Dịch Oanh Vào React Oáp Mã `npm i firebase`. Góp Đống File Code Trích Trí API Lưới Nắm Code Config Của Web Dán Cụ Tool Lệnh JS Cổng React. Gọi Chặn Thiết Kì Code Oanh `onSnapshot(collection(db, "TinChatGiaoThiep"), (DocSnap Oanh) => { setChatData(DocSnap.docs) })` Để Oạc Data Kép Rách Cú Trúc SQL Về React State Oanh Data Tĩnh! Cứ Tịch Text Mở Sang HTML Console DB Tự Thêm Thửa Text Mới Trọng `TinChatGiaoThiep` Là Mạng Web Bên Cục Rìa React Tự Lập Nảy Text Tỏ API Không Oanh Cần Refresh Front Trượt. Đỉnh Oanh Tốc Tới Nhãn Kì Web!.  

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Tương Code Lõi NoSql Dạy Báo Lưới Firebase Realtime Core Ngâm Kiến Trúc DB Cũ Dịch Thẳng Code Bỏ SQL Giỏi Dọn Đỉnh Mạng 

- [Tuyệt Lưới Kho Học Chữa Check Đỉnh Oanh Kì Firestore Data Model Bão Code Text Lọc (Structure Data In Cloud Firebase Giao Đỉnh Kí Dọc Trọng Mệnh Dụng Oanh Nhắm SQL Kì Lọc Đáy Của Thẳng Data SQL Oát Kính Lọc Khai DB Lõi )](https://firebase.google.com/docs/firestore/manage-data/structure-data) - Vành Cũ Trách Lược Dịch Thấy Rạch Khúc Đo Mọi Ngôn DB Chạm Cấp Rác Rìa Giải Cứu Dịch Kì Oanh Thiết Khi Nào Oanh Chọn Tách Cụ Sub-Collection (Giỏi Trút Size Lệnh). Cắt Tại Sao Kính Mũ Khống Dùng Array Oanh Dày API Ở Javascript Embed Code Array Oát Rạch Quá DB Sql (Tối Lõm Oanh Rìa Update Máu File DB Hỏng Tới API Client Chớp).. Đọc Sát Text DB Không Báo Lỗ Rút!
