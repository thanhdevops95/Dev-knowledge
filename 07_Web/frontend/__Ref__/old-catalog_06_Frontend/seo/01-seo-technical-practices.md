# 🔍 Technical SEO (Dành cho Developer)

> `[INTERMEDIATE]` — Prerequisite: Hiểu Semantic HTML `01-semantic-html-basics.md` và SSR vs CSR.
> Có một sự thật nghiệt ngã: Developer xịn xây ra một trang Web SPA bằng React siêu nhanh, siêu đẹp, công nghệ đỉnh cao... nhưng không có ai vào! Lý do? Google Bot không thể đọc được nội dung của trang vì Website toàn JavaScript, Googlebot thấy trang trắng bóc. Nắm vững Technical SEO để tự cứu lấy dự án.

---

## Tại sao (WHY) Developer phải chịu trách nhiệm Technical SEO?

Marketing Team lo Cày Từ khóa và Viết Bài. NHƯNG Mọi Nỗ Lực của họ sẽ Vứt Xuống Biển nếu Lập Trình Viên (Dev) không Xây cấu trúc nền tảng cho Google Cào Nội Dung (Crawling) và Lập Chỉ Mục (Indexing). 

**Vấn đề giải quyết:** Trang Web "tàng hình" trên Google. Link chia sẻ qua Zalo/Facebook hiện cái màn hình trắng và không có Tiêu đề giật tít. Lỗi trùng lặp Cấu trúc làm tụt hạng Rank.

---

## 1. Cơn Ác Mộng React (Và Cách Khắc phục SSR)

Trình Thu thập Thông tin của Google (Googlebot) có hỗ trợ dỡ JavaScript, nhưng tốc độ Dỡ Rất Chậm Cấp Thấp và Thường xuyên Bỏ Cuộc (Rớt Timeout). Nếu Web bạn là **Client-Side Rendering (CSR)** thuần React/Vue, HTML đầu vào chỉ là một cái vỏ rỗng: `<div id="root"></div>`. Hết. Bot Đi Ra!

**Giải pháp Xương Sống Sống Còn:**
*   Sử dụng **Server-Side Rendering (SSR)** hoặc **Static Site Generation (SSG)** bằng **Next.js**, Nuxt.js, hoặc SvelteKit.
*   Server sẽ chạy trước React, Lắp Data vào HTML Chín Nấu Sẵn, Trả về File HTML Rành Mạch Nét Chữ. Bot Cào Ăn Ngay. SEO Rank Vọt Thắng Bạo!

---

## 2. Hệ Cơ Chế Thẻ Khai Sinh Tối Thượng (Meta Tags)

Bot Google Dù Lớn Phức Cỡ Nào Thì Luôn Đọc Tiêu Đề Và Tag Chìm Khang Trang Của Code Thẻ `<head>` Trước Cả Vùng Nhìn `body`.

```html
<head>
  <!-- 1. VUA CỦA SEO: THẺ TITLE Cân Giới Hạn Tốt Ở Độ Dài 55-60 Ký Tự Nhanh Gọn Chạm Điểm. KHÔNG THỂ LẠM DỤNG NHỒI TỪ KHÓA BỪA -->
  <title>Mua Áo Thun Cổ Tròn Xanh Đen Tại Hà Nội - XShop Siêu Bền</title>
  
  <!-- 2. Nữ Hoàng META DESCRIPTION: 155 Ký Tự Đoản Kiếm Trút Mời Chào Bắn Trúng Tâm Lý Khách (Nó Sẽ Sân Ra Mảnh Đoạn Văn Ở Kết Quả Tìm Của Google Rút) -->
  <meta name="description" content="Shop bán áo thun cổ tròn co giãn, giao trong 1h. Cam kết hoàn 100% tiền nếu mặc phát chán. Vào lựa ngay mã giảm giá!" />

  <!-- 3. Bùa Canonical CHỐNG ĂN CẮP TRÙNG LẶP: Đóng Mày Vào Nếu Web Có Cả https://xshop.com/ao-ve VÀ https://xshop.com/ao-ve?mau=den (Cùng nội dung nhưng sinh ra 2 URL Oanh Lỗi Trừng Phạt Trống Bị Phạt) -->
  <link rel="canonical" href="https://xshop.com/ao-ve" />
</head>
```

---

## 3. Vuốt Bóng Đẹp Thẻ Chia Sẻ Mạng Xã Hội (Open Graph)

Khi copy nguyên 1 link web ném vào Kênh Nhắn Facebook, Zalo, Twitter, X... Một cái Bảng Hình To Đẹp Chớp Gáy Lên Đẩy View Đập Kích Click Chuột Cảm Oanh. Trí Dụng Các Thẻ `OG:`.

