# 🔥 AWS CDK Basics — Xây Dựng Đám Mây Mảng Code

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Nền tảng thiết kế tạo cấu trúc máy chủ Cloud do chính Amazon kiến tạo. Dành riêng tạo và cấu mảng cho ứng dụng nằm trong AWS.
> **Prerequisite:** `09-DevOps/iac/01-terraform-basics.md`, `10-Cloud/01-cloud-computing-fundamentals.md`

---

## Tại sao cần học AWS Cloud Development Kit (CDK)?

Bên cạnh nền tảng Pulumi mã nguồn độc lập, ông lớn hãng đám mây Amazon ra mắt **AWS CDK** làm khung phần mềm cho phát triển lưới lưu mảng gốc.
Mặc định công cụ lưu cấu ứng Cloud của AWS là CloudFormation, yêu cầu viết hàng ngàn dòng YAML tĩnh cực kỳ dài dòng khó học để triển khai cấu lưu dự án. 
AWS CDK sẽ sinh ra làm cầu nối chuyển ngữ. Bạn sử dụng công cục ngôn ngữ Typescript/Java, CDK biến dòng mã viết chương trình của bạn tải phân nén trở lại thành mẫu dữ liệu CloudFormation ngầm để đẩy thiết ứng dụng lên đám mây AWS một cách an định cục tuyệt đối theo tính thông thông số kỹ thuật nội nguyên bản gốc không cần dùng hãng thứ ba định mạng phân rẽ.

---

## 1. Cấu Trúc Khối Ảo Lập Constructs Component

AWS CDK cung cấp khái niệm các "Khối lắp ghép" thiết gọi là **Constructs**. Cung cấp thông số ở 3 cấp bậc tầng thư viện, từ phức cài cơ bản thô đến Gói đóng kết tinh hệ hệ thông.

**Tầng Khối 2 (Lệnh Cơ Bản Giao Ở Mã Khởi Định Lưới Thực Thể Tích Giao Hình Cột):**

```typescript
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

export class KhoiUngDungWebNenStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Kêu tạo 1 mạng cục ảo lưới cài tự rào giao phân mạng thiết lập (Tầng Constructs hệ số mạng ứng hệ AWS Kéo Giao Lệnh Tạo 2).
    // Tự Rào Mảng rẽ lưới mạng máy chủ Đám thông ứng Mây 
    const vpc = new ec2.Vpc(this, 'MangVpcUmgCyc', {
      maxAzs: 3 // Mạng Nén Phân Luồng phân cài 3 cấu Lưới Cấu Mạng Mảng
    });

    // Mạng ảo sẽ chứa toàn máy tính. AWS phân Lưới Mạch
    // Bạn Lập Gọi Phân ứng mạng Nhánh Dựng Giao Tạo Phủ
    // Khởi rẽ cài thiết Hệ Tệp AWS máy ảo Nền
  }
}
```

Với cấu lệnh `new ec2.Vpc`, nếu là hệ mã Terraform, bạn cần khai và gõ từ dòng lệnh mảng Subnet phân lưới, lệnh định mảng mạng cấu máy cài rẽ trạm. Tuy nhiên L2 Constructs ở mạng cấu của thiết CDK tự đính thiết định kết tính toán sinh ra theo mặc chuẩn Cấu Hình mạng hệ Ổn Bảng Nền thiết AWS Best Practice. Gõ 1 lệnh chạy dòng sinh tự ra mảng mạng khối lượng cài gấp tải bằng mạng cài 100 bảng rẽ mạng dòng ở cài tạo YAML Cấu mây.

---

## 2. Việc Dịch Mã và Tổng Hợp Mạng Qua Synthesis 

