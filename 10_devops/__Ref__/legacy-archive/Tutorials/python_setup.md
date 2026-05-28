# Hướng dẫn Cài đặt Python

<u>Version:</u> 1.0.0  
<u>Author:</u> ThanhRòm  
<u>Release Date:</u> 2025-12-17

## 📋**GIỚI THIỆU**

Tài liệu hướng dẫn cài đặt môi trường Python và quản lý dependencies.

---

## 🔧**CÀI ĐẶT PYTHON**

### Windows

1. Tải Python từ [python.org](https://www.python.org/downloads/)
2. Chạy installer, **QUAN TRỌNG**: ✅ Tick "Add Python to PATH"
3. Kiểm tra:
```powershell
python --version
pip --version
```

**Giải thích:**
- "Add Python to PATH": Thêm Python vào biến môi trường PATH để gõ `python` ở bất kỳ thư mục nào
- Nếu không tick, phải dùng đường dẫn tuyệt đối (rất phiền)
- `pip` (Package Installer for Python): Công cụ cài đặt thư viện
- `--version`: In ra version hiện tại

**Kết quả:**
```
python --version
Python 3.11.0
pip --version
pip 23.0 from C:\Users\john\AppData\...
```

**Ứng dụng:**
- Kiểm tra Python đã cài đúng không
- Xác nhận version trước khi chạy project
- Đảm bảo pip hoạt động

**Lưu ý:**
- Nếu gõ `python` không nhận, thử `py` (Windows)
- Phải đóng terminal và mở lại sau khi cài để PATH cập nhật
- Chọn "Install for all users" nếu muốn dùng chung

### macOS

```bash
# Dùng Homebrew
brew install python

# Kiểm tra
python3 --version
pip3 --version
```

**Giải thích:**
- Homebrew: Package manager cho macOS (như apt trên Linux)
- `python3`: Command gõ trên Mac (Python 2 deprecated)
- macOS có sẵn Python 2, nên cần cài Python 3 riêng
- Brew sẽ cài Python + pip tự động

**Chuẩn bị:**
```bash
# Nếu chưa có Homebrew, cài đầu tiên
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Kết quả:**
```
python3 --version
Python 3.11.6

pip3 --version
pip 23.2.1 from /usr/local/lib/python3.11/site-packages/pip ...
```

**Ứng dụng:**
- Cách chuẩn để cài Python trên Mac
- Dùng Homebrew quản lý được version dễ
- Cập nhật: `brew upgrade python`

**Lưu ý:**
- `python3` (không phải `python`) - cần ghi '3'
- `pip3` tương tự
- Nếu muốn gõ `python` mà không `3`, tạo alias

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Kiểm tra
python3 --version
pip3 --version
```

**Giải thích:**
- `sudo apt update`: Cập nhật danh sách package
- `python3`: Phiên bản Python chính
- `python3-pip`: Công cụ cài đặt thư viện
- `python3-venv`: Công cụ tạo virtual environment
- Tất cả cần cài để có đầy đủ môi trường

**Kết quả:**
```
python3 --version
Python 3.10.12

pip3 --version
pip 23.0.1 from /usr/lib/python3/dist-packages/pip ...
```

**Ứng dụng:**
- Cách tiêu chuẩn cài trên Linux
- Hầu hết server dùng Ubuntu/Debian
- Cập nhật: `sudo apt upgrade python3`

**Lưu ý:**
- Cần quyền sudo (admin)
- Luôn cài `python3-venv` để dùng virtual environment
- Không nên xóa system Python - nhiều ứng dụng phụ thuộc

---

## 📦**QUẢN LÝ THƯ VIỆN VỚI PIP**

### Cài đặt thư viện

```bash
# Cài 1 thư viện
pip install requests

# Cài nhiều thư viện
pip install pandas numpy matplotlib

# Cài version cụ thể
pip install requests==2.28.0

# Cài từ file requirements.txt
pip install -r requirements.txt
```

**Giải thích:**
- `pip install`: Lệnh cài đặt thư viện từ PyPI (Python Package Index)
- Cài từ PyPI (kho chứa hàng triệu thư viện)
- `requests`: Thư viện HTTP phổ biến
- `pandas`, `numpy`: Thư viện xử lý dữ liệu, toán học
- `-r requirements.txt`: Cài tất cả thư viện từ file

**Ví dụ:**
```bash
pip install requests               # Phiên bản mới nhất
pip install requests==2.28.0       # Phiên bản cụ thể
pip install "requests>=2.0,<3.0"   # Phiên bản trong khoảng
pip install requests[security]     # Cài thêm dependencies
```

**Kết quả:**
```
Successfully installed requests-2.31.0
Collecting pandas
... (quá trình download, install)
Successfully installed pandas-2.1.0
```

**Ứng dụng:**
- Cài thư viện cần dùng trong project
- Cài multiple thư viện cùng lúc
- Cài version cụ thể để tránh lỗi tương thích

**Lưu ý:**
- Phải kích hoạt venv trước khi cài (nếu dùng)
- `pip install` cài vào venv hiện tại hoặc system
- Cài lâu tùy tốc độ internet và kích thước thư viện

### Xem thư viện đã cài

```bash
# Liệt kê tất cả
pip list

# Xem chi tiết 1 thư viện
pip show requests

# Kiểm tra thư viện lỗi thời
pip list --outdated
```

**Giải thích:**
- `pip list`: Hiển thị tất cả thư viện đã cài
- `pip show <package>`: Xem chi tiết thư viện (path, version, dependencies)
- `--outdated`: Chỉ hiển thị thư viện có version mới hơn

**Ví dụ:**
```bash
pip list
# Package            Version
# requests           2.31.0
# pandas             2.1.0
# numpy              1.25.0

pip show requests
# Name: requests
# Version: 2.31.0
# Summary: A simple, yet elegant, HTTP library.
# Location: /usr/local/lib/python3.11/site-packages
# Requires: charset-normalizer, idna, urllib3, certifi
```

**Ứng dụng:**
- Kiểm tra thư viện đã cài chưa
- Xem version hiện tại
- Kiểm tra update sẵn có
- Debug dependencies conflict

**Lưu ý:**
- `pip list` liệt kê cả thư viện phụ (dependencies)
- `pip show` giúp biết nơi lưu file

### Gỡ thư viện

```bash
pip uninstall requests

# Gỡ nhiều thư viện
pip uninstall requests pandas numpy

# Gỡ không hỏi xác nhận
pip uninstall -y requests
```

**Giải thích:**
- `pip uninstall`: Xóa thư viện đã cài
- Hỏi xác nhận trước xóa (an toàn)
- `-y`: Xóa không hỏi

**Ví dụ:**
```bash
pip uninstall requests
# Found existing installation: requests 2.31.0
# Uninstalling requests-2.31.0:
#   Would remove: /usr/local/lib/python3.11/site-packages/requests-2.31.0.dist-info/*
#   ...
# Proceed (Y/n)? y
# Successfully uninstalled requests-2.31.0
```

**Ứng dụng:**
- Xóa thư viện không dùng
- Dọn dẹp project
- Giảm dung lượng venv

**Lưu ý:**
- Cẩn thận khi gỡ - một số thư viện phụ thuộc lẫn nhau
- `pip uninstall` không gỡ dependencies tự động
- Xóa file `venv/` nhanh hơn xóa từng thư viện

### Cập nhật thư viện

```bash
# Cập nhật 1 thư viện
pip install --upgrade requests

# Cập nhật pip
python -m pip install --upgrade pip
```

**Giải thích:**
- `--upgrade`: Cập nhật thư viện lên version mới nhất
- Kiểm tra PyPI xem có version mới
- `-m pip`: Chạy pip như module (more reliable)
- Cập nhật pip nên làm thường xuyên

**Ví dụ:**
```bash
pip install --upgrade requests
# Requirement already up-to-date: requests in /usr/local/lib/python3.11/site-packages (2.31.0)

pip install --upgrade pandas
# Collecting pandas
# ... (download version mới)
# Successfully installed pandas-2.1.1
```

**Ứng dụng:**
- Cập nhật lên version mới có bug fix
- Cập nhật pip (công cụ cài)
- Cập nhật tất cả: `pip install --upgrade -r requirements.txt`

**Lưu ý:**
- Cập nhật có thể break code nếu API thay đổi
- Kiểm tra release notes trước cập nhật
- Luôn backup hoặc dùng git trước cập nhật
- Cập nhật trong venv, không phải system Python

---

## 🌐**MÔI TRƯỜNG ẢO (VIRTUAL ENVIRONMENT)**

### Tại sao cần Virtual Environment?

| Vấn đề | Giải pháp |
|--------|-----------|
| Dự án A cần `requests 2.0`, dự án B cần `requests 3.0` | Mỗi dự án có môi trường riêng |
| Cài thư viện làm hỏng hệ thống | Thư viện chỉ nằm trong folder dự án |
| Khó chia sẻ dự án | Dùng `requirements.txt` để ai cũng cài được |

**Giải thích:**
- Virtual Environment (venv): Môi trường Python cách lập, độc lập từ system
- Mỗi project có folder `venv/` chứa Python + thư viện riêng
- Không ảnh hưởng đến Python system hoặc projects khác
- An toàn: có thể xóa venv và tạo lại bất cứ lúc nào
- Chuẩn: mỗi dự án chuyên nghiệp đều dùng venv

**Ứng dụng:**
- Isolate dependencies giữa các projects
- Tránh conflict version thư viện
- Dễ share project với team (chỉ cần requirements.txt)
- Dễ deploy lên server

**Lưu ý:**
- KHÔNG commit `venv/` lên git (quá lớn)
- Commit `requirements.txt` để ai cũng cài được
- Mỗi dev tạo `venv/` của riêng mình

### Tạo Virtual Environment

```bash
# Windows
python -m venv venv

# macOS/Linux
python3 -m venv venv
```

**Giải thích:**
- `python -m venv venv`: Chạy module venv để tạo môi trường
- `venv`: Tên folder (có thể đặt tên khác)
- `-m`: Chạy module (not a script)
- Tạo folder `venv/` chứa Python interpreter + site-packages

**Ví dụ:**
```bash
mkdir my-project
cd my-project
python -m venv venv

# Kết quả:
# my-project/
# └── venv/
#     ├── Include/
#     ├── Lib/
#     ├── Scripts/ (hoặc bin/ trên Mac/Linux)
#     └── pyvenv.cfg
```

**Kết quả:**
```
Successfully created virtual environment in my-project/venv
```

**Ứng dụng:**
- Chuẩn bị môi trường cho project mới
- Tạo venv trước khi cài dependencies

**Lưu ý:**
- Tạo venv tốn ít dung lượng (khoảng 100-200MB)
- Có thể xóa venv và tạo lại bất cứ lúc nào
- Tên folder thường là `venv` hoặc `.venv`

### Kích hoạt Virtual Environment

```bash
# Windows (PowerShell)
.\venv\Scripts\Activate

# Windows (CMD)
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

**Giải thích:**
- Kích hoạt venv = chuyển sang dùng Python từ venv
- Shell sẽ sử dụng `python`, `pip` từ venv
- Không ảnh hưởng đến system Python
- Cần chạy trước khi cài/dùng thư viện
- `activate`: Script kích hoạt (bash) hoặc `Activate` (PowerShell)

**Ví dụ:**
```bash
# Trước khi kích hoạt
$ python --version
Python 3.11.0 (system)

# Sau khi kích hoạt
$ source venv/bin/activate
(venv) $ python --version
Python 3.11.0 (from venv)
```

**Kết quả:**
```
(venv) $ 
```
> 💡 Khi kích hoạt, bạn sẽ thấy `(venv)` ở đầu dòng lệnh

**Ứng dụng:**
- Cần chạy trước khi làm việc với project
- Đảm bảo dùng Python + pip đúng

**Lưu ý:**
- LUÔN kích hoạt venv trước khi cài/chạy
- Không kích hoạt sẽ cài vào system Python (xấu!)
- Cần chạy mỗi lần mở terminal mới

### Hủy kích hoạt

```bash
deactivate
```

**Giải thích:**
- `deactivate`: Thoát khỏi venv, quay lại system Python
- Xóa tiền tố `(venv)` khỏi dòng lệnh
- Không cần chạy khi đóng terminal

**Ví dụ:**
```bash
(venv) $ deactivate
$ python --version
Python 3.11.0 (system)
```

**Ứng dụng:**
- Thoát venv khi xong
- Chuyển sang project khác với venv khác

### Cấu trúc thư mục sau khi tạo venv

```
my-project/
├── venv/                 # Thư mục môi trường ảo (KHÔNG commit lên git)
│   ├── Include/
│   ├── Lib/              # Thư viện cài đặt nằm ở đây
│   ├── Scripts/          # Chứa activate, python.exe
│   └── pyvenv.cfg
├── main.py
├── requirements.txt      # File này PHẢI commit lên git
└── .gitignore            # Thêm venv/ vào đây
```

**Giải thích:**
- `venv/`: Folder chính chứa Python + thư viện (xóa được)
- `Include/`, `Lib/`, `Scripts/`: Các folder nội bộ
- `Lib/`: Nơi lưu thư viện (site-packages)
- `Scripts/` (Windows) hoặc `bin/` (Mac/Linux): Chứa activate, python
- `main.py`: Code của bạn
- `requirements.txt`: Danh sách thư viện (chia sẻ)
- `.gitignore`: Thêm `venv/` để không commit

**Lưu ý:**
- KHÔNG commit `venv/` - nó lớn + máy khác cài lại được
- LUÔN commit `requirements.txt` - để team cài dependencies
- Thêm vào `.gitignore`:
  ```
  venv/
  __pycache__/
  *.pyc
  .env
  ```

---

## 📄**FILE REQUIREMENTS.TXT**

### Tạo file requirements.txt

```bash
# Tạo từ các thư viện đã cài
pip freeze > requirements.txt
```

**Giải thích:**
- `pip freeze`: Liệt kê tất cả thư viện đã cài với version chính xác
- `>`: Redirect output vào file
- Tạo file `requirements.txt` chứa danh sách thư viện + version
- Dùng để người khác cài lại ngay từng thư viện

**Ví dụ:**
```bash
# Kích hoạt venv trước
source venv/bin/activate

# Cài một số thư viện
pip install requests pandas numpy

# Tạo requirements.txt
pip freeze > requirements.txt

# Kết quả: file chứa
# requests==2.31.0
# pandas==2.1.0
# numpy==1.25.0
# ... (tất cả dependencies)
```

**Ứng dụng:**
- Chia sẻ project với team
- Deploy lên server
- Backup danh sách dependencies
- Tái tạo môi trường giống hệt

**Lưu ý:**
- Phải kích hoạt venv trước `pip freeze`
- Nếu chạy system Python, sẽ freeze toàn bộ system packages (không tốt)
- Nên commit requirements.txt lên git

### Cài đặt từ requirements.txt

```bash
pip install -r requirements.txt
```

**Giải thích:**
- `-r requirements.txt`: Cài tất cả thư viện từ file
- Cài từng thư viện theo version chỉ định
- Nhanh hơn cài từng cái
- Tất cả team dùng dependencies giống nhau

**Ví dụ:**
```bash
# Kích hoạt venv trước
source venv/bin/activate

# Cài từ file
pip install -r requirements.txt

# Kết quả:
# Collecting requests==2.31.0
# Collecting pandas==2.1.0
# ... (install hết)
# Successfully installed requests pandas numpy ...
```

**Kết quả:**
```
venv/Lib/site-packages/ sẽ chứa:
- requests-2.31.0/
- pandas-2.1.0/
- numpy-1.25.0/
- ... (tất cả dependencies)
```

**Ứng dụng:**
- Clone project từ github
- Chuẩn bị môi trường trên server
- Onboard developer mới

**Lưu ý:**
- Phải kích hoạt venv trước
- Cài lâu nếu thư viện lớn hoặc nhiều

### Ví dụ file requirements.txt

```txt
# ===== THƯ VIỆN CHÍNH =====
requests==2.31.0
pandas==2.1.0
numpy==1.25.0

# ===== THƯ VIỆN GUI =====
PySide6==6.5.0
# hoặc
# PyQt5==5.15.0
# hoặc
# tkinter (có sẵn, không cần cài)

# ===== THƯ VIỆN XỬ LÝ ẢNH =====
Pillow==10.0.0
opencv-python==4.8.0

# ===== THƯ VIỆN EXCEL =====
openpyxl==3.1.2
xlrd==2.0.1

# ===== THƯ VIỆN DEVELOPMENT =====
pytest==7.4.0
black==23.7.0
flake8==6.1.0
```

**Giải thích:**
- Mỗi dòng = 1 thư viện cần cài
- `package==version`: Version chính xác
- `#`: Ghi chú (Python sẽ bỏ qua)
- Tổ chức theo category (chính, GUI, ảnh, Excel, dev)
- Ghi chú giúp người khác hiểu mục đích

**Ứng dụng:**
- Document dependencies của project
- Giúp team biết thư viện nào dùng để làm gì
- Dễ bảo trì, update version

**Lưu ý:**
- Nên ghi comment giải thích từng section
- Cập nhật `requirements.txt` khi thêm thư viện mới
- Kiểm tra lại `pip freeze` trước khi commit

### Cú pháp trong requirements.txt

| Cú pháp | Ý nghĩa |
|---------|---------|
| `requests==2.31.0` | Chính xác version 2.31.0 |
| `requests>=2.31.0` | Version 2.31.0 trở lên |
| `requests>=2.0,<3.0` | Từ 2.0 đến dưới 3.0 |
| `requests` | Version mới nhất |
| `# comment` | Ghi chú |

**Giải thích:**
- `==`: Chính xác version (most common, safe)
- `>=`: Version này hoặc cao hơn (flexible)
- `>=,<`: Khoảng version (compatible versions)
- Không ghi version: Cài mới nhất (không an toàn)
- `#`: Comment (Python bỏ qua)

**Ví dụ:**
```txt
# Chính xác - BEST PRACTICE
requests==2.31.0
pandas==2.1.0

# Flexible
Flask>=2.0,<3.0

# Chỉ định tối thiểu
pytest>=7.0

# Mới nhất (không nên dùng cho production)
matplotlib
```

**Ứng dụng:**
- `==`: Production code (cần stability)
- `>=`: Development (muốn features mới)
- `>=,<`: Compromise (tương thích version range)

**Lưu ý:**
- Dùng `==` cho production code
- Dùng `pip freeze` tự động tạo `==` chính xác
- Kiểm tra compatibility trước khi lỏng version

---

## 🚀**QUY TRÌNH SETUP DỰ ÁN MỚI**

### Bước 1: Tạo thư mục dự án
```bash
mkdir my-project
cd my-project
```

**Giải thích:** Tạo folder chứa project

### Bước 2: Tạo virtual environment
```bash
python -m venv venv
```

**Giải thích:** Tạo môi trường Python riêng cho project

### Bước 3: Kích hoạt venv
```bash
# Windows
.\venv\Scripts\Activate

# macOS/Linux
source venv/bin/activate
```

**Giải thích:** Chuyển sang dùng Python từ venv (sẽ thấy `(venv)` ở đầu)

### Bước 4: Cài thư viện cần thiết
```bash
pip install requests pandas pillow
```

**Giải thích:** Cài các thư viện mà project cần dùng

### Bước 5: Tạo requirements.txt
```bash
pip freeze > requirements.txt
```

**Giải thích:** Lưu danh sách thư viện + version để share với team

### Bước 6: Tạo .gitignore
```bash
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
```

**Giải thích:** 
- Thêm `venv/` vào .gitignore để không commit lên git
- Thêm `__pycache__/` (folder cache Python)
- Nên thêm thêm: `.env`, `*.pyc`, `*.egg-info/`

**Ví dụ .gitignore đầy đủ:**
```
venv/
__pycache__/
*.py[cod]
*$py.class
.env
.DS_Store
*.egg-info/
dist/
build/
.pytest_cache/
```

### Bước 7: Khởi tạo git
```bash
git init
git add .
git commit -m "Initial commit"
```

**Giải thích:**
- `git init`: Tạo repository
- `git add .`: Thêm tất cả file (trừ .gitignore)
- `git commit`: Lưu commit đầu tiên

**Tóm tắt quy trình:**
```bash
mkdir my-project && cd my-project
python -m venv venv
source venv/bin/activate  # hoặc .\venv\Scripts\Activate trên Windows
pip install requests pandas pillow
pip freeze > requirements.txt
echo "venv/" > .gitignore
git init
git add .
git commit -m "Initial commit"
```

**Ứng dụng:**
- Chuẩn bị project Python từ đầu
- Setup lần đầu tiên khi bắt đầu project

**Lưu ý:**
- LUÔN tạo venv trước khi cài thư viện
- LUÔN kích hoạt venv trước khi làm gì
- LUÔN commit requirements.txt, KHÔNG commit venv/
- Thêm .gitignore từ đầu (dễ hơn xóa sau)

---

## 🔄**QUY TRÌNH CLONE DỰ ÁN CÓ SẴN**

### Bước 1: Clone repo
```bash
git clone https://github.com/username/project.git
cd project
```

**Giải thích:**
- `git clone`: Tải project từ github
- Tải toàn bộ source code + git history
- KHÔNG tải venv (quá lớn)

### Bước 2: Tạo virtual environment
```bash
python -m venv venv
```

**Giải thích:**
- Tạo venv mới (vì project không kèm venv)
- Mỗi máy/user tạo venv của riêng mình

### Bước 3: Kích hoạt venv
```bash
# Windows
.\venv\Scripts\Activate

# macOS/Linux
source venv/bin/activate
```

**Giải thích:** Chuyển sang dùng Python từ venv

### Bước 4: Cài thư viện từ requirements.txt
```bash
pip install -r requirements.txt
```

**Giải thích:**
- Cài tất cả thư viện + version chính xác
- Môi trường giống hệt người clone project
- Không cần phải cài từng cái

### Bước 5: Chạy ứng dụng
```bash
python main.py
```

**Giải thích:** Chạy file chính của project

**Tóm tắt quy trình:**
```bash
git clone https://github.com/username/project.git
cd project
python -m venv venv
source venv/bin/activate  # hoặc .\venv\Scripts\Activate Windows
pip install -r requirements.txt
python main.py
```

**Ứng dụng:**
- Clone project từ github
- Chuẩn bị environment để chạy code
- Onboard developer mới

**Lưu ý:**
- LUÔN tạo venv (không được dùng venv của dev khác)
- LUÔN cài từ requirements.txt (đảm bảo version đúng)
- Nếu venv bị hỏng, xóa venv/ và tạo lại
- Kiểm tra requirements.txt có requirements khác không

---

## ⚠️**LỖI THƯỜNG GẶP**

### Lỗi: 'python' is not recognized

**Nguyên nhân:** Python chưa được thêm vào PATH

**Giải pháp:**
```powershell
# Thử dùng py thay vì python (Windows)
py --version

# Hoặc cài lại Python, tick "Add to PATH"
```

**Chi tiết:**
- PATH: Biến môi trường chứa danh sách thư mục có executable
- Khi gõ `python`, Windows tìm trong PATH, không thấy → lỗi
- Lỗi này hay xảy ra khi cài Python mà quên tick "Add to PATH"

**Cách khắc phục:**
```powershell
# Cách 1: Dùng py (Windows cài sẵn)
py --version       # → Python 3.11.0
py -m pip list     # Dùng py thay python

# Cách 2: Cài lại Python, BẢO ĐẢM tick "Add Python to PATH"

# Cách 3: Thêm Python vào PATH manual (advanced)
# Control Panel → Environment Variables → Path → Add → C:\Users\username\AppData\Local\Programs\Python\Python311
```

**Lưu ý:**
- `py` có sẵn trên Windows (Python launcher)
- Có thể dùng `py` thay `python` tạm thời
- Cài lại Python là cách chắc chắn nhất

### Lỗi: Permission denied khi activate venv (PowerShell)

**Nguyên nhân:** Policy chặn chạy script

**Giải pháp:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Chi tiết:**
- Windows PowerShell có chính sách bảo mật (ExecutionPolicy)
- Mặc định không chạy script từ user (chỉ chạy system scripts)
- `RemoteSigned`: Cho phép chạy script local, nhưng script tải từ internet phải ký
- `Scope CurrentUser`: Chỉ áp dụng cho user hiện tại

**Cách khác:**
```powershell
# Dùng CMD.exe thay PowerShell
# Mở Command Prompt (cmd.exe)
venv\Scripts\activate.bat    # Chạy .bat thay .ps1

# Hoặc dùng bash (Git Bash hoặc WSL)
source venv/Scripts/activate
```

**Lưu ý:**
- `RemoteSigned` tương đối an toàn, phổ biến nhất
- Không nên dùng `Unrestricted` (quá mở)
- Nếu lo ngại, dùng CMD.exe hoặc bash

### Lỗi: ModuleNotFoundError

**Nguyên nhân:** Chưa kích hoạt venv hoặc chưa cài thư viện

**Giải pháp:**
```bash
# Kiểm tra venv đã kích hoạt chưa (phải có (venv) ở đầu)
# Cài thư viện
pip install <tên-thư-viện>
```

**Chi tiết:**
- `ModuleNotFoundError: No module named 'requests'`
- Nguyên nhân #1: Quên kích hoạt venv → dùng system Python (không cài thư viện)
- Nguyên nhân #2: Kích hoạt venv nhưng chưa cài thư viện
- Nguyên nhân #3: Cài vào venv khác hoặc system

**Cách khắc phục:**
```bash
# Kiểm tra venv kích hoạt
# Xem có (venv) ở đầu dòng không?
(venv) $ python --version
Python 3.11.0

# Nếu không có (venv), kích hoạt venv
source venv/bin/activate

# Cài thư viện
pip install requests

# Kiểm tra
python -c "import requests; print(requests.__version__)"
```

**Ví dụ lỗi:**
```bash
# SAIIII - chưa kích hoạt venv
$ python main.py
ModuleNotFoundError: No module named 'requests'

# ĐÚNG - kích hoạt venv trước
$ source venv/bin/activate
(venv) $ pip install requests
(venv) $ python main.py
# ✓ Chạy thành công
```

**Lưu ý:**
- LUÔN kích hoạt venv trước
- Kiểm tra `pip list` xem thư viện có cài chưa
- Chắc chắn kích hoạt venv đúng (xem `(venv)` ở đầu)

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
