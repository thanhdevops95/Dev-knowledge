# GIAI ĐOẠN 4: THÊM NGINX - WEB INTERFACE

## 📌 MỤC TIÊU GIAI ĐOẠN 4
Sau khi hoàn thành giai đoạn này, bạn sẽ:

✅ Xây dựng giao diện web đẹp cho TODO App  
✅ Hiểu cách NGINX hoạt động như web server  
✅ Cấu hình NGINX làm reverse proxy  
✅ Tích hợp Frontend → NGINX → Python → Go  
✅ Xử lý CORS và static files  
✅ Có ứng dụng hoàn chỉnh user có thể dùng được

---

## 🗂️ PHẦN 1: TỔNG QUAN KIẾN TRÚC

### 1.1. Kiến trúc hiện tại (Giai đoạn 3)

```
User (curl/Postman) → Python API → Go Service
```

**Vấn đề:**

- Không có giao diện trực quan
- Chỉ developer mới dùng được
- Khó demo cho người khác

### 1.2. Kiến trúc mới (Giai đoạn 4)

```
┌─────────────────────────────────────────────┐
│           User (Browser)                     │
└─────────────────┬───────────────────────────┘
                  │ HTTP
         ┌────────▼────────┐
         │  NGINX :80      │
         │  - Static files │
         │  - Reverse Proxy│
         └────────┬────────┘
                  │
         ┌────────▼────────────────┐
         │                         │
    Static Files          /api/* requests
    (HTML/CSS/JS)                 │
         │                        │
         │               ┌────────▼────────┐
         │               │ Python :8080    │
         │               │ (Gateway)       │
         │               └────────┬────────┘
         │                        │
         │               ┌────────▼────────┐
         │               │ Go :8081        │
         │               │ (Backend)       │
         │               └─────────────────┘
         │
    ┌────▼─────┐
    │ Browser  │
    │ renders  │
    └──────────┘
```

**Giải thích luồng:**

1. User mở `http://localhost` → NGINX
2. NGINX serve `index.html`, `style.css`, `app.js`
3. Browser render giao diện
4. User click "Add TODO" → JavaScript gọi API
5. AJAX request → `http://localhost/api/todos`
6. NGINX proxy → Python (port 8080)
7. Python forward → Go (port 8081)
8. Response ngược → Go → Python → NGINX → Browser
9. JavaScript update DOM

---

## 🎨 PHẦN 2: XÂY DỰNG FRONTEND

### 2.1. Tạo cấu trúc thư mục

```bash
# Di chuyển về thư mục gốc
cd todo-app-devsecops

# Tạo cấu trúc frontend
mkdir -p frontend/css
mkdir -p frontend/js
mkdir -p frontend/images
```

**Cấu trúc:**
```
frontend/
├── index.html       ← Trang chính
├── css/
│   └── style.css    ← Styles
├── js/
│   └── app.js       ← Logic JavaScript
└── images/          ← Hình ảnh (nếu có)
```

### 2.2. Tạo index.html

