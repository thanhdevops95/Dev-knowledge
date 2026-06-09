# 🧪 Bài thực hành: Người hùng giải cứu code — Conflict Hero

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.1.0\
> **Tạo lúc:** 26/05/2026\
> **Cập nhật:** 26/05/2026\
> **Độ khó:** 🟡\
> **Thời gian ước tính:** ~30 phút\
> **Prerequisites:** Đã học xong bài học [01_resolving-conflicts.md](../../lessons/02_intermediate/01_resolving-conflicts.md) ✅

---

## 🎯 Mục tiêu của bài Lab
Trăm nghe không bằng một thấy, trăm thấy không bằng một gõ! Cách duy nhất để bạn không còn sợ hãi trước Merge Conflict là **chủ động tạo ra nó trong môi trường kiểm soát và tự mình giải quyết nó**. 

Trong bài Lab này, bạn sẽ đóng vai một dũng sĩ dung hợp hai trường phái sức mạnh: **Kiếm thuật** và **Phép thuật** đang bị xung đột mã nguồn trong tệp tin `hero.py` để tạo nên một chiêu thức tối thượng vô địch!

---

## 🔍 Kiểm tra môi trường (Environment Check)
Hãy đảm bảo môi trường Terminal của bạn sẵn sàng để thực hiện phân nhánh và gộp code nâng cao:

| Công cụ | Lệnh kiểm tra | Kết quả mong đợi |
|---|---|---|
| **Git đã cài** | `git --version` | Phiên bản Git hiện tại |
| **Trình soạn thảo VS Code** | `code --version` | Đảm bảo lệnh `code` mở được VS Code từ terminal |

> 💡 **Mẹo:** Nếu gõ `code .` mà báo lỗi `command not found`, hãy mở VS Code lên → Nhấn `Cmd+Shift+P` (Mac) hoặc `Ctrl+Shift+P` (Windows) → Gõ `Shell Command: Install 'code' command in PATH` → Nhấn Enter là xong.

---

## 🗺️ Quy trình giả lập xung đột
```
                  ┌─── Nhánh feature/magic-sword ───> Sửa dòng 3 thành "Kiếm Pháp" ───> Merge OK
                  │
[Commit gốc: Độc hành]
                  │
                  └─── Nhánh feature/fire-magic  ───> Sửa dòng 3 thành "Hỏa Thuật"  ───> Merge CONFLICT!
```

---

## 🛠️ Từng bước thực hành chi tiết

### 📂 Bước 1: Khởi tạo Repo thực hành cục bộ
Mở Terminal của bạn lên và gõ các lệnh sau để tạo một thư mục trống:

```bash
cd ~/Desktop
mkdir conflict-hero-playground
cd conflict-hero-playground
git init
```
Output thực tế hiển thị:
```
Initialized empty Git repository in /Users/user/Desktop/conflict-hero-playground/.git/
```
*   **Giải thích output:** Thư mục ẩn `.git/` đã được khởi tạo thành công làm cơ sở dữ liệu ngầm để lưu giữ lịch sử phân nhánh của dũng sĩ.

---

### 📝 Bước 2: Tạo tệp `hero.py` và tạo commit gốc
Tạo file `hero.py` mô tả trạng thái ban đầu của dũng sĩ cô độc chưa có kỹ năng:
```bash
cat > hero.py << 'EOF'
class Hero:
    def __init__(self):
        self.skill = "Độc hành (Basic)"

    def show_identity(self):
        print(f"Ta là Dũng sĩ với kỹ năng: {self.skill}")
EOF
```

Đóng gói commit gốc trên nhánh `main`:
```bash
git add hero.py
git commit -m "feat: init lonely hero class"
```
Output thực tế hiển thị:
```
[main (root-commit) f1e2d3c] feat: init lonely hero class
 1 file changed, 6 insertions(+)
 create mode 100644 hero.py
```
*   **Giải thích output:** Git tạo thành công commit gốc `f1e2d3c` trên nhánh chính `main` ghi nhận sự khai sinh của class Hero.

