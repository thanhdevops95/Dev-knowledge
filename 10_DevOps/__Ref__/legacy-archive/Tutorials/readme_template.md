# Hướng dẫn Viết README

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Tổng hợp các template README.md cho các loại dự án khác nhau.

---

## 📦**TEMPLATE: DỰ ÁN CHUNG**

```markdown
# Tên Dự Án

Mô tả ngắn gọn về dự án này làm gì.

## ✨ Tính năng

- Tính năng 1
- Tính năng 2
- Tính năng 3

## 📋 Yêu cầu

- Python 3.8+
- Thư viện xyz

## 🚀 Cài đặt

\`\`\`bash
git clone https://github.com/username/project.git
cd project
pip install -r requirements.txt
\`\`\`

## 💻 Sử dụng

\`\`\`bash
python main.py
\`\`\`

## 📖 Ví dụ

\`\`\`python
from mypackage import something

result = something.do_work()
print(result)
\`\`\`

## 🤝 Đóng góp

1. Fork dự án
2. Tạo branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📝 License

MIT License - Xem file [LICENSE](LICENSE)

## 📧 Liên hệ

- Author: Tên bạn
- Email: email@example.com
- GitHub: [@username](https://github.com/username)
```

---

## 🐍**TEMPLATE: DỰ ÁN PYTHON**

```markdown
# My Python App

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Mô tả dự án...

## 📋 Yêu cầu hệ thống

- Python 3.8 trở lên
- pip (Python package manager)

## 🔧 Cài đặt

### Bước 1: Clone repository

\`\`\`bash
git clone https://github.com/username/my-python-app.git
cd my-python-app
\`\`\`

### Bước 2: Tạo môi trường ảo

\`\`\`bash
python -m venv venv

# Windows
.\venv\Scripts\Activate

# macOS/Linux
source venv/bin/activate
\`\`\`

### Bước 3: Cài đặt dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## 🚀 Chạy ứng dụng

\`\`\`bash
python main.py
\`\`\`

## 📁 Cấu trúc thư mục

\`\`\`
my-python-app/
├── main.py              # Entry point
├── config.py            # Cấu hình
├── utils/               # Tiện ích
├── tests/               # Unit tests
├── requirements.txt     # Dependencies
├── README.md
└── .gitignore
\`\`\`

## ⚙️ Cấu hình

Tạo file `.env` từ mẫu:

\`\`\`bash
cp .env.example .env
\`\`\`

Chỉnh sửa các biến:

\`\`\`
API_KEY=your_api_key_here
DEBUG=True
\`\`\`

## 🧪 Chạy tests

\`\`\`bash
pytest tests/
\`\`\`

## 📝 License

MIT License
```

---

## 🔌**TEMPLATE: API/LIBRARY**

```markdown
# My API Library

A Python library for interacting with XYZ API.

## Installation

\`\`\`bash
pip install my-api-library
\`\`\`

## Quick Start

\`\`\`python
from my_api import Client

# Khởi tạo client
client = Client(api_key="your-api-key")

# Lấy dữ liệu
data = client.get_data(id=123)
print(data)

# Tạo mới
result = client.create(name="Test", value=100)
\`\`\`

## API Reference

### Client

\`\`\`python
Client(api_key: str, timeout: int = 30)
\`\`\`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| api_key | str | Yes | Your API key |
| timeout | int | No | Request timeout in seconds (default: 30) |

### Methods

#### get_data(id)

Lấy dữ liệu theo ID.

\`\`\`python
data = client.get_data(id=123)
\`\`\`

**Parameters:**
- `id` (int): ID của record

**Returns:** `dict` - Dữ liệu

#### create(name, value)

Tạo record mới.

\`\`\`python
result = client.create(name="Test", value=100)
\`\`\`

## Error Handling

\`\`\`python
from my_api import Client, APIError

try:
    client.get_data(id=999)
except APIError as e:
    print(f"Error: {e.message}")
    print(f"Code: {e.code}")
\`\`\`

## Contributing

Xem [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License
```