Tạo file `frontend/index.html`:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TODO App - DevSecOps Learning</title>
    <link rel="stylesheet" href="/css/style.css">
    <!-- Font Awesome cho icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <h1><i class="fas fa-tasks"></i> TODO App</h1>
            <p class="subtitle">DevSecOps Learning Project</p>
        </div>
    </header>

    <!-- Main Container -->
    <main class="container">
        <!-- Stats Section -->
        <section class="stats-section">
            <div class="stat-card">
                <i class="fas fa-list"></i>
                <div class="stat-info">
                    <span class="stat-number" id="total-count">0</span>
                    <span class="stat-label">Tổng số</span>
                </div>
            </div>
            <div class="stat-card">
                <i class="fas fa-check-circle" style="color: #10b981;"></i>
                <div class="stat-info">
                    <span class="stat-number" id="completed-count">0</span>
                    <span class="stat-label">Hoàn thành</span>
                </div>
            </div>
            <div class="stat-card">
                <i class="fas fa-clock" style="color: #f59e0b;"></i>
                <div class="stat-info">
                    <span class="stat-number" id="pending-count">0</span>
                    <span class="stat-label">Đang làm</span>
                </div>
            </div>
            <div class="stat-card">
                <i class="fas fa-server" style="color: #6366f1;"></i>
                <div class="stat-info">
                    <span class="stat-number" id="ping-count">0</span>
                    <span class="stat-label">Ping Count</span>
                </div>
            </div>
        </section>

        <!-- Add TODO Form -->
        <section class="add-todo-section">
            <form id="add-todo-form" class="add-todo-form">
                <input 
                    type="text" 
                    id="todo-input" 
                    placeholder="Thêm công việc mới..." 
                    required
                    autocomplete="off"
                >
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-plus"></i> Thêm
                </button>
            </form>
        </section>

        <!-- Filter Tabs -->
        <section class="filter-section">
            <div class="filter-tabs">
                <button class="filter-tab active" data-filter="all">
                    <i class="fas fa-list"></i> Tất cả
                </button>
                <button class="filter-tab" data-filter="active">
                    <i class="fas fa-clock"></i> Đang làm
                </button>
                <button class="filter-tab" data-filter="completed">
                    <i class="fas fa-check-circle"></i> Hoàn thành
                </button>
            </div>
        </section>

        <!-- TODO List -->
        <section class="todo-list-section">
            <!-- Loading Spinner -->
            <div id="loading" class="loading" style="display: none;">
                <i class="fas fa-spinner fa-spin"></i> Đang tải...
            </div>

            <!-- Error Message -->
            <div id="error-message" class="error-message" style="display: none;"></div>

            <!-- Empty State -->
            <div id="empty-state" class="empty-state" style="display: none;">
                <i class="fas fa-inbox"></i>
                <p>Chưa có công việc nào</p>
                <small>Thêm công việc đầu tiên của bạn!</small>
            </div>

            <!-- TODO List -->
            <ul id="todo-list" class="todo-list"></ul>
        </section>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>
                <i class="fas fa-code"></i> 
                Made with <i class="fas fa-heart" style="color: #ef4444;"></i> 
                for DevSecOps Learning
            </p>
            <div class="service-status">
                <span class="status-indicator" id="service-status">
                    <i class="fas fa-circle"></i> Kiểm tra kết nối...
                </span>
            </div>
        </div>
    </footer>

    <!-- Edit Modal -->
    <div id="edit-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2><i class="fas fa-edit"></i> Chỉnh sửa công việc</h2>
                <button class="modal-close" id="modal-close">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <input 
                    type="text" 
                    id="edit-todo-input" 
                    placeholder="Nhập tiêu đề mới..."
                >
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" id="cancel-edit">Hủy</button>
                <button class="btn btn-primary" id="save-edit">
                    <i class="fas fa-save"></i> Lưu
                </button>
            </div>
        </div>
    </div>

    <!-- JavaScript -->
    <script src="/js/app.js"></script>
</body>
</html>
```

### 2.3. Tạo style.css

Tạo file `frontend/css/style.css`:

```css
/* ==================== RESET & BASE ==================== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    /* Colors */
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --secondary: #8b5cf6;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --info: #3b82f6;
    
    /* Grays */
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-300: #d1d5db;
    --gray-400: #9ca3af;
    --gray-500: #6b7280;
    --gray-600: #4b5563;
    --gray-700: #374151;
    --gray-800: #1f2937;
    --gray-900: #111827;
    
    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;
    
    /* Border Radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --radius-xl: 1rem;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: var(--gray-900);
    line-height: 1.6;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 var(--spacing-md);
}

/* ==================== HEADER ==================== */
.header {
    background: white;
    box-shadow: var(--shadow-md);
    padding: var(--spacing-xl) 0;
    margin-bottom: var(--spacing-2xl);
}

.header h1 {
    font-size: 2.5rem;
    color: var(--primary);
    margin-bottom: var(--spacing-sm);
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

.header h1 i {
    font-size: 2rem;
}

.subtitle {
    color: var(--gray-600);
    font-size: 1rem;
}

/* ==================== STATS SECTION ==================== */
.stats-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: var(--spacing-md);
    margin-bottom: var(--spacing-xl);
}

.stat-card {
    background: white;
    padding: var(--spacing-lg);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.stat-card i {
    font-size: 2rem;
    color: var(--primary);
}

.stat-info {
    display: flex;
    flex-direction: column;
}

.stat-number {
    font-size: 1.75rem;
    font-weight: bold;
    color: var(--gray-900);
    line-height: 1;
}

.stat-label {
    font-size: 0.875rem;
    color: var(--gray-600);
}

/* ==================== ADD TODO FORM ==================== */
.add-todo-section {
    margin-bottom: var(--spacing-xl);
}

.add-todo-form {
    display: flex;
    gap: var(--spacing-md);
    background: white;
    padding: var(--spacing-md);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

.add-todo-form input {
    flex: 1;
    padding: var(--spacing-md);
    border: 2px solid var(--gray-200);
    border-radius: var(--radius-md);
    font-size: 1rem;
    transition: border-color 0.2s;
}

.add-todo-form input:focus {
    outline: none;
    border-color: var(--primary);
}

.add-todo-form input::placeholder {
    color: var(--gray-400);
}

/* ==================== BUTTONS ==================== */
.btn {
    padding: var(--spacing-md) var(--spacing-lg);
    border: none;
    border-radius: var(--radius-md);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-sm);
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
}

.btn:active {
    transform: translateY(0);
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover {
    background: var(--primary-dark);
}

.btn-secondary {
    background: var(--gray-200);
    color: var(--gray-700);
}

.btn-secondary:hover {
    background: var(--gray-300);
}

.btn-success {
    background: var(--success);
    color: white;
}

.btn-danger {
    background: var(--danger);
    color: white;
}

.btn-sm {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: 0.875rem;
}

/* ==================== FILTER TABS ==================== */
.filter-section {
    margin-bottom: var(--spacing-lg);
}

.filter-tabs {
    display: flex;
    gap: var(--spacing-sm);
    background: white;
    padding: var(--spacing-sm);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

.filter-tab {
    flex: 1;
    padding: var(--spacing-md);
    background: transparent;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
    color: var(--gray-600);
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-sm);
}

.filter-tab:hover {
    background: var(--gray-100);
    color: var(--gray-900);
}

.filter-tab.active {
    background: var(--primary);
    color: white;
}

/* ==================== TODO LIST ==================== */
.todo-list-section {
    background: white;
    padding: var(--spacing-lg);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    min-height: 300px;
}

.todo-list {
    list-style: none;
}

.todo-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--gray-200);
    transition: background 0.2s;
}

