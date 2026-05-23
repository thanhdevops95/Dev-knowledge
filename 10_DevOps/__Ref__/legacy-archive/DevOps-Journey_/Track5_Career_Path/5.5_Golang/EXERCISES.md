# 💪 Exercises: Golang

> **Practice Exercises for Golang**
>
> *Bài tập thực hành Golang.*

---

## Exercise 1: Hello CLI (Beginner)

Create a CLI tool that:

*(Tạo công cụ CLI mà:)*

1. Accepts a name flag *(Nhận flag tên)*
2. Prints greeting *(In lời chào)*
3. Defaults to "World" *(Mặc định là "World")*

```bash
./hello --name DevOps
# Output: Hello, DevOps!
```

---

## Exercise 2: File Counter (Beginner)

Create a program that:

*(Tạo chương trình mà:)*

1. Counts files in a directory *(Đếm files trong thư mục)*
2. Reports by extension *(Báo cáo theo phần mở rộng)*
3. Outputs as JSON *(Xuất ra JSON)*

```json
{
  ".go": 5,
  ".md": 3,
  ".yaml": 2
}
```

---

## Exercise 3: Health Check Server (Intermediate)

Create an HTTP server with:

*(Tạo HTTP server với:)*

1. `/health` endpoint *(Endpoint health)*
2. `/ready` endpoint *(Endpoint ready)*
3. Metrics endpoint *(Endpoint metrics)*
4. Graceful shutdown *(Tắt máy graceful)*

---

## Exercise 4: System Info Tool (Intermediate)

Create a CLI that displays:

*(Tạo CLI hiển thị:)*

- OS information *(Thông tin OS)*
- CPU cores *(Số lõi CPU)*
- Memory usage *(Sử dụng bộ nhớ)*
- Disk space *(Dung lượng ổ đĩa)*

---

## Exercise 5: Config Parser (Advanced)

Create a tool that:

*(Tạo công cụ mà:)*

1. Reads YAML config *(Đọc config YAML)*
2. Validates required fields *(Xác thực các trường bắt buộc)*
3. Outputs as JSON *(Xuất ra JSON)*
4. Supports environment variable substitution *(Hỗ trợ thay thế biến môi trường)*

---

## ✅ Submission Checklist

- [ ] Code compiles without errors *(Code biên dịch không lỗi)*
- [ ] Tests pass *(Tests pass)*
- [ ] README with usage *(README có hướng dẫn sử dụng)*
- [ ] Dockerfile included *(Có Dockerfile)*

---

**[← Back to README](./README.md)**
