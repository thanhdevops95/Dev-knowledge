# Hướng dẫn Cấu trúc Dự án

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Tài liệu hướng dẫn cách tổ chức thư mục dự án chuẩn cho các ngôn ngữ khác nhau.

---

## 🐍**CẤU TRÚC DỰ ÁN PYTHON**

### Dự án đơn giản (Script)

```
my-script/
├── main.py               # File chính
├── README.md             # Hướng dẫn
├── requirements.txt      # Dependencies
├── .gitignore           # Ignore git
└── venv/                # Virtual environment (không commit)
```

### Dự án vừa (Application)

```
my-app/
├── src/                  # Source code
│   ├── __init__.py      # Đánh dấu là package
│   ├── main.py          # Entry point
│   ├── config.py        # Cấu hình
│   ├── utils.py         # Tiện ích
│   └── modules/         # Các module
│       ├── __init__.py
│       ├── module1.py
│       └── module2.py
├── tests/               # Unit tests
│   ├── __init__.py
│   ├── test_main.py
│   └── test_utils.py
├── data/                # Dữ liệu (thường không commit)
├── logs/                # Log files (không commit)
├── docs/                # Tài liệu
├── README.md
├── requirements.txt
├── setup.py             # Nếu publish lên PyPI
├── .gitignore
└── venv/
```

### Dự án lớn (Package có thể publish)

```
my-package/
├── src/
│   └── my_package/      # Tên package
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── engine.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py
│       └── cli.py       # Command line interface
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py      # Pytest fixtures
├── docs/
│   ├── api/
│   └── guides/
├── examples/            # Ví dụ sử dụng
├── scripts/             # Scripts hỗ trợ
├── README.md
├── LICENSE
├── CHANGELOG.md
├── requirements.txt
├── requirements-dev.txt # Dependencies cho development
├── setup.py
├── setup.cfg
├── pyproject.toml       # Modern Python packaging
├── Makefile             # Commands tự động
├── .gitignore
├── .github/             # GitHub Actions
│   └── workflows/
└── venv/
```

---

## 🟢**CẤU TRÚC DỰ ÁN NODE.JS**

### Dự án đơn giản

```
my-node-app/
├── src/
│   └── index.js         # Entry point
├── package.json         # Dependencies & scripts
├── package-lock.json    # Lock file
├── README.md
├── .gitignore
└── node_modules/        # (không commit)
```

### Dự án Express.js (API)

```
my-api/
├── src/
│   ├── index.js         # Entry point
│   ├── app.js           # Express app
│   ├── config/
│   │   └── database.js
│   ├── routes/
│   │   ├── index.js
│   │   ├── users.js
│   │   └── products.js
│   ├── controllers/
│   │   ├── userController.js
│   │   └── productController.js
│   ├── models/
│   │   ├── User.js
│   │   └── Product.js
│   ├── middlewares/
│   │   ├── auth.js
│   │   └── errorHandler.js
│   └── utils/
│       └── helpers.js
├── tests/
├── public/              # Static files
├── views/               # Templates (nếu có)
├── package.json
├── .env.example         # Mẫu file .env
├── .gitignore
└── README.md
```

### Dự án React/Next.js

```
my-react-app/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── index.js
│   ├── App.js
│   ├── components/
│   │   ├── Header/
│   │   │   ├── Header.js
│   │   │   └── Header.css
│   │   └── Footer/
│   ├── pages/
│   │   ├── Home.js
│   │   └── About.js
│   ├── hooks/           # Custom hooks
│   ├── context/         # React Context
│   ├── services/        # API calls
│   ├── utils/
│   ├── assets/          # Images, fonts
│   └── styles/
│       ├── global.css
│       └── variables.css
├── package.json
├── .env
├── .gitignore
└── README.md
```

---

## 🔵**CẤU TRÚC DỰ ÁN C#/.NET**

### Console App