.todo-item:last-child {
    border-bottom: none;
}

.todo-item:hover {
    background: var(--gray-50);
}

.todo-item.completed .todo-text {
    text-decoration: line-through;
    color: var(--gray-500);
}

.todo-checkbox {
    width: 24px;
    height: 24px;
    cursor: pointer;
}

.todo-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
}

.todo-text {
    font-size: 1.125rem;
    color: var(--gray-900);
    word-break: break-word;
}

.todo-meta {
    font-size: 0.75rem;
    color: var(--gray-500);
    display: flex;
    gap: var(--spacing-md);
}

.todo-actions {
    display: flex;
    gap: var(--spacing-sm);
}

.todo-actions button {
    padding: var(--spacing-sm) var(--spacing-md);
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 0.2s;
    font-size: 0.875rem;
}

.btn-edit {
    background: var(--info);
    color: white;
}

.btn-edit:hover {
    background: #2563eb;
}

.btn-delete {
    background: var(--danger);
    color: white;
}

.btn-delete:hover {
    background: #dc2626;
}

/* ==================== LOADING & STATES ==================== */
.loading {
    text-align: center;
    padding: var(--spacing-2xl);
    color: var(--gray-600);
    font-size: 1.125rem;
}

.loading i {
    font-size: 2rem;
    color: var(--primary);
}

.empty-state {
    text-align: center;
    padding: var(--spacing-2xl);
    color: var(--gray-500);
}

.empty-state i {
    font-size: 4rem;
    margin-bottom: var(--spacing-md);
    color: var(--gray-300);
}

.empty-state p {
    font-size: 1.25rem;
    margin-bottom: var(--spacing-sm);
}

.error-message {
    background: #fee2e2;
    border: 1px solid var(--danger);
    color: #991b1b;
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    margin-bottom: var(--spacing-md);
}

/* ==================== MODAL ==================== */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    align-items: center;
    justify-content: center;
}

.modal.active {
    display: flex;
}

.modal-content {
    background: white;
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-xl);
    max-width: 500px;
    width: 90%;
    max-height: 90vh;
    overflow: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-lg);
    border-bottom: 1px solid var(--gray-200);
}

.modal-header h2 {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    color: var(--gray-900);
}

.modal-close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--gray-600);
    padding: var(--spacing-sm);
    line-height: 1;
}

.modal-close:hover {
    color: var(--gray-900);
}

.modal-body {
    padding: var(--spacing-lg);
}

.modal-body input {
    width: 100%;
    padding: var(--spacing-md);
    border: 2px solid var(--gray-200);
    border-radius: var(--radius-md);
    font-size: 1rem;
}

.modal-body input:focus {
    outline: none;
    border-color: var(--primary);
}

.modal-footer {
    padding: var(--spacing-lg);
    border-top: 1px solid var(--gray-200);
    display: flex;
    justify-content: flex-end;
    gap: var(--spacing-md);
}

/* ==================== FOOTER ==================== */
.footer {
    background: white;
    margin-top: var(--spacing-2xl);
    padding: var(--spacing-xl) 0;
    text-align: center;
    box-shadow: var(--shadow-md);
}

.footer p {
    color: var(--gray-600);
    margin-bottom: var(--spacing-md);
}

.service-status {
    font-size: 0.875rem;
}

.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-md);
    background: var(--gray-100);
    border-radius: var(--radius-md);
}

.status-indicator.online {
    background: #d1fae5;
    color: #065f46;
}

.status-indicator.online i {
    color: var(--success);
}

.status-indicator.offline {
    background: #fee2e2;
    color: #991b1b;
}

.status-indicator.offline i {
    color: var(--danger);
}

