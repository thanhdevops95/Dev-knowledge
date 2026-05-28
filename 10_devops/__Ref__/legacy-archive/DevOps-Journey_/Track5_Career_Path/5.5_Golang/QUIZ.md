# ❓ Quiz: Golang

> **Knowledge Check for Golang (5 Questions)**
>
> *Kiểm tra kiến thức Golang (5 câu hỏi).*

---

### Q1: Package Declaration

What is the entry point package name for a Go executable?

*(Tên package bắt đầu cho Go executable là gì?)*

- a) `package app`
- b) `package main`
- c) `package root`
- d) `package start`

---

### Q2: Variable Declaration

Which is a valid short variable declaration in Go?

*(Cách khai báo biến ngắn hợp lệ trong Go?)*

- a) `var name = "Go"`
- b) `name := "Go"`
- c) `let name = "Go"`
- d) Both a and b *(Cả a và b)*

---

### Q3: Error Handling

How does Go handle errors?

*(Go xử lý lỗi như thế nào?)*

- a) Try-catch blocks
- b) Exception throwing
- c) Return error as value *(Trả về error như giá trị)*
- d) Panic only

---

### Q4: Goroutines

What keyword starts a goroutine?

*(Từ khóa nào bắt đầu goroutine?)*

- a) `async`
- b) `go`
- c) `thread`
- d) `spawn`

---

### Q5: Build Output

What does `CGO_ENABLED=0 go build` do?

*(`CGO_ENABLED=0 go build` làm gì?)*

- a) Enable C libraries *(Bật thư viện C)*
- b) Create static binary *(Tạo binary tĩnh)*
- c) Optimize for speed *(Tối ưu tốc độ)*
- d) Enable debugging *(Bật debugging)*

---

## 📝 Answers

<details>
<summary>Click to view answers / Nhấn để xem đáp án</summary>

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | b | `package main` is required for executables |
| 2 | d | Both `var` and `:=` are valid |
| 3 | c | Go returns errors as values |
| 4 | b | `go func()` starts a goroutine |
| 5 | b | Disables CGO for static binary |

</details>

---

**[← Back to README](./README.md)**