---

### ⚔️ Bước 3: Học "Kiếm Pháp" ở nhánh `feature/magic-sword`
Tách nhánh mới để phát triển chiêu thức Kiếm thuật:
```bash
git checkout -b feature/magic-sword
```
Output thực tế:
```
Switched to a new branch 'feature/magic-sword'
```
*   **Giải thích output:** Trạng thái chuyển nhánh thành công sang dòng thời gian song song mang tên `feature/magic-sword`. Mọi code gõ ở đây sẽ hoàn toàn độc lập với `main`.

Mở file `hero.py` ra sửa đổi dòng số 3 thành kỹ năng kiếm thuật:
```bash
cat > hero.py << 'EOF'
class Hero:
    def __init__(self):
        self.skill = "Tuyệt kỹ: Vạn Kiếm Quy Tông ⚔️"

    def show_identity(self):
        print(f"Ta là Dũng sĩ với kỹ năng: {self.skill}")
EOF
```

Lưu lại chiến công kiếm pháp:
```bash
git commit -am "feat: learn ultimate sword skill"
```

---

### 🔥 Bước 4: Học "Hỏa Thuật" ở nhánh `feature/fire-magic`
Quay trở lại nhánh `main` để chuẩn bị đi theo trường phái phép thuật:
```bash
git checkout main
```
Output thực tế:
```
Switched to branch 'main'
```
*   **Giải thích output:** Quay trở về nhánh chính. File `hero.py` lập tức quay về trạng thái thô sơ ban đầu *"Độc hành (Basic)"* nhờ cơ chế khôi phục kỳ diệu của Git.

Tách nhánh phụ thứ hai để học phép thuật lửa:
```bash
git checkout -b feature/fire-magic
```

Sửa đổi đúng dòng số 3 của file `hero.py` thành chiêu thức phép thuật lửa bùng cháy:
```bash
cat > hero.py << 'EOF'
class Hero:
    def __init__(self):
        self.skill = "Phép thuật: Long Hỏa Bùng Cháy 🔥"

    def show_identity(self):
        print(f"Ta là Dũng sĩ với kỹ năng: {self.skill}")
EOF
```

Lưu lại chiến công hỏa thuật:
```bash
git commit -am "feat: learn ultimate fire magic"
```

---

### 💥 Bước 5: Kích hoạt Merge Conflict đỏ lửa!
Quay trở lại nhánh chính `main`:
```bash
git checkout main
```

**Gộp nhánh thứ nhất (Kiếm thuật) vào trước:**
```bash
git merge feature/magic-sword
```
Output thực tế hiển thị:
```
Updating f1e2d3c..a4b5c6d
Fast-forward
 hero.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
```
*   **Giải thích output:** Git tiến hành gộp nhanh kiểu **Fast-forward** không tạo commit mới vì nhánh `main` chưa bị chỉnh sửa gì kể từ khi tách nhánh Kiếm thuật. Nhánh `main` lúc này chính thức sở hữu kỹ năng *"Vạn Kiếm Quy Tông ⚔️"*.

**Gộp tiếp nhánh thứ hai (Phép thuật lửa) đè lên:**
```bash
git merge feature/fire-magic
```
Ngay lập tức, tiếng nổ xung đột dữ dội vang lên!
```
Auto-merging hero.py
CONFLICT (content): Merge conflict in hero.py
Automatic merge failed; fix conflicts and then commit the result.
```
*   **Giải thích output:** Git thông báo quá trình tự động gộp file `hero.py` thất bại vì phát hiện hai thay đổi đè lên cùng một dòng số 3. Hệ thống bị kẹt lại để chờ bạn hòa giải.

---

### 🤝 Bước 6: Dung hợp chiêu thức tối thượng — Resolve Conflict
Mở thư mục dự án này bằng **VS Code** của bạn:
```bash
code .
```