/* ==================== ANIMATIONS ==================== */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.todo-item {
    animation: fadeIn 0.3s ease;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 768px) {
    .header h1 {
        font-size: 2rem;
    }
    
    .stats-section {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .filter-tabs {
        flex-direction: column;
    }
    
    .todo-item {
        flex-wrap: wrap;
    }
    
    .todo-actions {
        width: 100%;
        justify-content: flex-end;
    }
}
```

### 2.4. Tạo app.js

Tạo file `frontend/js/app.js`:

```javascript
// ==================== CONFIGURATION ====================
const API_BASE_URL = '/api'; // NGINX sẽ proxy /api/* sang Python

// ==================== STATE ====================
let todos = [];
let currentFilter = 'all'; // 'all', 'active', 'completed'
let editingTodoId = null;

// ==================== DOM ELEMENTS ====================
const elements = {
    todoList: document.getElementById('todo-list'),
    todoInput: document.getElementById('todo-input'),
    addTodoForm: document.getElementById('add-todo-form'),
    loading: document.getElementById('loading'),
    errorMessage: document.getElementById('error-message'),
    emptyState: document.getElementById('empty-state'),
    
    // Stats
    totalCount: document.getElementById('total-count'),
    completedCount: document.getElementById('completed-count'),
    pendingCount: document.getElementById('pending-count'),
    pingCount: document.getElementById('ping-count'),
    
    // Filters
    filterTabs: document.querySelectorAll('.filter-tab'),
    
    // Modal
    editModal: document.getElementById('edit-modal'),
    editTodoInput: document.getElementById('edit-todo-input'),
    modalClose: document.getElementById('modal-close'),
    cancelEdit: document.getElementById('cancel-edit'),
    saveEdit: document.getElementById('save-edit'),
    
    // Service status
    serviceStatus: document.getElementById('service-status')
};

// ==================== API FUNCTIONS ====================

/**
 * Generic fetch wrapper với error handling
 */
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        // Kiểm tra response
        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || `HTTP ${response.status}`);
        }
        
        // DELETE thường trả 204 No Content
        if (response.status === 204) {
            return { success: true };
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

/**
 * Lấy tất cả TODO
 */
async function fetchTodos() {
    const data = await apiCall('/todos');
    return data.data || [];
}

/**
 * Tạo TODO mới
 */
async function createTodo(title) {
    const data = await apiCall('/todos', {
        method: 'POST',
        body: JSON.stringify({ title })
    });
    return data.data;
}

/**
 * Cập nhật TODO
 */
async function updateTodo(id, updates) {
    const data = await apiCall(`/todos/${id}`, {
        method: 'PUT',
        body: JSON.stringify(updates)
    });
    return data.data;
}

/**
 * Xóa TODO
 */
async function deleteTodo(id) {
    await apiCall(`/todos/${id}`, {
        method: 'DELETE'
    });
}

/**
 * Lấy ping stats
 */
async function fetchStats() {
    try {
        const data = await apiCall('/stats');
        return data.data || { success_count: 0 };
    } catch (error) {
        return { success_count: 0 };
    }
}

/**
 * Test ping
 */
async function pingService() {
    try {
        await apiCall('/ping', { method: 'POST' });
        return true;
    } catch (error) {
        return false;
    }
}

// ==================== UI FUNCTIONS ====================

/**
 * Hiển thị loading
 */
function showLoading() {
    elements.loading.style.display = 'block';
    elements.todoList.style.display = 'none';
    elements.emptyState.style.display = 'none';
    elements.errorMessage.style.display = 'none';
}

/**
 * Ẩn loading
 */
function hideLoading() {
    elements.loading.style.display = 'none';
}

/**
 * Hiển thị error
 */
function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorMessage.style.display = 'block';
    setTimeout(() => {
        elements.errorMessage.style.display = 'none';
    }, 5000);
}

/**
 * Format timestamp
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    // Dưới 1 phút
    if (diff < 60000) {
        return 'Vừa xong';
    }
    
    // Dưới 1 giờ
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes} phút trước`;
    }
    
    // Dưới 1 ngày
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours} giờ trước`;
    }
    
    // Ngày cụ thể
    return date.toLocaleDateString('vi-VN');
}

/**
 * Render 1 TODO item
 */