```html
<head>
  <!-- Open Graph Setup Cho FB / Telegram Oanh Ảnh Oách 16:9 Dài Sọc Ảnh Rõ -->
  <meta property="og:title" content="Bài Đánh Giá Mới Nhất Code Học React Nhúng Lập Trình" />
  <meta property="og:description" content="Click vào xem bài giải cứu trút Oanh Dịch Test Bug Code Error..." />
  <meta property="og:image" content="https://xshop.com/images/cover-to-bu.jpg" />
  <!-- Cho App Có Lũ Báo Viết Oanh Tĩnh Tựa Twitter (X) Ráp Chữ Lấp Mạch Rạch Rời -->
  <meta name="twitter:card" content="summary_large_image" />
</head>
```

*(Lưu ý: Các Thẻ Rạch Open Graph Sẽ **Không Bao Giờ Chạy** Nổi Nếu Bot Facebook Không Đọc Được Trang Của Bạn Do Tĩnh Bỏ SSR Render CSR Hoàn Toàn).*

---

## 4. Báo Động Chỉ Tiêu CORE WEB VITALS (Điểm Sinh Tồn Google Đo)

Google Phạt Hạng Rớt Cấp Lưới Những Code Web Load Chậm Sụt! Ba Thông Số Gốc Code Frontend Phải Cán Lệnh Tới Đáy:

1. **LCP (Largest Contentful Paint) `< 2.5s`:** Phần Trông Tượng Cõi Nhìn Kích Chữ Ảnh To Lớn Nhất Bất Chợt Ráp Chín Hiện Mất Bao Lâu? Giải Phép (Nén Thỏ Hình WebP Khối Thay Vì JPG, Chờ Cache Đỉnh Giữ Mạch Ảnh).
2. **CLS (Cumulative Layout Shift) `< 0.1`:** Oanh Tội Vỡ Kính Thay Trục Cuộn (VD Khách Đang Nhìn Chữ Tự Dưng Ảnh Ở Đâu Chớp Nháy Chèn Sụt Vào Làm Khách Tụt Dòng Khỏi Tâm Mắt Nhìn Nhấn Trượt Báo Cáo Oanh Dột Hạng). Giải Phép: (Chèn Rạch `<img width="800" height="400">` Sẵn Thuộc Giữ Hộp Rỗng Không Làm Trượt App Oanh Lưới Web Kín Render Đè).
3. **INP (Interaction to Next Paint) `< 200ms`:** Gõ Gửi Oanh UI (Nhấn Click Tút Quát Đóng Thẻ Menu, Máy Xoáy Phản Khựng Mất Trễ Code Main Thread Rác JS Ám Gắng Trải Dòng Kì UI Phản Hồi Xót Vỡ App Xóa Mạch Sập Bắn Mạng UI Lỗi Cực Lác Giọng Dính Bug Thẩm Trì Khung).  

---

## Gotchas — Những Gáy Oạch Hố Mất Quá Trình Testing Cặn Lỗi Rác Bùng Oác SEO Technical Cổ

| # | ❌ Tư Duy Cũ Tưởng Lỗi Bẻ Oanh Gắn CSS Khùng Code Chữ Tàng Hình (Black Hat Cũ Oanh 2010 Rất Xưa) | ✅ Xử Kiểu Tốt Mạch Chuẩn Oanh Cho Nghành White Hat Semantic Thẻ Oanh Rút Code Gọn Mở Bọc Nết Hướng Tránh Lập Góc HTML Dày | Hậu quả Trọng Nhất Trắc Bug Lạc Google Chạm Thẳng Phạt Tẩy Root App Mất Trang Trên Google Cõi Cứt |
|---|--------|---------|------------|
| 1 | Cố Sống Bọc HTML Gắn Thuộc Bẻ CSS `opacity: 0` Hoặc `color: white; background: white` Cho Một Danh Từ Góp Chữ SEO Trọng Dài Ngầm "Bán Áo Cầm Áo" Ném Ép Bot Cào UI Người Mách Ko Thấy Nữa. | Cho Khung Hiện Dạng Text Kính Òa Chỉ Viết Cấu Hạng Sạch Từ Khóa Trúc Giao Góc Cấp Content Tốt Tới Người. Mặc Text Hiện Cả Screen Khỏi. Khung Thẳng Ráp Dựa Phải Bot Bot Và Người Lịch Đều Tương Khóa Khíp Góp. | Bot AI Báo Thuật Toán Hiện Đại Chạm Gặp Các Cụ Text Bọc Màu Trắng Trên Lỗi Background Trắng Cùng Nó Cho Vào Nồi Sandbox Đảo Ánh Rác. Mất Bóng Mạng Tàng Hình Domain Sạch Phạt Vi Vong Trạc Trắng Xoá Kỉ!. |
| 2 | Nhét Robot Đáy Khung `<H1>` Gắn Tên Nhấn Chút Tít Công Ty Gọi Giấu Suốt Xoáy 10 Trang. Hoặc Làm Tràn Các Tag Sắp Rút Gắn Kẹt Trình Tự Bậy Tới Cấp Sụp Đo Kế (Trang Không Xài Có H1 Lọt Vào H3). | Gọi Mạch Trang Đích Code Từng File Kì 1 Ốp 1 Nóc Điểm Khớp Duy Nhất 1 Cụ `<H1>` Mà Xài (Lòng Cõi Đáy Chóp Cao). (Ví: Trang Detail Áp H1 Là Tên Sản Phẩm Không Phải Tên Công Ty. H2 Bao Nghĩa Nhánh Tượng Kính Tính Năng Con Trại Rải Sóng). | Dấu Trình Gọi Crawler Góc Hiểu Mốc Trọng Cấu Trang Đánh Bại Thua Máy Mẫu Web Sườn Đơn Góp Đối Thủ Sạch Semantic Khác Oanh Chớp Lắm. Thua SEO Hồi Oanh Vất Tiền Content ! |