Mở tệp `hero.py` lên. Bạn sẽ thấy VS Code bôi đậm vùng màu xung đột kèm theo các nút bấm trực quan trên đầu dòng số 3:
```python
<<<<<<< HEAD
        self.skill = "Tuyệt kỹ: Vạn Kiếm Quy Tông ⚔️"
=======
        self.skill = "Phép thuật: Long Hỏa Bùng Cháy 🔥"
>>>>>>> feature/fire-magic
```

Bản chất của một người anh hùng không phải là triệt tiêu đối thủ, mà là **hòa hợp sức mạnh**. 
*   Hãy dùng chuột click chọn **`Accept Both Changes`** (Nhận cả hai thay đổi) trong VS Code.
*   Sau đó tự tay biên soạn lại dòng code số 3 để dung hợp hai sức mạnh thành chiêu thức độc nhất vô nhị. Nội dung file `hero.py` sau khi hòa giải tuyệt đối:

```python
class Hero:
    def __init__(self):
        self.skill = "Song hệ: Ma Kiếm Vạn Hỏa bùng nổ! ⚔️🔥"

    def show_identity(self):
        print(f"Ta là Dũng sĩ với kỹ năng: {self.skill}")
```
*Lưu file lại.*

Quay lại Terminal, kiểm tra trạng thái và đóng gói Merge Commit để hoàn tất:
```bash
git add hero.py
git commit -m "merge: resolve conflict, combine sword and fire magic into hybrid skill"
```
Output thực tế hiển thị thành công:
```
[main e7f8g9h] merge: resolve conflict, combine sword and fire magic into hybrid skill
```
*   **Giải thích output:** Merge Commit `e7f8g9h` đã được tạo ra ghi nhận sự hòa hợp tuyệt vời của hai nhánh kỹ năng.

---

## ✅ Tiêu chí hoàn thành bài Lab (Exit Criteria)
Hãy tự kiểm chứng thành quả anh hùng của bạn:

1.  **Kiểm tra lịch sử:** Chạy lệnh `git log --oneline --graph`. Bạn phải thấy sơ đồ hiển thị nhánh rẽ ra làm hai dòng thời gian và chụm đầu lại tại một commit gộp hoàn mỹ:
    ```
    *   e7f8g9h (HEAD -> main) merge: resolve conflict, combine sword and fire magic into hybrid skill
    |\  
    | * f6g7h8i (feature/fire-magic) feat: learn ultimate fire magic
    * | a4b5c6d feat: learn ultimate sword skill
    |/  
    * f1e2d3c feat: init lonely hero class
    ```
2.  **Kiểm tra trạng thái:** Gõ `git status` báo `working tree clean`.
3.  **Kiểm tra code:** Chạy thử file python (nếu máy có cài python):
    ```bash
    python3 -c "import hero; h = hero.Hero(); h.show_identity()"
    ```
    Output in ra màn hình kiêu hãnh dòng chữ:
    ```
    Ta là Dũng sĩ với kỹ năng: Song hệ: Ma Kiếm Vạn Hỏa bùng nổ! ⚔️🔥
    ```

---

## 🧹 Dọn dẹp tài nguyên (Cleanup)
Sau khi đã hoàn thành thử thách và gỡ conflict thành công, hãy dọn dẹp sạch sẽ thư mục thực hành trên Desktop để máy tính luôn gọn gàng:

```bash
cd ~/Desktop
rm -rf conflict-hero-playground
```
*Việc dọn dẹp này giúp tránh rác ổ cứng và tránh xung đột đường dẫn cho các bài thực hành tiếp theo.*

---

## 🔗 Liên kết & Tài nguyên
*   ➡️ Thử thách tiếp theo: [lab_team-pull-request.md](./lab_team-pull-request.md) — Thực hành quy trình Pull Request chuyên nghiệp.
