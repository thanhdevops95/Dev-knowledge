# 💪 Exercises: Git & GitLab

> **Self-practice exercises for Git.**
>
> *Bài tập tự luyện Git.*

---

## Exercise 1: Repository Setup ⭐

1. Create a new repository with README, .gitignore (Node.js), and LICENSE *(Tạo repository mới với README, .gitignore, và LICENSE)*
2. Clone to local *(Clone về local)*
3. Create structure: *(Tạo cấu trúc:)*

   ```
   project/
   ├── src/
   ├── tests/
   ├── docs/
   └── .github/
   ```

4. Commit and push *(Commit và push)*

---

## Exercise 2: Branching Strategy ⭐⭐

1. Create branches: `develop`, `feature/auth`, `feature/api` *(Tạo các branches)*
2. Implement "features" (create files) in each branch *(Implement "features" trong mỗi branch)*
3. Merge `feature/auth` into `develop` *(Merge vào develop)*
4. Merge `feature/api` into `develop`
5. Create release branch `release/1.0`
6. Merge release into `main` and `develop`
7. Tag version `v1.0.0`

---

## Exercise 3: Conflict Resolution ⭐⭐

1. Create file `config.json` on `main` *(Tạo file trên main)*
2. Create 2 branches from main *(Tạo 2 branches từ main)*
3. Edit the same line on both branches *(Edit cùng dòng trên cả 2 branches)*
4. Merge branch 1 into main
5. Merge branch 2 (will conflict) *(Sẽ conflict)*
6. Resolve conflict manually *(Resolve conflict thủ công)*
7. Document conflict resolution process

---

## Exercise 4: Interactive Rebase ⭐⭐⭐

1. Create 5 commits with poor messages *(Tạo 5 commits với messages không tốt)*
2. Use `git rebase -i` to: *(Sử dụng `git rebase -i` để:)*
   - Squash 2 commits
   - Reword 2 commits
   - Reorder commits
3. Push with `--force-with-lease`

---

## Exercise 5: Git Hooks ⭐⭐

Create hooks: *(Tạo hooks:)*

1. **pre-commit**: Check for TODO comments
2. **commit-msg**: Enforce conventional commits
3. **pre-push**: Run tests

---

## Exercise 6: Collaboration Workflow ⭐⭐⭐

1. Fork a public repository *(Fork một public repository)*
2. Clone fork to local *(Clone fork về local)*
3. Add upstream remote
4. Create feature branch
5. Make changes and commit *(Thay đổi và commit)*
6. Sync with upstream *(Sync với upstream)*
7. Create Pull Request

---

## 📝 Checklist

- [ ] Exercise 1: Repository Setup
- [ ] Exercise 2: Branching Strategy
- [ ] Exercise 3: Conflict Resolution
- [ ] Exercise 4: Interactive Rebase
- [ ] Exercise 5: Git Hooks
- [ ] Exercise 6: Collaboration

---

**[← Back to README](./README.md)** | **[View Solutions →](./SOLUTIONS.md)**
