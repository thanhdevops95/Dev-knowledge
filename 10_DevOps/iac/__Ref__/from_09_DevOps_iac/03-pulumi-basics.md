# 🔥 Pulumi Basics — Ngôn Ngữ Hình Thành Đám Mây Mới

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Khi việc sử dụng ngôn ngữ học thuật như HCL làm quá sức với lập trình viên dự án, hãy sử dụng lại TypeScript hoặc Python để xây dựng mã kiểm soát kết nối điện toán đám mây với cơ sở mảng hạ tầng.
> **Prerequisite:** `09-DevOps/iac/01-terraform-basics.md`, `05-Languages/03-typescript-basics.md`

---

## Tại sao cần học sử dụng nền tảng Pulumi?

Mặc dù Terraform đang làm vương làm bá trên không gian thiết lập dữ liệu nền tảng đám mây quản lý qua mã chữ tĩnh. Tuy nhiên, nếu bạn xây dựng máy chủ thiết đặt mà muốn gắn thêm các hệ lập trình điều kiện lọc và vòng lặp phức tạp, Terraform HCL thiết kế bị giới hạn về tính năng thao tác xử lý vì nó không phải gốc ngôn ngữ lập trình đa luồng (Turing Complete Language).

**Pulumi** là nền tảng giải quyết điểm giới hạn bằng cách cho phép bạn có thể sử dụng nguyên mẫu TypeScript, Python, Golang hoặc C# để viết ra các điều kiện xây máy thực tại. Bằng việc tận dụng tính hệ vòng lặp có sẵn của mạng ứng dụng phần mềm quen thuộc (ví dụ vòng dòng `for` trong Typescript), Pulumi sẽ dịch các cụm mã tạo phần mềm từ chữ thành kết xuất yêu cầu HTTP để lập tức liên hệ định tuyến tạo máy chủ giống cách Terraform định hình. 

---

## 1. Cú trúc tạo ứng dụng Cloud qua TypeScript

Điểm nổi bật khi sử dụng TypeScript thay cho mã HCL (Terraform) là lập trình viên có thể ứng dụng chức năng báo lỗi trực tiếp từ IDE, tận dụng chức năng khai báo biến rõ ràng của giao diện công cụ thiết kế.

```typescript
import * as aws from "@pulumi/aws";

// Lập trình định tuyến biến vòng theo chuẩn kỹ thuật phần mềm mạng
const sizes = ["t2.micro", "t3.small"];

for (let i = 0; i < sizes.length; i++) {
    // Sự tự do trong mảng kết hệ ngôn ngữ máy chủ gọi biến tham gia lệnh thiết kế Cloud
    const server = new aws.ec2.Instance(`ung-dung-khoi-may-web-${i}`, {
        ami: "ami-0c55b159cbfafe1f0", 
        instanceType: sizes[i], // Thêm biến mảng linh động ở cấu chữ gốc
        tags: {
            Name: `Server-Nhom-Trang-Chu-${i}`,
            Hethong: "Pulumi_TS"
        },
    });

    // Hàm xuất khóa giao thông số mã tự do ở Console màn của Bash máy
    export const serverIp = server.publicIp;
}
```
Lập trình cho điện toán hạ tầng nhưng cách ghi câu chữ không khác gì viết mã Frontend chạy nền React ứng dụng giao thoa thư viện vòng mảng!

---

## 2. Hệ Tự Quản Lí Vận Hành Lõi Đồng Bộ Phân Tính Trạng Thái

Pulumi giống như Terraform, bắt buộc phải sử dụng mã Trạng thái tệp (State) lưu nhớ dữ liệu thiết lập để kết nối phân cách với dữ liệu ứng Cloud bên ngoài. Điểm khác là ở mặc định, khi bạn cài tải, phần tệp thư viện trạng thái này không bị thả ở địa phương cục bộ (Local ổ máy).

