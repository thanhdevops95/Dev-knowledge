# GIAI ĐOẠN 5: NGINX & WEB INTERFACE - TRẢI NGHIỆM NGƯỜI DÙNG

## 📌 MỤC TIÊU GIAI ĐOẠN 5
Người dùng cuối không biết dùng `curl`. Họ cần giao diện Web.
Chúng ta sẽ dựng một **Web Server (NGINX)** đóng vai trò:
1. **Web Server**: Trả về các file tĩnh (HTML, CSS, JS).
2. **Reverse Proxy**: Điều hướng các request `/api` sang Python Gateway.

---

## 🎨 PHẦN 1: CODE FRONTEND (HTML/CSS/JS)

Hãy copy nội dung dưới đây vào các file tương ứng trong thư mục `frontend/`.

### 1. `frontend/index.html`
*(File giao diện chính)*
```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevSecOps Todo App</title>
    <link rel="stylesheet" href="css/style.css">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <header>
            <h1><i class="fas fa-check-double"></i> Todo Application</h1>
            <p>DevOps Zero to Hero Learning Path</p>
        </header>

        <section class="input-section">
            <input type="text" id="todo-input" placeholder="Bạn muốn làm gì hôm nay?">
            <button id="add-btn"><i class="fas fa-plus"></i> Thêm</button>
        </section>

        <section class="list-section">
            <ul id="todo-list">
                <!-- Javascript sẽ rải data vào đây -->
            </ul>
        </section>

        <footer>
            <p id="status-text">Đang kết nối...</p>
        </footer>
    </div>
    <script src="js/app.js"></script>
</body>
</html>
```

### 2. `frontend/css/style.css`
*(Trang trí cho đẹp)*
```css
:root {
    --primary: #6366f1;
    --bg: #f3f4f6;
    --text: #1f2937;
}

body {
    font-family: 'Segoe UI', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    justify-content: center;
    padding-top: 50px;
}

.container {
    background: white;
    width: 400px;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
}

header h1 { color: var(--primary); text-align: center; }
header p { text-align: center; color: #6b7280; font-size: 0.9rem; }

.input-section {
    display: flex;
    gap: 10px;
    margin: 20px 0;
}

input {
    flex: 1;
    padding: 10px;
    border: 2px solid #e5e7eb;
    border-radius: 0.5rem;
    outline: none;
}

input:focus { border-color: var(--primary); }

button {
    background: var(--primary);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: 0.2s;
}

button:hover { opacity: 0.9; }

.list-section ul { list-style: none; padding: 0; }

.todo-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #f3f4f6;
    animation: fadeIn 0.3s ease;
}

.todo-item.completed span {
    text-decoration: line-through;
    color: #9ca3af;
}

.delete-btn {
    background: #ef4444;
    padding: 5px 10px;
    font-size: 0.8rem;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
```

### 3. `frontend/js/app.js`
*(Logic gọi API - Lưu ý gọi vào /api/todos)*
```javascript
const API_URL = '/api/todos'; // Gọi qua NGINX Proxy (cùng domain)

document.addEventListener('DOMContentLoaded', () => {
    fetchTodos();
    document.getElementById('add-btn').addEventListener('click', addTodo);
});

async function fetchTodos() {
    try {
        const res = await fetch(API_URL);
        const data = await res.json();
        renderList(data);
        document.getElementById('status-text').innerText = 'System Healthy ✅';
        document.getElementById('status-text').style.color = 'green';
    } catch (e) {
        console.error(e);
        document.getElementById('status-text').innerText = 'Connection Lost ❌';
        document.getElementById('status-text').style.color = 'red';
    }
}

async function addTodo() {
    const input = document.getElementById('todo-input');
    const title = input.value.trim();
    if (!title) return;

    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title })
    });
    
    input.value = '';
    fetchTodos();
}

async function deleteTodo(id) {
    if(!confirm('Xóa nhé?')) return;
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    fetchTodos();
}

function renderList(todos) {
    const list = document.getElementById('todo-list');
    list.innerHTML = '';
    
    if (!todos) return;

    todos.forEach(todo => {
        const li = document.createElement('li');
        li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
        li.innerHTML = `
            <span>${todo.title}</span>
            <button class="delete-btn" onclick="deleteTodo('${todo.id}')">
                <i class="fas fa-trash"></i>
            </button>
        `;
        list.appendChild(li);
    });
}
```

---

## ⚙️ PHẦN 2: CẤU HÌNH NGINX

Tạo file `nginx/conf.d/default.conf`. Đây là file cấu hình bảo NGINX phải làm gì.

```nginx
server {
    listen 80;
    server_name localhost;

    # 1. Phục vụ Frontend (File tĩnh)
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    # 2. Reverse Proxy cho API
    # Mọi request bắt đầu bằng /api/ sẽ được chuyển sang container Gateway
    location /api/ {
        # 'gateway' là tên service trong docker-compose
        # Port 8080 là port nội bộ của Python Flask
        proxy_pass http://gateway:8080;
        
        # Các header cần thiết để forward
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📦 PHẦN 3: CẬP NHẬT DOCKER COMPOSE

Sửa file `docker-compose.yaml` để thêm service NGINX.

```yaml
version: '3.8'

services:
  backend:
    container_name: go-app
    image: todo-go:v2
    volumes:
      - ./data:/app/data
    networks:
      - app-network
    restart: always

  gateway:
    container_name: python-app
    image: todo-python:v1
    environment:
      - GO_HOST=backend
    depends_on:
      - backend
    networks:
      - app-network

  # --- Service Mới: Web Server ---
  web:
    image: nginx:alpine
    container_name: todo-web
    ports:
      - "80:80"             # Cổng 80 - Web mặc định
    volumes:
      # Mount code frontend vào thư mục mặc định của Nginx
      - ./frontend:/usr/share/nginx/html
      # Mount file config
      - ./nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - gateway
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

*Lưu ý: Ta đã bỏ mapping port `5000:8080` của gateway vì giờ người dùng không được gọi trực tiếp Gateway nữa. Mọi thứ phải đi qua NGINX (Port 80).*

---

## 🚀 PHẦN 4: DEPLOY & TẬN HƯỞNG

### 1. Khởi chạy
```bash
docker compose up -d
```

### 2. Kiểm tra
Mở trình duyệt truy cập: `http://localhost` (Không cần :port gì cả vì 80 là mặc định).

Bạn sẽ thấy giao diện Web xinh đẹp.
- Thử thêm Todo -> JS gọi `/api/todos`.
- Nginx bắt `/api/` -> Chuyền cho Python Gateway.
- Python Gateway -> Chuyền cho Go Backend.
- Go Backend -> Ghi xuống File JSON.

Tất cả hoạt động nhịp nhàng! 🎉

---

## 📝 TỔNG KẾT
Bạn đã hoàn thành mô hình **3-Tier Architecture** kinh điển:
1. **Presentation Layer**: Nginx + HTML/JS
2. **Logic Layer**: Python Gateway
3. **Data Layer**: Go Backend + Filesystem

👉 **Bước tiếp theo:** Dùng File JSON (Flat file) không thể chịu tải cao và gặp lỗi race condition. Giai đoạn 6 chúng ta sẽ nâng cấp lên **Database thực thụ (MySQL)**.
