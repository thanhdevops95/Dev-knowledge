# 🟨 javascript-dom — Thêm tương tác cho trang web

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 07/06/2026\
> **Trạng thái:** ✅ Cụm Basic hoàn chỉnh (5/5 bài)

> 🎯 *Cụm thứ hai của frontend, nối tiếp HTML/CSS. JavaScript là ngôn ngữ duy nhất chạy native trong trình duyệt — nó biến trang web tĩnh thành ứng dụng có tương tác: click, validate form, gọi API, cập nhật giao diện. Học xong, bạn nắm cú pháp JS cốt lõi, điều khiển được DOM, xử lý sự kiện và bất đồng bộ (async), gọi được backend — sẵn sàng bước sang React.*

---

## 🚀 Bắt đầu nhanh

Bạn đang cần gì? Chọn nhanh rồi nhảy thẳng vào bài:

- **JavaScript là gì, chạy ở đâu?** → [JavaScript là gì?](lessons/01_basic/00_what-is-javascript.md).
- **Cú pháp cốt lõi (biến, hàm, kiểu)?** → [Variables, Functions, Types](lessons/01_basic/01_variables-functions-types.md).
- **Dùng JS đổi nội dung HTML?** → [DOM Manipulation](lessons/01_basic/02_dom-manipulation.md).
- **Xử lý click + Promise + async/await?** → [Events & Async](lessons/01_basic/03_events-and-async.md).
- **Gọi backend bằng fetch + tách code module?** → [Fetch API & ES Modules](lessons/01_basic/04_fetch-and-modules.md).

---

## 📂 Cấu trúc cụm

```
javascript-dom/
├── README.md                          ← (file này)
└── lessons/
    └── 01_basic/                      ← ✅ 5/5 bài hoàn chỉnh
        ├── 00_what-is-javascript.md
        ├── 01_variables-functions-types.md
        ├── 02_dom-manipulation.md
        ├── 03_events-and-async.md
        └── 04_fetch-and-modules.md
```

---

## 📖 Lessons — Cụm Basic (5 bài)

Năm bài đi theo trình tự thêm "sự sống" cho trang HTML/CSS: hiểu JS là gì, nắm cú pháp nền, điều khiển DOM, bắt sự kiện và xử lý bất đồng bộ, rồi gọi API thật + tổ chức code thành module.

| # | Bài | Trọng tâm | Tag |
|---|---|---|---|
| 00 | [JavaScript là gì?](lessons/01_basic/00_what-is-javascript.md) | Vai trò JS trong browser, cách chạy, JS engine | MUST-KNOW |
| 01 | [Variables, Functions, Types](lessons/01_basic/01_variables-functions-types.md) | `let`/`const`, hàm, kiểu dữ liệu, scope | MUST-KNOW |
| 02 | [DOM Manipulation](lessons/01_basic/02_dom-manipulation.md) | Truy vấn + sửa DOM, tạo/xoá phần tử | MUST-KNOW |
| 03 | [Events & Async](lessons/01_basic/03_events-and-async.md) | Event listener, Promise, async/await | MUST-KNOW |
| 04 | [Fetch API & ES Modules](lessons/01_basic/04_fetch-and-modules.md) | `fetch` gọi backend, import/export module | MUST-KNOW |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Cụm trước:** [HTML & CSS là gì? — Nền tảng frontend web](../html-css/lessons/01_basic/00_what-is-html-and-css.md)
- ➡️ **Cụm sau:** [React là gì?](../react/lessons/01_basic/00_what-is-react.md)
- ↑ **Về nhóm:** [frontend](../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- 🎨 [html-css](../html-css/) — khung xương + style mà JS sẽ điều khiển
- ⚛️ [react](../react/) — khi UI phức tạp, chuyển từ DOM thủ công sang component
- 🐍 [FastAPI backend](../../backend/python-fastapi/) — backend mà `fetch` sẽ gọi

### 🌐 Tài nguyên tham khảo khác

- 📖 [MDN — JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- 📖 [javascript.info](https://javascript.info/) — tutorial hiện đại, sâu
- 📖 [MDN — Document Object Model (DOM)](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model)
- 📖 [MDN — Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (23/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (07/06/2026)** — Viết README hoàn chỉnh cho cụm Basic 5/5 bài (cụm đã có nội dung từ trước nhưng README còn skeleton): mục tiêu, bắt đầu nhanh, bảng danh mục bài, mục Liên kết chuẩn 3 sub.
