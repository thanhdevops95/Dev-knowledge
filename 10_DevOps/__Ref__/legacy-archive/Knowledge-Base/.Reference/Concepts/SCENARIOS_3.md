# Module 04: Git Scenarios

---

## 🎯 Mục đích

Các tình huống Git thực tế và cách xử lý như một DevOps.

---

## 🚨 Scenario 1: "Committed với message sai"

### 📍 Bối cảnh

Bạn vừa commit:

```bash
git commit -m "fix bug"
```

Nhận ra message không rõ ràng, boss yêu cầu viết lại.

### 💡 Giải quyết

**Chưa push:**

```bash
git commit --amend -m "fix: resolve null pointer exception in user authentication"
```

**Đã push (cẩn thận!):**

```bash
# Sửa message
git commit --amend -m "fix: resolve null pointer in auth"

# Force push (CHỈ KHI bạn là người duy nhất làm việc trên branch)
git push --force-with-lease
```

### 📚 Bài học

- `--amend` sửa commit cuối cùng
- `--force-with-lease` an toàn hơn `--force` (check nếu ai đó đã push)
- Không force push trên branch chung (main, develop)

---

## 🚨 Scenario 2: "Committed file nhạy cảm"

### 📍 Bối cảnh

Bạn vô tình commit file chứa password:

```bash
git add .
git commit -m "add config"
git push
# Ôi không! .env với DB_PASSWORD đã lên GitHub!
```

### 🔍 Vấn đề

- Password đã public
- Xóa file không xóa khỏi history
- Ai đó có thể xem commit cũ

### 💡 Giải quyết

**Bước 1: Đổi password ngay lập tức!**

Password đã bị lộ = coi như bị hack.

**Bước 2: Xóa file khỏi history**

```bash
# Dùng git filter-branch
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

# Hoặc dùng BFG (nhanh hơn)
bfg --delete-files .env

# Force push tất cả branches
git push --force --all
```

**Bước 3: Thêm vào .gitignore**

```bash
echo ".env" >> .gitignore
git add .gitignore
git commit -m "chore: add .env to gitignore"
git push
```

### 📚 Bài học

1. **LUÔN có .gitignore** trước khi code
2. **Review `git status`** trước khi add all
3. **Dùng pre-commit hooks** để ngăn commit secrets

---

## 🚨 Scenario 3: "Push lên branch sai"

### 📍 Bối cảnh

Bạn làm việc, commit, push... rồi nhận ra đang ở `main` thay vì branch của mình!

```bash
git push origin main
# 😱 Pushed to production!
```

### 💡 Giải quyết

**Bước 1: Tạo branch mới với commits đó**

```bash
# Di chuyển commits sang branch mới
git checkout -b feature/my-work
```

**Bước 2: Reset main về trạng thái trước**

```bash
git checkout main

# Xem commit trước của bạn
git log --oneline

# Reset về commit cuối đúng (abc1234)
git reset --hard abc1234

# Force push main
git push --force origin main
```

**Bước 3: Push branch mới**

```bash
git checkout feature/my-work
git push -u origin feature/my-work
```

### 📚 Bài học

1. **Kiểm tra branch** trước khi commit: `git branch`
2. **Protect main branch** trên GitHub Settings
3. **Dùng Pull Request** thay vì push trực tiếp

---

## 🚨 Scenario 4: "Merge conflict trong file quan trọng"

### 📍 Bối cảnh

Bạn merge feature branch và gặp conflict trong file production config.

```bash
git merge feature/new-deployment
# CONFLICT (content): Merge conflict in deployment.yaml
```

### 🔍 Phân tích

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 
<<<<<<< HEAD
    3
=======
    5
>>>>>>> feature/new-deployment
```

HEAD (main) có 3 replicas, feature branch có 5.

### 💡 Giải quyết

**Bước 1: Hiểu context**

```bash
# Xem commit của mỗi bên
git log --oneline main

