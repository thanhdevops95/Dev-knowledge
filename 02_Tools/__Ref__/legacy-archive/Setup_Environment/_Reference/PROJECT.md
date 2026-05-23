---
module: "0"
title: "Setup Environment – Project"
track: "0"
version: "1.0"
last_updated: "2025-12-27"
difficulty: "Beginner"
estimated_time: "30 minutes"
technologies: ["Git", "Markdown", "VS Code"]
---

## MODULE 0 – Setup Environment Project

### 🚀 Project: My First DevOps Workspace

### Project Overview

Dự án khởi động này yêu cầu bạn tạo một kho lưu trữ (repository) cá nhân để lưu trữ toàn bộ bài tập và ghi chú trong suốt khóa học. Bạn sẽ thực hành quy trình Git cơ bản và viết Markdown.

### Architecture Diagram

```mermaid
graph LR
    Local[Local Computer] -->|Git Push| GitHub[GitHub Repo]
    VSCode[VS Code] -->|Edit| Local
```

### Project Requirements

#### Functional Requirements

1. **GitHub Repo:** Tạo một repo mới tên `devops-learning-journal`.
2. **README:** Có file `README.md` giới thiệu bản thân và mục tiêu khóa học, trình bày đẹp bằng Markdown (dùng Heading, List, Image, Bold/Italic).
3. **Structure:** Tổ chức folder theo modules (ví dụ: `Module00`, `Module01`).
4. **First Commit:** Commit code đầu tiên và push lên GitHub.

#### Non-functional Requirements

- Commit message rõ ràng (ví dụ: `docs: initialize learning journal`).
- Repo để chế độ Public để mentor có thể review (hoặc Private nhưng add collaborator nếu cần).

### Step-by-Step Implementation

#### Phase 1: Create Repository

1. Log in GitHub -> New Repository -> Name: `devops-learning-journal`.
2. Không chọn "Add a README file" (chúng ta sẽ tạo thủ công).

#### Phase 2: Local Setup

1. Mở terminal (WSL):

   ```bash
   mkdir devops-learning-journal
   cd devops-learning-journal
   git init
   ```

2. Tạo file `README.md` bằng VS Code:

   ```bash
   code README.md
   ```

3. Viết nội dung giới thiệu bản thân.

#### Phase 3: Push to GitHub

1. Link local repo với remote:

   ```bash
   git remote add origin https://github.com/<username>/devops-learning-journal.git
   ```

2. Commit và Push:

   ```bash
   git add .
   git commit -m "docs: first commit"
   git branch -M main
   git push -u origin main
   ```

### Evaluation Criteria

| Tiêu chí | Điểm | Check |
|----------|------|-------|
| Repository tồn tại trên GitHub | 30 | [ ] |
| README.md format đẹp | 40 | [ ] |
| Cấu trúc folder hợp lý | 10 | [ ] |
| Commit/Push thành công | 20 | [ ] |

### Navigation Footer ⭐ BẮT BUỘC

---

[⬅️ QUIZ](./QUIZ.md) | [📚 Mục lục](../../README.md) | [Bài tiếp: Track 1 ➡️](../Track1_Foundation_StaticWeb/1.1_Linux_Bash/README.md)