function renderTodoItem(todo) {
    const li = document.createElement('li');
    li.className = `todo-item ${todo.completed ? 'completed' : ''}`;
    li.dataset.id = todo.id;
    
    li.innerHTML = `
        <input 
            type="checkbox" 
            class="todo-checkbox" 
            ${todo.completed ? 'checked'tiếp tục : ''}
data-id="${todo.id}"
>
<div class="todo-content">
<div class="todo-text">${escapeHtml(todo.title)}</div>
<div class="todo-meta">
<span><i class="fas fa-clock"></i> ${formatDate(todo.created_at)}</span>
${todo.completed ? '<span><i class="fas fa-check"></i> Hoàn thành</span>' : ''}
</div>
</div>
<div class="todo-actions">
<button class="btn-edit" data-id="${todo.id}">
<i class="fas fa-edit"></i> Sửa
</button>
<button class="btn-delete" data-id="${todo.id}">
<i class="fas fa-trash"></i> Xóa
</button>
</div>
`;
return li;
}
/**

Escape HTML để tránh XSS
*/
function escapeHtml(text) {
const div = document.createElement('div');
div.textContent = text;
return div.innerHTML;
}

/**

Filter todos theo trạng thái
*/
function getFilteredTodos() {
switch (currentFilter) {
case 'active':
return todos.filter(t => !t.completed);
case 'completed':
return todos.filter(t => t.completed);
default:
return todos;
}
}

/**

Render danh sách TODO
*/
function renderTodoList() {
const filteredTodos = getFilteredTodos();
// Clear list
elements.todoList.innerHTML = '';
// Kiểm tra empty
if (filteredTodos.length === 0) {
elements.todoList.style.display = 'none';
elements.emptyState.style.display = 'block';
return;
}
// Hiển thị list
elements.todoList.style.display = 'block';
elements.emptyState.style.display = 'none';
// Render items
filteredTodos.forEach(todo => {
const li = renderTodoItem(todo);
elements.todoList.appendChild(li);
});
// Update stats
updateStats();
}

/**

Update statistics
*/
function updateStats() {
const total = todos.length;
const completed = todos.filter(t => t.completed).length;
const pending = total - completed;
elements.totalCount.textContent = total;
elements.completedCount.textContent = completed;
elements.pendingCount.textContent = pending;
}

/**

Load todos từ server
*/
async function loadTodos() {
showLoading();
try {
todos = await fetchTodos();
renderTodoList();
} catch (error) {
showError('Không thể tải danh sách TODO. Vui lòng kiểm tra kết nối.');
console.error('Load todos error:', error);
} finally {
hideLoading();
}
}

/**

Load ping stats
*/
async function loadPingStats() {
try {
const stats = await fetchStats();
elements.pingCount.textContent = stats.success_count || 0;
} catch (error) {
console.error('Load stats error:', error);
}
}

/**

Check service status
*/
async function checkServiceStatus() {
const isOnline = await pingService();
const status = elements.serviceStatus;
if (isOnline) {
status.className = 'status-indicator online';
status.innerHTML = '<i class="fas fa-circle"></i> Dịch vụ hoạt động';
await loadPingStats();
} else {
status.className = 'status-indicator offline';
status.innerHTML = '<i class="fas fa-circle"></i> Mất kết nối';
}
}

// ==================== EVENT HANDLERS ====================
/**

Handle add TODO
*/
async function handleAddTodo(e) {
e.preventDefault();
const title = elements.todoInput.value.trim();
if (!title) return;
try {
const newTodo = await createTodo(title);
todos.push(newTodo);
renderTodoList();
elements.todoInput.value = '';
elements.todoInput.focus();
} catch (error) {
showError('Không thể thêm TODO. Vui lòng thử lại.');
console.error('Create todo error:', error);
}
}

/**

Handle toggle checkbox
*/
async function handleToggleTodo(id, completed) {
try {
const updatedTodo = await updateTodo(id, { completed: !completed });
const index = todos.findIndex(t => t.id === id);
if (index !== -1) {
todos[index] = updatedTodo;
renderTodoList();
}
} catch (error) {
showError('Không thể cập nhật TODO.');
console.error('Toggle todo error:', error);
}
}

/**

Handle edit TODO
*/
function handleEditClick(id) {
const todo = todos.find(t => t.id === id);
if (!todo) return;
editingTodoId = id;
elements.editTodoInput.value = todo.title;
elements.editModal.classList.add('active');
elements.editTodoInput.focus();
}

/**

Handle save edit
*/
async function handleSaveEdit() {
const newTitle = elements.editTodoInput.value.trim();
if (!newTitle || !editingTodoId) return;
try {
const updatedTodo = await updateTodo(editingTodoId, { title: newTitle });
const index = todos.findIndex(t => t.id === editingTodoId);
if (index !== -1) {
todos[index] = updatedTodo;
renderTodoList();
}
closeEditModal();
} catch (error) {
showError('Không thể cập nhật TODO.');
console.error('Update todo error:', error);
}
}

/**

Close edit modal
*/
function closeEditModal() {
elements.editModal.classList.remove('active');
editingTodoId = null;
elements.editTodoInput.value = '';
}