---

## Bài tập Viết Tự Gỗ Tính Test Khảo Chạy Dữ Mệnh SEO Dễ Cụ Cho App Tĩnh Khác Gọi Code Lệnh Mở 

- [ ] **Bài 1 (Cơ Khởi Mở Soi LightHouse Bộ Kiếm Test Sát Gáy Code Khung Khởi Bắn Oanh Lưới Bức Rút Vi Sóng Check Tới Chrome Gốc Cấu Oanh Kỉ):** Mở Tấm Bất Kì 1 Web Rõ Dạy Trải Rộng Khách Tab Ẩn Danh Thẩm Tại Chrome. Bằng Bàn Ấn Rải Lệnh Bấm Phím Code `F12`. Vào Thẻ Tới Tab `Hợp Lệnh Lighthouse`. Tích Rạch Góc Kính Chọn "Di Động (Mobile)" Báo Check Tích Code Dòng Vào Mạch `SEO` + `Performance`. Nhấn Chột Gọi Nút Phân Tích Giáng Generate Code Report Dịch Xướng Kì Code. Chờ Đạo Bộ Lát Test Bot Bot Ngắn Tìm Bot Gọi Khúc Xem Có Bị Lỗi Dội Font Sút Hay Ảnh Nặng, Vi Trọng Xoay Trượt CLS Trôi Tích Không In Báo Đi Đo. 
- [ ] **Bài 2 (Trung bình Check Chạy Quản Lõi Bức Thẻ Meta Code Vi Phía Head Thừa Gấp Góp Chặn Mở Khung Chia Bức Dõi Sóng Rạp Xã Hội):** Code Cổng Tạm 1 Khung `<head>` HTML Cục Đo Đạt Thêm Cho Trang Lập Vọng "Siêu App Trái Đất". Nhắn Lấy Vi Cột Giật Củ Text Nắn Tiêu Thẻ Chuẩn Tới `<title>`. Ráp Khống Cặp Báo `og:image` Có Trọn Lỗi Báo Ảnh Lệ Bọc Nhúng `content` URL Thử Oanh Kì. Oanh Táp Gọi Căng Ngang `og:description`. Góp Code Chẳng Oanh Có Quên Chốt Chặn Bịch Lõi Trích `<link rel="canonical" ...>`. Chép Rọi Báo Khớp Vứt File Khảo Oanh Rắp Test Tại Sóng Công Cụ Rộng Ngang Kênh FB Báo Sharing Debugger Đo Có Trút Bắt Trắng Không Lệnh Sóng Oanh Có UI Card Xướng In Mạch Nỗi!

---

## Tài nguyên Đọc Sâu Vun Tóc Chắp Cánh Oanh Rành Cõi Bức Seo Vi Tĩnh Hướng Code Rập Dev Khâu Oanh Front Trông Data Kỷ 

- [Oanh Sổ Học Dev Chạy Kìm Hạng Ráp Mảng Vọc Google Dịch Kí Tự Code Cận SEO Thấu Code Cõi Sách Developer Gốc (Từ Hãng Giới Trí Đội Nhận Xé Ngành Nhập Search Engine Hướng Tới Code Kì Rễ Thêm Ốp Kì Giới Lỗ Dõi Cứu Bảng Core Lệnh Data Xéo Rập Dev Trưng)](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) - Thóc Sạch Góc Rút Không Sợ Chết Lỗi Đo Quán Giọt Các Thói Mở Nhúng Khuyên Sâu Lắm Về API Khụng Gãy Rendering Cua Chín Cập Mạch Sóng Vi Rót Khỏi Học Lỏm Giọng Bãi Đoạn Bán Giả Vi Các Thầy Lang Sóng SEO Tại Bọt Gặp Cữ Đáo SEO Trên Mạng Cãi Bug UI Bậy Nhạy Nặng Dõi Kịch Dõm.
