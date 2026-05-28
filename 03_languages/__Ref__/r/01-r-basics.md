# 📊 R Basics — Nhập môn R

> `[BEGINNER]` — Prerequisite: Không có (Biết cơ bản về Toán Thống kê/Excel là một lợi thế).
> Ngôn ngữ sinh ra bởi các nhà thống kê, dành riêng cho tính toán khoa học dữ liệu, vẽ biểu đồ và học máy (Machine Learning).

---

## Tại sao (WHY) lại dùng R?

Trong ngành Khoa học dữ liệu (Data Science), thế giới bị chia làm hai nửa: Python (mạnh về AI/Deep Learning và hệ thống Mạng) và R (mạnh vô đối về Thống kê hàn lâm và Vẽ biểu đồ tĩnh cực đẹp). Mọi thao tác xử lý dữ liệu phức tạp trong Excel đều có thể chạy tự động bằng R trong nháy mắt với vài dòng lệnh.

**Vấn đề giải quyết:** Xử lý file CSV/Excel khổng lồ hàng triệu dòng, mô hình hóa dữ liệu thống kê, và vẽ biểu đồ báo cáo khoa học sắc nét (ggplot2).

**So sánh nhanh:**
| Tính năng | R | Python (Pandas/Matplotlib) | Excel / SQL |
|---|---|---|---|
| **Thế mạnh** | Cực mạnh về Thống kê, Gói Tidyverse vẽ đồ thị số 1 | Cân bằng mọi thứ (Web, API, ML) | Trực quan ô lưới (Excel), Query Truy xuất (SQL) |
| **Cú pháp** | Lạ lùng, hơi cổ (dùng `<-`) | Dễ đọc, OOP | Công thức kéo thả / Rập khuôn |
| **Đối tượng dùng** | Data Analyst, Nhà khoa học | Data Engineer, Software Dev | Dân văn phòng, Kế toán |

---

## 1. Cài đặt Môi trường (R base & RStudio)

Tuy bạn có thể viết R bằng Command Line, nhưng 99% cộng đồng đều sử dụng biến thể IDE huyền thoại có tên là **RStudio**. 