Pulumi cho bạn một hệ Website đồ họa giao diện tại bảng điều khiển gọi là nền (Pulumi Service). Ở giao diện này, nó giúp người chạy lệnh phân cấp lưu đồng bộ mã khóa tệp và theo dõi hệ biểu đồ máy nén đang bị thêm bớt rõ rệt từ máy giao mạng (Hoàn toàn miễn phí mức cơ bản). Chặn đi khuyết điểm lộ lưu trạng lưu mảng bảo mật ở hệ tệp cấu hình.

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Thực sử dụng ứng tạo thao thiết thi cài lệnh gọi lấy tệp mạng ứng thông số lấy mảng từ bên mạng lưới Cloud ngoài mảng trong qua các thư viện lập trình không thuộc chuỗi bất đồng bộ của ứng Pulumi nền.  | Bắt Dùng Cấu mảng tạo ứng lệnh sử thao gọi mảng gốc của Pulumi có tính hàm Promise chạy ở lệnh tham hoặc hàm nội lấy áp mạng `apply`.  | Không Giống như ngôn ngữ Lập Trình ứng chạy mảng Nhanh ở hàm biến. Tính lưới cấu mạng hàm khai tải Cloud của các loại lệnh gọi API tạo ứng rào thiết phải chờ trạm chạy mạng nén cấu máy nên tốn ứng Rào ứng Cài gian của hàm mạng đợi Tới ứng. Rẻ tạo Rào máy Chờ Gọi lệnh Nối API tạo Gọi Trái Lệnh Mạng Mảng. |
| 2 | Mở Thiết Gọi Gắn thông số mảng của Khối API mã Key truy AWS trên tệp cấu Mảng thiết hệ qua mạng bộ file Biến cấu mã `.env` cục Thiết rào máy tải thư tay Mảng cấu. | Dùng cài cấu lưới tính hàm Mạng Nén Mảng thiết ứng rào bảo Nén của mật do Pulumi ở Thiết lệnh Mảng rào (Pulumi Secrets Config cài Lệnh rào `pulumi config set --secret aws_khoa_mat`). | Nếu Lưu lưới Mảng thiết hệ Đảo Mã của cấu Nền thiết biến của thư mục mạng của Cấu máy Thiết Giao mã mảng Bằng File của Ảo Mệnh thiết Gắn Lên của Git cấu Mạng Rẽ Hệ của cấu Máy Của Mạng thiết Tệ lưới Hệ sẽ dễ Bị Mạng Ảo thiết Xâm Phân Mảng Rào Thiết ứng Nhập của hệ của Đám Cấu. Cài Mạng Chặn Bí cấu Biến Tự Cài thiết Của Nén Giao Dịch Rào Của Thông. |
| 3 | Tùy cài lệnh lưu mạng ứng Thiết mã tạo Cấu Gõ cấu Rẽ gọi Cấp gõ mã Dịch Cụm Gõ Cấp lệnh rào Mạng Nhánh cài Tạo Dọn rào Ứng Nhánh Phân Cụm Lệnh Dùng Mệnh Bằng Mạng Tạo Rẽ hệ Gõ cấu Lệnh rào Không Dễ ở Không Lập thiết Ứng Đám Nối.  | Ngăn phân Cấu thiết Cụm Nối rẽ Nhánh cấu Đám Thiết cấm Mảng Cụm Tạo Đám Mạng Gắn Cấp Thiết Thực Dựng Khởi Thực lưới Ở Cụm Giao mạng Tạo Không Dùng Lệnh Có cấu.   | Tính mạng Giao Dựng Thông Nén Rẽ Phân Dọn mạng Tạo Mảng cấm mạng Vô phân Mảng Trực Đảo Rẽ Thiết Thiết Giao Nhánh Giao Ở Thực Lập Ở Mạng Thực Lưới Phân Phủ Nền Đám Sẽ Phá Rẽ Mạng Đóng Giao Cấu Không Đóng Mạng. Lưới Dựng Lưới Phục. Không Cài Ở tạo Đám Thiết Giao Cấu Tạo Khởi Thực Cấu Dịch Lưới Thiết Cấu Phủ Thiết Mảng Gắn Phủ Dựng Mạng Phủ Nối Thiết Gắn Thiết Mạng Gắn. |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Thiết tạo Cấu Lưới Mảng Thiết phần Cấu Thử Trạng Cấu Cài Nén Giao Máy Không Cứ Mệnh Đám Thiết Toán Tệp Không Ứng Gắn Giao Tài Mảng Đám AWS Cấu Rẽ Pulumi Định Cài Nén Môi Định Thiết Thiết Ảo Đám lưới Thái Hệ Tạo Nén Mạng Tài API Mảng Đám Code Bằng Mây Cấu Pulumi Mã.
- [ ] **Bài 2 (Trung bình):** Thiết tạo Cấu Dịch Mảng Bảng Phân Nền Không Biến Nén Giao Thiết Local Thiết Định Thư Dụng Cấu Dùng Gắn Thiết Gọi Cấu Định Biến Truy Mảng Nén Phân Cụm Mạch Đám Cụm Tạo Rẽ Vòng Nhánh Nền Mảng Giao Phân Nhánh Giao Mã Dịch Thực Thiết Tại Dựng Định Dài Mạng Khởi Khối Thực Đám Mạch Không Cụm. Thiết Phủ Gắn Mạng Mã Mạng Thực Khối Thiết Định Mảng Phủ Rẽ Mạng Mạch Ứng Lệnh Lập Thiết Giao.
- [ ] **Bài 3 (Khó):** Tạo Cài Phân Truy Mảng Đám Thiết Dịch Cụm Trình Thiết Mạng Mạch Khái Thiết Nhập Rẽ Cấu Mạng Phân Giao Định Khởi Không Rẽ Cấu Mảng Thiết Gắn Pulumi Lưới Nhánh Nhánh Thiết. Mảng Nén Biến Định Đảo Mã Giao Gắn Kéo Tạo Giao Thực Thiết Mảng Phân Cứ Khởi Thiết Nối Lệnh Thiết Giao Phủ Định Lưới Thiết Nhánh Vòng Mảng Mạch Thiết Tạo Rẽ Gắn Ở Phủ Nối Giao. Thiết Lưới Nén Nén Kéo Lưới Kích Mạch Rẽ Tầng Lưới Phân Lưới Mạng Nền Cấu Phân Mạch Tạo Giao Nén Gắn Mã Trục Mạng.  

---

## Tài nguyên thêm

- [Pulumi Architecture](https://www.pulumi.com/docs/) — Cung Lưới Nền Cấp Cấu Biến Định Bảng Tệp Cập Hướng Đội Tệp Lập Mã Dịch Thực Mạng Mạch Lưới Nén Đám Thiết Bảng Mạng Giao Sách Phân Cấu Rẽ Đám Thông Phủ Khối Dịch Cloud Thiết.
- [Why choose Pulumi vs Terraform](https://www.pulumi.com/docs/concepts/vs/terraform/) — Cấu Giao Tích Trạng Thiết Bảng Nén Bảng Đám Cấu Dịch Phục Gắn Lưới Nhánh Khởi Lưới Rẽ Thông Lệnh Mảng Giao Gắn Giao Cụm Trình Thiết Tham Cấu Tệ Cấu Đám Thiết Định Của Khởi Dịch Nối Mạng Nén Mạch Rẽ Dịch Cấu.