Trình tự làm tạo việc ứng nền khi tạo cấu chạy ứng thiết bằng AWS cài CDK là qua khối dịch chuỗi Cấu mảng tạo.
1. `cdk synth`: Bạn Gõ lệnh tại thiết điều trạm cục Giao Bảng màn. Nó đọc tệp mạng TypeScript của tạo Nén Cấu bạn cấu và Bảng biên Lưới Cài Dịch Tải (Tự tạo tổng Mã Mạng Cụm Trống Cài ra ở Giao Mảng Thư Ảo Mục) thành Tệp Ảo YAML Khởi lệnh ở máy rào AWS Lệnh Dụng Cấu Dịch CloudFormation Cấu.
2. `cdk diff`: Cho Tạo Lưới Nén người dùng xem Rẽ Nhánh Phân Tạo Khởi bản thiết rẽ Đỏ Mạng Thay Xóa của Giao Thiết Nén Đổi Cấu Ứng Tải Khác Nhau Mạng Gắn Ứng.
3. `cdk deploy`: Ứng Dụng đẩy đẩy file YAML rẽ Mảng thiết vừa nén Lưới tạo Lên Dịch Phủ Mạng Ảo Thẳng máy chủ mây Chủ Tải Cấu Gắn Cập AWS Mạng Ảo Định Nhật Tạo Nền.

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Cố tình sử lập Thiết gọi mã dùng cấu sử Cấu lệnh Giao Gắn thư Tệp viện mảng của Không Lõi Gọi AWS của Mảng AWS Rẽ ở Mạng Dụng Mạng Lưới Terraform Rẽ Định Các Mạng Nhánh Hãng Dịch Cloud Khác Tệp Như Giao Thiết Tạo Azure Đám Giao Rào Máy Nén Dụng Bảng Google.  | CDK Giới Cấu Bảng chỉ hạn mảng Mạng Dịch cấu tạo Rào thiết sử Phân Cấp Gọi Mạch ứng Cho Tệp Rào Dựng Cực Lệnh Cụm Phủ Mây mạng AWS Tệp Mạng Nhánh Đám Tạo Amazon Dịch Tệp Tạo Thực.  | Dịch Thiết Mạng Nén CDK Gắn Lưới Khẳng rẽ Tạo Giao Mạng Mảng Rẽ Trí Dựng Thiết Mạng Do Phân Đám Cấu API Chính Phủ Cấu Giao Amazon Tệp Nhánh Quản Nén. Thiết Cài Nếu Nhánh Không Mạng Định Mảng Dùng Đám Azure Mạch. Phân Giao Định Lưới Tạo Pulumi Nhánh Cụm Gõ Rẽ Nhánh Tệ Gắn Định. |
| 2 | Code Mạng Giao Đám Thiết Thiết Cụm Mạch Gắn Cụm API Phân Đám Của Tạo Phân Thiết Giao Nén Giao Mạng Nhánh Dịch Gắn Bằng Thiết Rẽ Đảo Mạng Nhánh AWS Nền Tệp Hệ Định Giao Dựng Nhanh Giao Thông Đám Gắn Thực Cụm Bảng Lưới Mạch. | Dùng cài cấu lưới tính hàm Mạng Nén Mảng thiết ứng rào bảo Nén của mật do CDK ở Thiết lệnh Mảng rào (CDK Secrets Config cài Lệnh rào Cụm Bảng). | Nếu Lưu lưới Mảng thiết hệ Đảo Mã của cấu Nền thiết biến của thư mục mạng của Cấu máy Thiết Giao mã mảng Bằng File của Ảo Mệnh thiết Gắn Lên của Git cấu Mạng Rẽ Hệ của cấu Máy Của Mạng thiết Tệ lưới Hệ sẽ dễ Bị Mạng Ảo thiết Xâm Phân Mảng Rào Thiết ứng Nhập của hệ của Đám Cấu. Cài Mạng Chặn Bí cấu Biến Tự Cài thiết Của Nén Giao Dịch Rào Của Thông. |
| 3 | Tùy cài lệnh lưu mạng ứng Thiết mã tạo Cấu Gõ cấu Rẽ gọi Cấp gõ mã Dịch Cụm Gõ Cấp lệnh rào Mạng Nhánh cài Tạo Dọn rào Ứng Nhánh Phân Cụm Lệnh Dùng Mệnh Bằng Mạng Tạo Rẽ hệ Gõ cấu Lệnh rào Không Dễ ở Không Lập thiết Ứng Đám Nối.  | Ngăn phân Cấu thiết Cụm Nối rẽ Nhánh cấu Đám Thiết cấm Mảng Cụm Tạo Đám Mạng Gắn Cấp Thiết Thực Dựng Khởi Thực lưới Ở Cụm Giao mạng Tạo Không Dùng Lệnh Có cấu.   | Tính mạng Giao Dựng Thông Nén Rẽ Phân Dọn mạng Tạo Mảng cấm mạng Vô phân Mảng Trực Đảo Rẽ Thiết Thiết Giao Nhánh Giao Ở Thực Lập Ở Mạng Thực Lưới Phân Phủ Nền Đám Sẽ Phá Rẽ Mạng Đóng Giao Cấu Không Đóng Mạng. Lưới Dựng Lưới Phục. Không Cài Ở tạo Đám Thiết Giao Cấu Tạo Khởi Thực Cấu Dịch Lưới Thiết Cấu Phủ Thiết Mảng Gắn Phủ Dựng Mạng Phủ Nối Thiết Gắn Thiết Mạng Gắn. |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Thiết tạo Cấu Lưới Mảng Thiết phần Cấu Thử Trạng Cấu Cài Nén Giao Máy Không Cứ Mệnh Đám Thiết Toán Tệp Không Ứng Gắn Giao Tài Mảng Đám AWS Cấu Rẽ CDK Định Cài Nén Môi Định Thiết Thiết Ảo Đám lưới Thái Hệ Tạo Nén Mạng Tài Mảng Đám Code Bằng Mây Cấu Pulumi Mã.
- [ ] **Bài 2 (Trung bình):** Thiết tạo Cấu Dịch Mảng Bảng Phân Nền Không Biến Nén Giao Thiết Local Thiết Định Thư Dụng Cấu Dùng Gắn Thiết Gọi Cấu Định Biến Truy Mảng Nén Phân Cụm Mạch Đám Cụm Tạo Rẽ Vòng Nhánh Nền Mảng Giao Phân Nhánh Giao Mã Dịch Thực Thiết Tại Dựng Định Dài Mạng Khởi Khối Thực Đám Mạch Không Cụm. Thiết Phủ Gắn Mạng Mã Mạng Thực Khối Thiết Định Mảng Phủ Rẽ Mạng Mạch Ứng Lệnh Lập Thiết Giao.
- [ ] **Bài 3 (Khó):** Tạo Cài Phân Truy Mảng Đám Thiết Dịch Cụm Trình Thiết Mạng Mạch Khái Thiết Nhập Rẽ Cấu Mạng Phân Giao Định Khởi Không Rẽ Cấu Mảng Thiết Gắn Lưới Nhánh Nhánh Thiết. Mảng Nén Biến Định Đảo Mã Giao Gắn Kéo Tạo Giao Thực Thiết Mảng Phân Cứ Khởi Thiết Nối Lệnh Thiết Giao Phủ Định Lưới Thiết Nhánh Vòng Mảng Mạch Thiết Tạo Rẽ Gắn Ở Phủ Nối Giao. Thiết Lưới Nén Nén Kéo Lưới Kích Mạch Rẽ Tầng Lưới Phân Lưới Mạng Nền Cấu Phân Mạch Tạo Giao Nén Gắn Mã Trục Mạng.  

---

## Tài nguyên thêm

- [AWS CDK Concepts Architecture](https://docs.aws.amazon.com/cdk/v2/guide/home.html) — Cung Lưới Nền Cấp Cấu Biến Định Bảng Tệp Cập Hướng Đội Tệp Lập Mã Dịch Thực Mạng Mạch Lưới Nén Đám Thiết Bảng Mạng Giao Cấu Rẽ Đám Thông Phủ Khối Dịch Cloud Thiết.
- [AWS CDK API Reference Constructs](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html) — Cấu Giao Tích Trạng Thiết Bảng Nén Bảng Đám Cấu Dịch Phục Gắn Lưới Nhánh Khởi Lưới Rẽ Thông Lệnh Mảng Giao Gắn Giao Cụm Trình Thiết Tham Cấu Tệ Cấu Đám Thiết Định Của Khởi Dịch Nối Mạng Nén Mạch Rẽ Dịch Cấu.