git log --oneline feature/new-deployment
```

**Bước 2: Quyết định**

- Hỏi người tạo feature branch: "Tại sao đổi từ 3 → 5?"
- Có thể feature cần nhiều replicas hơn cho performance

**Bước 3: Resolve**

```yaml
# Chọn giá trị phù hợp
spec:
  replicas: 5  # Increased for new feature load
```

```bash
git add deployment.yaml
git commit -m "Merge feature/new-deployment: increase replicas to 5"
```

### 📚 Bài học

1. **Đừng resolve mù quáng** - Hiểu tại sao có conflict
2. **Communicate** với team
3. **Test sau khi resolve**

---

## 🚨 Scenario 5: "Commit nhầm file lớn"

### 📍 Bối cảnh

Commit file 500MB (video, database dump...), giờ không push được.

```bash
git push origin main
# remote: error: GH001: Large files detected
# remote: error: File data.dump is 523.00 MB; exceeds 100 MB limit
```

### 💡 Giải quyết

**Cách 1: Nếu chưa push, xóa khỏi history**

```bash
# Xóa file khỏi commit cuối
git rm --cached data.dump
git commit --amend --no-edit

# Thêm vào gitignore
echo "*.dump" >> .gitignore
git add .gitignore
git commit -m "chore: ignore dump files"
```

**Cách 2: Dùng Git LFS (Large File Storage)**

```bash
# Cài Git LFS
git lfs install

# Track file types lớn
git lfs track "*.dump"
git lfs track "*.zip"

# Add .gitattributes
git add .gitattributes
git commit -m "chore: setup Git LFS"

# Push
git push
```

### 📚 Bài học

1. **Setup .gitignore sớm**
2. **Dùng Git LFS** cho files lớn
3. **Không commit generated files** (builds, dumps)

---

## 🚨 Scenario 6: "Mất code sau khi reset --hard"

### 📍 Bối cảnh

Bạn chạy:

```bash
git reset --hard HEAD~5
# 😱 5 commits cuối biến mất!
```

### 💡 Giải quyết

**Git reflog cứu bạn!**

```bash
# Xem lịch sử tất cả HEAD movements
git reflog

# Output:
# abc1234 HEAD@{0}: reset: moving to HEAD~5
# def5678 HEAD@{1}: commit: feat: important feature
# 789ghi0 HEAD@{2}: commit: fix: critical bug
# ...

# Quay lại commit trước reset
git reset --hard def5678
```

### 📚 Bài học

1. **git reflog** là lifesaver
2. **Nghĩ kỹ trước khi `--hard`**
3. **Push thường xuyên** lên remote để có backup

---

## 🚨 Scenario 7: "Pull bị reject"

### 📍 Bối cảnh

```bash
git push origin main
# ! [rejected] main -> main (non-fast-forward)
# error: failed to push some refs
```

### 🔍 Nguyên nhân

Ai đó đã push commits mới lên main. Git từ chối vì sẽ mất commits đó.

### 💡 Giải quyết

**Cách 1: Pull rồi push**

```bash
git pull origin main
# Có thể có conflict, resolve nếu cần
git push origin main
```

**Cách 2: Pull với rebase (history sạch hơn)**

```bash
git pull --rebase origin main
# Apply commits của bạn lên trên commits mới
git push origin main
```

### Sơ đồ

```
Before pull:
Remote: A---B---C
Local:  A---B---X---Y

After pull --rebase:
A---B---C---X'---Y'
```

### 📚 Bài học

1. **Pull trước khi push**
2. **Dùng `--rebase`** cho history linear
3. **Fetch thường xuyên** để biết có changes mới

---

## 📋 Git Troubleshooting Cheatsheet

| Vấn đề | Giải pháp |
|--------|-----------|
| Sai commit message | `git commit --amend` |
| Committed secrets | Filter-branch/BFG + đổi password |
| Push nhầm branch | Reset + force push |
| Merge conflict | Manual resolve |
| File quá lớn | Git LFS |
| Mất commits | `git reflog` |
| Push rejected | `git pull --rebase` |
| Wrong branch | `git checkout -b` + reset |

---

## ⏭️ Module tiếp theo

👉 **[Module 05: Web Servers](../05_WEB_SERVERS/README.md)**