```
MyConsoleApp/
├── MyConsoleApp.sln     # Solution file
├── src/
│   └── MyConsoleApp/
│       ├── MyConsoleApp.csproj
│       ├── Program.cs
│       ├── Services/
│       └── Models/
├── tests/
│   └── MyConsoleApp.Tests/
│       ├── MyConsoleApp.Tests.csproj
│       └── UnitTests.cs
├── README.md
└── .gitignore
```

### ASP.NET Web API

```
MyWebApi/
├── MyWebApi.sln
├── src/
│   └── MyWebApi/
│       ├── MyWebApi.csproj
│       ├── Program.cs
│       ├── Startup.cs
│       ├── Controllers/
│       │   └── UsersController.cs
│       ├── Models/
│       │   └── User.cs
│       ├── Services/
│       │   └── UserService.cs
│       ├── Data/
│       │   └── AppDbContext.cs
│       ├── DTOs/
│       └── appsettings.json
├── tests/
├── README.md
└── .gitignore
```

---

## ☕**CẤU TRÚC DỰ ÁN JAVA**

### Maven Project

```
my-java-app/
├── pom.xml              # Maven config
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── mycompany/
│   │   │           └── app/
│   │   │               ├── App.java
│   │   │               ├── models/
│   │   │               ├── services/
│   │   │               └── utils/
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/
│           └── com/
│               └── mycompany/
│                   └── app/
│                       └── AppTest.java
├── target/              # Build output (không commit)
├── README.md
└── .gitignore
```

### Spring Boot

```
my-spring-app/
├── pom.xml
├── src/
│   ├── main/
│   │   ├── java/com/mycompany/app/
│   │   │   ├── Application.java
│   │   │   ├── controller/
│   │   │   ├── service/
│   │   │   ├── repository/
│   │   │   ├── model/
│   │   │   ├── dto/
│   │   │   └── config/
│   │   └── resources/
│   │       ├── application.yml
│   │       ├── static/
│   │       └── templates/
│   └── test/
├── README.md
└── .gitignore
```

---

## 📁**CÁC THƯ MỤC CHUNG**

| Thư mục | Mục đích |
|---------|----------|
| `src/` | Source code chính |
| `tests/` hoặc `test/` | Unit tests |
| `docs/` | Tài liệu |
| `scripts/` | Scripts hỗ trợ (build, deploy) |
| `config/` | File cấu hình |
| `data/` | Dữ liệu mẫu, fixtures |
| `logs/` | Log files |
| `public/` | Static files (web) |
| `assets/` | Images, fonts |
| `examples/` | Ví dụ sử dụng |
| `.github/` | GitHub Actions, templates |

---

## 📄**CÁC FILE QUAN TRỌNG**

| File | Mục đích |
|------|----------|
| `README.md` | Hướng dẫn dự án |
| `LICENSE` | Giấy phép |
| `CHANGELOG.md` | Lịch sử thay đổi |
| `.gitignore` | Ignore files cho git |
| `.env` | Biến môi trường (không commit) |
| `.env.example` | Mẫu .env (commit) |
| `Makefile` | Commands tự động |
| `Dockerfile` | Cấu hình Docker |
| `docker-compose.yml` | Multi-container Docker |

---

## ✅**QUY TẮC ĐẶT TÊN**

### Thư mục

| Convention | Ví dụ | Dùng cho |
|------------|-------|----------|
| lowercase | `models`, `utils` | Phổ biến nhất |
| snake_case | `my_module` | Python |
| kebab-case | `my-component` | Node.js, web |
| PascalCase | `MyClass` | C#, Java (cho class) |

### File

| Ngôn ngữ | Convention | Ví dụ |
|----------|------------|-------|
| Python | snake_case | `my_module.py` |
| JavaScript | camelCase hoặc kebab-case | `myModule.js`, `my-component.js` |
| C# | PascalCase | `MyClass.cs` |
| Java | PascalCase (class) | `MyClass.java` |

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