---

## 🖥️**TEMPLATE: GUI APPLICATION**

```markdown
# My GUI App

![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

Ứng dụng desktop để làm XYZ.

## 📸 Screenshots

![Main Screen](docs/images/main.png)

## ✨ Tính năng

- ✅ Tính năng 1
- ✅ Tính năng 2
- ✅ Tính năng 3
- 🔜 Tính năng sắp có

## 📋 Yêu cầu

- Python 3.8+
- Thư viện:
  - PySide6 / PyQt5 / Tkinter
  - Pillow
  - pandas

## 🚀 Cài đặt & Chạy

\`\`\`bash
# Clone
git clone https://github.com/username/my-gui-app.git
cd my-gui-app

# Cài đặt
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt

# Chạy
python main.py
\`\`\`

## 💻 Hướng dẫn sử dụng

### Bước 1: Mở ứng dụng

Chạy `python main.py`

### Bước 2: Chọn file

Click nút "Open" để chọn file...

### Bước 3: Xử lý

Click "Process" để bắt đầu...

## ⌨️ Phím tắt

| Phím | Chức năng |
|------|-----------|
| Ctrl+O | Mở file |
| Ctrl+S | Lưu |
| Ctrl+Q | Thoát |
| F1 | Trợ giúp |

## 🐛 Lỗi thường gặp

### Lỗi: "ModuleNotFoundError"

**Giải pháp:** Kiểm tra đã kích hoạt venv và cài requirements.txt

### Lỗi: "Permission denied"

**Giải pháp:** Chạy với quyền Administrator

## 📝 License

MIT License

## 👤 Tác giả

**Tên bạn**
- GitHub: [@username](https://github.com/username)
```

---

## 🌐**TEMPLATE: WEB PROJECT**

```markdown
# My Web App

A modern web application built with React/Vue/Node.js.

## 🛠️ Tech Stack

- **Frontend:** React, TailwindCSS
- **Backend:** Node.js, Express
- **Database:** PostgreSQL
- **Deployment:** Docker, AWS

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- PostgreSQL

### Installation

1. Clone the repository
\`\`\`bash
git clone https://github.com/username/my-web-app.git
cd my-web-app
\`\`\`

2. Install dependencies
\`\`\`bash
npm install
\`\`\`

3. Set up environment variables
\`\`\`bash
cp .env.example .env
# Edit .env with your values
\`\`\`

4. Run database migrations
\`\`\`bash
npm run migrate
\`\`\`

5. Start development server
\`\`\`bash
npm run dev
\`\`\`

Open [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

\`\`\`
my-web-app/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/
│   └── utils/
├── public/
├── tests/
├── package.json
└── README.md
\`\`\`

## 📜 Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run test` | Run tests |
| `npm run lint` | Lint code |

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET` | Secret for JWT tokens | Yes |
| `PORT` | Server port (default: 3000) | No |

## 🚀 Deployment

### Docker

\`\`\`bash
docker build -t my-web-app .
docker run -p 3000:3000 my-web-app
\`\`\`

### Manual

\`\`\`bash
npm run build
npm start
\`\`\`

## 📝 License

MIT License
```

---

## 🏷️**BADGES (SHIELDS.IO)**

Thêm badges vào README để hiển thị thông tin:

```markdown
<!-- Version -->
![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)

<!-- License -->
![License](https://img.shields.io/badge/License-MIT-green.svg)

<!-- Python version -->
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

<!-- Build status (GitHub Actions) -->
![Build](https://github.com/username/repo/workflows/CI/badge.svg)

<!-- npm version -->
![npm](https://img.shields.io/npm/v/package-name.svg)

<!-- Downloads -->
![Downloads](https://img.shields.io/npm/dm/package-name.svg)
```

Tạo badge tại: [shields.io](https://shields.io/)

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