**Cách Cài đặt:**
1. Lên web tải lõi chạy (R Base): [CRAN R-Project](https://cran.r-project.org/)
2. Lên web tải Trình biên soạn (RStudio Desktop Phổ thông): [Posit / RStudio](https://posit.co/download/rstudio-desktop/)

Mở RStudio lên. Bạn sẽ thấy ngay một khung **Console (Terminal)** phía dưới để chạy từng lệnh tương tác.

---

## 2. Hello World! và Cú pháp Gán Lạ Lùng

Trong R, để gán biến, người ta dùng mũi tên `<-` (Phím tắt trong RStudio: `Alt + -`) thay vì dấu `=`. Dấu `=` chỉ dùng khi gán tham số trong một hàm.

```r
# Dòng chú thích bắt đầu bằng dấu thăng
print("Xin chào Thế giới R!")

# 1. Khai báo biến (Tự suy luận kiểu)
name <- "Học giả Data"
age <- 25
is_student <- TRUE   # R BẮT BUỘC boolean phải viết HOA TOÀN BỘ (TRUE / FALSE / T / F)

# 2. Vector — Cấu trúc dữ liệu Tối Quan Trọng nhất trong R
# Hàm c() (Combine) dùng để chắp ngọc tạo 1 danh sách. Mọi thứ trong R bản chất đều là Vector.
diem_thi <- c(8.5, 9.0, 7.5, 10.0)

# Lệnh thống kê làm trọn ngay lập tức!
mean(diem_thi) # Tính giá trị Trung bình
max(diem_thi)  # Tìm điểm Cao nhất
```

---

## 3. Data Frame — "Bảng Excel" Của Giới Lập Trình

Data Frame chính là một cái bảng có Cột (Tên biến) và Dòng (Dữ liệu). Tính năng này của R là nguồn cảm hứng tạo ra siêu thư viện `pandas` bên Python.

```r
# Chắp tay xây dựng 1 Bảng Dữ liệu (Row-Column)
df_sinhvien <- data.frame(
  ID = c(1, 2, 3),
  Ten = c("An", "Bình", "Châu"),
  Diem = c(8.5, 6.0, 9.2)
)

print(df_sinhvien) 
# Kết quả ra Console Lưới Rất Đẹp:
#   ID   Ten Diem
# 1  1    An  8.5
# 2  2  Bình  6.0
# 3  3  Châu  9.2

# Trích xuất 1 Cột Bất kỳ Bằng DẤU ĐÔ LA ($)
print(df_sinhvien$Ten)

# Trích xuất dạng Ma trận [Dòng, Cột]
# Chú ý: R BẮT ĐẦU ĐẾM INDEX TỪ SỐ 1 (KHÔNG PHẢI SỐ 0 NHƯ CÁC NGÔN NGỮ KHÁC)
df_sinhvien[1, 2]  # Lấy Dòng 1, Cột 2 => Ra chữ "An"
df_sinhvien[ , 2]  # Bỏ trống Dòng => Lấy TẤT CẢ Dòng của Cột 2
```

---

## 4. Đặc sản Chói Lọi: Tidyverse & Toán Tử Ống (`%>%`)

R gốc (Base R) khá cổ xưa. Thay vào đó, mọi người dùng gói bộ thư viện vĩ đại nhất của R Mảng Data Science: **Tidyverse** (Đặc biệt là gói con `dplyr`).

Trong Tidyverse, người ta dùng cái ống `%>%` (Đọc là "Sau đó làm cái này") để chèn nối kết quả từ Hàm trước xuống Hàm sau (Giống hệt Lọc Filter / Pipe). Phím tắt: `Ctrl + Shift + M`. Từ R 4.1+, R ra mắt ống chuẩn `|>` ngắn gọn hơn.

```r
# Tải về và Gọi Gói Chuyên Món Lọc Data (Chạy 1 lần trên máy)
# install.packages("dplyr")
library(dplyr)

# Rất tự nhiên: Lấy bảng df_sinhvien
#   -> SAU ĐÓ Lọc (filter) đứa nào Điểm > 8
#   -> SAU ĐÓ Sắp xếp (arrange) tên giảm dần
df_sv_gioi <- df_sinhvien %>%
  filter(Diem >= 8.0) %>%
  arrange(desc(Ten))

print(df_sv_gioi)
```

---

## 5. Vẽ Biểu Đồ Thần Sầu với `ggplot2`

R vua vẽ đồ thị vì cách tiếp cận theo Lớp (Grammar of Graphics). Bạn phủ từng Lớp vẽ lên Cái Bạc Canvas Khung đồ thị Tĩnh cực kỳ Khoa Học Tỉ Mỉ Dễ Thấy. Bằng lệnh cộng `+`.

```r
# Gọi Thư Viện Chuyên Môn Đồ Họa 
library(ggplot2)

# Xây Khung Bạc Trục Oxy (Data Nằm Ở Bảng Nào, Trục X Y Lấy Cột Nào) + Lớp Chỉ Đạo Trục Vẽ Cột Điểm
ggplot(data = df_sinhvien, aes(x = Ten, y = Diem, fill = Ten)) +
  geom_col() +                         # Phủ 1 Phím Lệnh Vẽ Ra Hình Cột Bar Chart
  theme_minimal() +                    # Phủ 1 Lớp Giao Diện Font Đẹp Gọn Minimal 
  labs(title = "Bảng Điểm Thi Phổ Thông Bằng GGPlot 2") # Phủ Lớp Tên Rực Rỡ Ghi Chú Đỉnh Đồ Thị
```

---

## Gotchas — Những Lỗ Hổng Ngã Oạch Dễ Gặp Khi Làm Quen R

| # | ❌ Tư Duy Cũ Các Ngôn Ngữ (Sai Lệch Nhận Thức Lập Trình) | ✅ Phong Cách Nhận Xử R Idiomatic Điểm Tuyệt Đỉnh | Hậu quả của Việc Mang Râu Quái Trí Thói Quen Cũ Vào Đóng |
|---|--------|---------|------------|
| 1 | Cố Mở Chữ `for (i in 1..x)` Quét Mảng Cộng Số List Ngàn Lần Tính Chóng Mặt Mảng Vì Dính Thói Nếp Python JS C. | R Dùng Ma Trận TÍNH Vectơ SIÊU HẠNG Dưới C Tự Động Rập Trọng Nguyên 1 Hàng Nghìn Khối Lên Quét Luôn Thay Cột Lần Nạp Hàm. Xài Phẳng `c(1,2) * c(3,4)` Chứ Đừng For Đục Phá Từ Liệu. | Chạy Góp Code Treo Quay Dòng Đồ RAM Nằm Kẹt R Máy Viết Ngược Xử Thơ Dài Bị Ngán Ức Sập Loop Trong Vector Nặng Khủng Chạy Khổ Sở Gây Nặng Kém Đuối Của Tốc Độ Base R. |
| 2 | Nhầm Đếm Khóa Điểm Địa Mảng Mở Bắt Đếm Nhặt Phần Tử Mục Index Kèm Mang Nhan Đề Từ Số Vạch Không `arr[0]`. | Index Ở Vector Mảng DataFrame Tận Lõi R LUÔN Bắt Dãy Dấu Nhặt Từ Cạnh Điểm Ranh Khai Từ Số Số SÁNG Một (1). `arr[1]`. | Kêu Mảng List Trả `Numeric(0)` Trắng Báo Khống Vất Lỗi Kẹt Tịt Trắng Data Bưng Máy Viết Tầm Kiếm Tạm Hiểu Bể Script Hoảng. |
| 3 | Sợ Gõ Cấu Toán Tử Cài Gọi Gói Gà Dại Nối Quét Hàm Gọi Nối Giao Nhọc Hàm Bao Phủ Trống Vết `round(mean(c(1,5)))`. | Cấp Cho Luồng Tượng Thần Vị Khung Cái Ống Khói Dẫn Tẩu Nối `%>%` Chạy Dài Chuyền Đầu Sạch Rõ Bọc Mượt Data Như Dòng Trôi Nhẹ Chạm Lọc Phểu Rành Mạch Nhanh. | Tháo Sai Cái Hoặc Khung Dấu Bị Văng Block Chứa Kèo Code Tổ Ong (Lồng Dăm Vỏ Nhau Lộn) Sẽ Rút Gãy Mắt Người Kiểm Rất Đau Lọc Nùi Nhờ. |

---

## Bài tập Viết Tự Cải Nắm Thuần R Nền 

- [ ] **Bài 1 (Cơ Bản Mức Vector Chỉ Báo):** Khai Băng Số Chạm Điểm Lệnh Vectơ Qua Bọc Khai Báo Biến Tên `vec_Diem` Nạp Qua Hàm Ôm Nối 5 Mệnh Lỗ Các Mảnh Ngẫu Trị Điểm Số. Cho Tính In Ra `mean()` Tổng Ngược Vector Bằng Điểm Cuối Gọi Kiểm Toán Chạy `summary()` Vét Dữ Độ Trải Phổ . 
- [ ] **Bài 2 (Trung bình Múa Thống Bảng `data.frame` Phím Mở Khóa Data Lớn):** Ôm Nặn Một Data Tượng (Với Khối Trường Lớp `Ten_SP`, `Gia`, `Da_Ban`) Lên Tựa Tạo Ít Nhất 3 Cụm. Kêu Khung Sạch Ra Chạy Dấu Đô la Chọn Khứ Chiết Xử Nhân Điểm Tổng Toán Số Lượng Thu Về Bằng Cây Toán Thực (Cho R Chỉ Chọi `Gia * Da_Ban` Làm Kết Mới Và Push Dấu Chữ Nhét Vô Khung).  

---

## Tài nguyên Đọc Sâu Vun Chắp Cánh Tầm Chuyên Làm Data Phân Tích Thực Tiễn Nghiệp

- [Quyển Thánh Kinh Vị Quán Tốt Nhất Mọi Dân Data Nhà Tidy R For Data Science](https://r4ds.had.co.nz/) - Được Tác Gỉả Gốc Xây Chứa Gói Của Ngành Xào Dữ R Viết Riêng Cho Sự Học Thành Data. Tráng Mức Dễ Và Thâm Đi Sâu .
- [Base Khóa R Cấp Chuẩn Tương Tác Nền Online Của Sàn Datacamp Lớn Nhất](https://www.datacamp.com/courses/free-introduction-to-r) - Giao Chạy Sát Viền Test Phim Chạm R Rõ Tiện Khởi Sân Đầu Cơ Web Lướt Lỗ Hiểu Kệnh Đất Xếp List R Tầng.
- [Xưởng Tra Bảng Vải Code Dựng Khối GGplot 2 (R Graph Gallery Sảnh Dữ Tưởng Tượng Tươi Mát)](https://r-graph-gallery.com/) - Kênh Gắn Đủ Snippet Copy Vẽ Tranh Khoa Hình Mạng Gốc Lướt 3 Phút Mảnh Data Dài Đăng Kết Rực Màu Ngỡ Quáng Nghề.