/**

Handle delete TODO
*/
async function handleDeleteTodo(id) {
if (!confirm('Bạn có chắc muốn xóa TODO này?')) return;
try {
await deleteTodo(id);
todos = todos.filter(t => t.id !== id);
renderTodoList();
} catch (error) {
showError('Không thể xóa TODO.');
console.error('Delete todo error:', error);
}
}

/**

Handle filter change
*/
function handleFilterChange(filter) {
currentFilter = filter;
// Update active tab
elements.filterTabs.forEach(tab => {
if (tab.dataset.filter === filter) {
tab.classList.add('active');
} else {
tab.classList.remove('active');
}
});
renderTodoList();
}

// ==================== EVENT LISTENERS ====================
// Form submit
elements.addTodoForm.addEventListener('submit', handleAddTodo);
// Todo list delegation
elements.todoList.addEventListener('click', (e) => {
const target = e.target;
// Checkbox toggle
if (target.classList.contains('todo-checkbox')) {
    const id = target.dataset.id;
    const todo = todos.find(t => t.id === id);
    if (todo) {
        handleToggleTodo(id, todo.completed);
    }
}

// Edit button
if (target.classList.contains('btn-edit') || target.parentElement.classList.contains('btn-edit')) {
    const btn = target.classList.contains('btn-edit') ? target : target.parentElement;
    handleEditClick(btn.dataset.id);
}

// Delete button
if (target.classList.contains('btn-delete') || target.parentElement.classList.contains('btn-delete')) {
    const btn = target.classList.contains('btn-delete') ? target : target.parentElement;
    handleDeleteTodo(btn.dataset.id);
}
});
// Filter tabs
elements.filterTabs.forEach(tab => {
tab.addEventListener('click', () => {
handleFilterChange(tab.dataset.filter);
});
});
// Modal events
elements.modalClose.addEventListener('click', closeEditModal);
elements.cancelEdit.addEventListener('click', closeEditModal);
elements.saveEdit.addEventListener('click', handleSaveEdit);
// Close modal khi click outside
elements.editModal.addEventListener('click', (e) => {
if (e.target === elements.editModal) {
closeEditModal();
}
});
// Enter key trong edit modal
elements.editTodoInput.addEventListener('keypress', (e) => {
if (e.key === 'Enter') {
handleSaveEdit();
}
});
// ==================== INITIALIZATION ====================
/**

Initialize app
*/
async function init() {
console.log('TODO App initializing...');
// Check service status
await checkServiceStatus();
// Load initial data
await loadTodos();
// Auto refresh ping stats mỗi 30s
setInterval(loadPingStats, 30000);
// Auto check service status mỗi 10s
setInterval(checkServiceStatus, 10000);
console.log('TODO App ready!');
}

// Start app khi DOM loaded
if (document.readyState === 'loading') {
document.addEventListener('DOMContentLoaded', init);
} else {
init();
}
```

---

## 🔧 PHẦN 3: CÀI ĐẶT VÀ CẤU HÌNH NGINX

### 3.1. Cài đặt NGINX

#### **Windows:**
```bash
# Tải NGINX
# Truy cập: http://nginx.org/en/download.html
# Tải phiên bản Windows (nginx-1.24.0.zip)

# Giải nén vào thư mục
# Ví dụ: C:\nginx
```

#### **macOS:**
```bash
# Cài qua Homebrew
brew install nginx

# Kiểm tra
nginx -v
```

#### **Linux (Ubuntu/Debian):**
```bash
# Cập nhật package list
sudo apt update

# Cài NGINX
sudo apt install nginx -y

# Kiểm tra
nginx -v

# Start NGINX
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 3.2. Tạo cấu hình NGINX cho TODO App

**Tạo thư mục nginx config:**
```bash
# Di chuyển về thư mục gốc
cd todo-app-devsecops

# Tạo thư mục nginx
mkdir nginx
```

**Tạo file `nginx/nginx.conf`:**
```nginx
# ==================== NGINX CONFIGURATION FOR TODO APP ====================

# Chạy NGINX với user hiện tại (development mode)
# Production nên dùng user nginx hoặc www-data
user nginx;

# Số worker processes (= số CPU cores)
worker_processes auto;

# Error log
error_log /var/log/nginx/error.log warn;

# PID file
pid /var/run/nginx.pid;

events {
    # Số connections mỗi worker có thể xử lý
    worker_connections 1024;
}

http {
    # ==================== MIME TYPES ====================
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # ==================== LOGGING ====================
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;

    # ==================== PERFORMANCE ====================
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # ==================== GZIP COMPRESSION ====================
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss;

    # ==================== SERVER BLOCK ====================
    server {
        listen 80;
        server_name localhost;

        # Root directory cho static files
        root /usr/share/nginx/html;
        index index.html;

        # ==================== STATIC FILES ====================
        # Serve HTML, CSS, JS từ frontend folder
        location / {
            try_files $uri $uri/ /index.html;
            
            # Cache static files
            location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
                expires 1y;
                add_header Cache-Control "public, immutable";
            }
        }

        # ==================== API PROXY ====================
        # Proxy tất cả /api/* requests sang Python service
        location /api/ {
            # Python service đang chạy trên port 8080
            proxy_pass http://localhost:8080;
            
            # Headers để preserve thông tin request gốc
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeout settings
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
            
            # Buffer settings
            proxy_buffering off;
            proxy_request_buffering off;
            
            # CORS headers (nếu cần)
            add_header Access-Control-Allow-Origin * always;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
            add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
            
            # Handle OPTIONS preflight
            if ($request_method = 'OPTIONS') {
                add_header Access-Control-Allow-Origin * always;
                add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
                add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
                add_header Content-Length 0;
                add_header Content-Type text/plain;
                return 204;
            }
        }

        # ==================== HEALTH CHECK ====================
        location /nginx-health {
            access_log off;
            return 200 "NGINX is healthy\n";
            add_header Content-Type text/plain;
        }

        # ==================== ERROR PAGES ====================
        error_page 404 /404.html;
        location = /404.html {
            internal;
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            internal;
        }
    }
}
```

### 3.3. Copy frontend files vào NGINX directory

#### **Linux/macOS:**
```bash
# Tạo symbolic link
sudo ln -s $(pwd)/frontend /usr/share/nginx/html

# Hoặc copy trực tiếp
sudo cp -r frontend/* /usr/share/nginx/html/
```

#### **Windows:**

**Nếu NGINX cài tại `C:\nginx`:**
```bash
# Copy frontend vào nginx html folder
xcopy /E /I frontend C:\nginx\html
```

### 3.4. Test cấu hình NGINX
```bash
# Linux/macOS
sudo nginx -t

# Windows (chạy từ thư mục nginx)
nginx.exe -t
```

**Output mong đợi:**
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

### 3.5. Chạy NGINX

#### **Linux/macOS:**
```bash
# Start NGINX
sudo systemctl start nginx

# Hoặc
sudo nginx

# Reload config (nếu đã chạy)
sudo systemctl reload nginx

# Hoặc
sudo nginx -s reload

# Kiểm tra status
sudo systemctl status nginx
```

#### **Windows:**
```bash
# Di chuyển vào thư mục NGINX
cd C:\nginx

# Start NGINX
start nginx.exe

# Reload (nếu thay đổi config)
nginx.exe -s reload

# Stop NGINX
nginx.exe -s stop
```

---

## 🧪 PHẦN 4: TEST TOÀN BỘ HỆ THỐNG

### 4.1. Checklist trước khi test

- [ ] Go service đang chạy (port 8081)
- [ ] Python service đang chạy (port 8080)
- [ ] NGINX đang chạy (port 80)
- [ ] Frontend files đã copy vào nginx/html

### 4.2. Test từng layer

**Test 1: NGINX Health Check**
```bash
curl http://localhost/nginx-health
```

**Kết quả:**
NGINX is healthy

**Test 2: Static Files**
```bash
# Mở browser
http://localhost

# Hoặc dùng curl
curl http://localhost
# Phải trả về HTML của index.html
```

**Test 3: API Proxy**
```bash
curl http://localhost/api/todos
```

**Kết quả:**
```json
{
  "count": 0,
  "data": [],
  "retrieved_at": "...",
  "status": "success"
}
```

### 4.3. Test giao diện web

1. **Mở browser:** `http://localhost`
2. **Kiểm tra giao diện hiển thị đúng**
3. **Thêm TODO mới:**
   - Nhập "Học Docker"
   - Click "Thêm"
   - TODO xuất hiện trong danh sách
4. **Đánh dấu hoàn thành:**
   - Click checkbox
   - TODO có gạch ngang
5. **Chỉnh sửa:**
   - Click "Sửa"
   - Modal hiện ra
   - Đổi tiêu đề → "Lưu"
6. **Xóa TODO:**
   - Click "Xóa"
   - Confirm → TODO biến mất
7. **Filter:**
   - Click "Đang làm" → Chỉ hiện TODO chưa xong
   - Click "Hoàn thành" → Chỉ hiện TODO đã xong
   - Click "Tất cả" → Hiện hết

### 4.4. Test luồng hoàn chỉnh
Browser → NGINX (port 80)
↓ GET /
NGINX serve index.html
↓
Browser render giao diện
↓ User click "Thêm TODO"
JavaScript → POST /api/todos
↓
NGINX proxy → Python (port 8080)
↓
Python forward → Go (port 8081)
↓
Go lưu vào RAM → trả response
↓
Response: Go → Python → NGINX → Browser
↓
JavaScript update DOM → TODO xuất hiện

---

## 🐛 PHẦN 5: XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi 1: NGINX không start

**Triệu chứng:**
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)

**Nguyên nhân:** Port 80 bị chiếm

**Giải pháp:**
```bash
# Linux/macOS - Tìm process
sudo lsof -i :80

# Kill process
sudo kill -9 [PID]

# Hoặc đổi port trong nginx.conf
listen 8000;  # Thay vì 80
```

### Lỗi 2: 502 Bad Gateway

**Triệu chứng:** Browser hiển thị "502 Bad Gateway"

**Nguyên nhân:** Python service không chạy hoặc sai port

**Kiểm tra:**
```bash
# Test Python có chạy không
curl http://localhost:8080/health

# Nếu không, start Python
cd python-service
python app.py
```

### Lỗi 3: Static files không load

**Triệu chứng:** Giao diện không có CSS, JavaScript không chạy

**Nguyên nhân:** Sai đường dẫn trong nginx.conf

**Kiểm tra:**
```bash
# Xem nginx log
sudo tail -f /var/log/nginx/error.log

# Kiểm tra file có tồn tại
ls -la /usr/share/nginx/html/
```

### Lỗi 4: CORS error

**Triệu chứng:** Console browser báo CORS policy error

**Giải pháp:** Đã được xử lý trong nginx.conf với:
```nginx
add_header Access-Control-Allow-Origin * always;
```

### Lỗi 5: API trả về HTML thay vì JSON

**Nguyên nhân:** NGINX đang serve static file thay vì proxy

**Kiểm tra nginx.conf:**
```nginx
# Đảm bảo location /api/ đứng TRƯỚC location /
location /api/ {
    proxy_pass http://localhost:8080;
}

location / {
    try_files $uri $uri/ /index.html;
}
```

---

## 🎯 PHẦN 6: BÀI TẬP THỰC HÀNH

### Bài 1: Thêm Due Date cho TODO

**Yêu cầu:**
1. Thêm field `due_date` vào TODO struct (Go)
2. Thêm input date trong form
3. Hiển thị due date trong danh sách
4. Highlight TODO quá hạn (màu đỏ)

### Bài 2: Thêm Dark Mode

**Yêu cầu:**
1. Thêm toggle button dark/light mode
2. Lưu preference vào localStorage
3. Apply dark theme CSS

**Gợi ý CSS:**
```css
body.dark-mode {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
}

.dark-mode .todo-item {
    background: #1f2937;
    color: #f3f4f6;
}
```

### Bài 3: Thêm Search

**Yêu cầu:**
1. Thêm search box
2. Filter TODO theo title real-time
3. Highlight từ khóa tìm kiếm

### Bài 4: Export/Import JSON

**Yêu cầu:**
1. Button "Export" → download todos.json
2. Button "Import" → upload JSON file
3. Parse và bulk create TODOs

---

## ✅ PHẦN 7: CHECKLIST HOÀN THÀNH GIAI ĐOẠN 4

- [ ] NGINX đã cài đặt và chạy được
- [ ] Frontend files đã copy vào nginx directory
- [ ] Giao diện web hiển thị đúng
- [ ] Có thể thêm TODO qua giao diện
- [ ] Có thể đánh dấu hoàn thành
- [ ] Có thể chỉnh sửa TODO
- [ ] Có thể xóa TODO
- [ ] Filter hoạt động (All/Active/Completed)
- [ ] Stats hiển thị đúng
- [ ] Service status hiển thị đúng
- [ ] Responsive trên mobile
- [ ] Không có lỗi CORS
- [ ] Hiểu được vai trò của NGINX (web server + reverse proxy)
- [ ] Hiểu được luồng: Browser → NGINX → Python → Go

---

## 📚 PHẦN 8: TÀI LIỆU THAM KHẢO

### NGINX:
- Official docs: https://nginx.org/en/docs/
- Reverse proxy: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/
- Configuration: https://www.nginx.com/resources/wiki/start/topics/examples/full/

### Frontend:
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- DOM Manipulation: https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model
- CSS Grid: https://css-tricks.com/snippets/css/complete-guide-grid/

---

## 🎊 KẾT LUẬN GIAI ĐOẠN 4

Chúc mừng! Bạn đã hoàn thành Giai đoạn 4 - TODO App với giao diện web hoàn chỉnh!

**Đã đạt được:**
✅ Giao diện web đẹp, responsive  
✅ NGINX làm web server + reverse proxy  
✅ Full CRUD operations qua UI  
✅ Real-time stats  
✅ Service health monitoring  
✅ Professional UX/UI  

**Vấn đề cần giải quyết tiếp:**
❌ Dữ liệu vẫn lưu RAM (mất khi restart)  
❌ Chưa containerize (Docker)  
❌ Deploy thủ công (chưa có CI/CD)  
❌ Chưa có monitoring