---
module: "0"
title: "Setup Environment – Solutions"
track: "0"
version: "1.0"
last_updated: "2025-12-27"
---

## MODULE 0 – Setup Environment Solutions

### Exercise 1: Docker Permission Challenge

**Problem Recap:** Lỗi `permission denied` khi chạy docker không sudo.

#### 💡 Why This Solution?

Mặc định daemon Docker chạy dưới quyền root. Socket Unix `/var/run/docker.sock` thuộc về user `root` và group `docker`. Bằng cách thêm user hiện tại vào group `docker`, bạn có quyền đọc/ghi vào socket này mà không cần leo thang đặc quyền tạm thời bằng `sudo`.

#### Solution Steps

1. Tạo group docker (nếu chưa có):

   ```bash
   sudo groupadd docker
   ```

2. Thêm user hiện tại ($USER) vào group docker:

   ```bash
   sudo usermod -aG docker $USER
   ```

3. Kích hoạt thay đổi group (hoặc log out/log in):

   ```bash
   newgrp docker
   ```

4. Verify:

   ```bash
   docker run hello-world
   ```

**Common Mistakes:**

- Quên logout/login hoặc chạy `newgrp` nên shell chưa nhận group mới.
- Dùng `chmod 777` lên file socket (Rất nguy hiểm về bảo mật!).

---

### Exercise 2: Git Identity Crisis

**Problem Recap:** GitHub không nhận diện được commit owner.

#### 💡 Why This Solution?

GitHub map commit với user dựa trên trường `email` trong meta-data của commit. Nếu email này không khớp với bất kỳ email nào đã verify trong tài khoản GitHub của bạn, nó sẽ coi là một user vô danh.

#### Solution Steps

1. Kiểm tra config hiện tại:

   ```bash
   git config user.email
   ```

2. Cài đặt lại email khớp với GitHub:

   ```bash
   git config --global user.email "your_email@example.com"
   ```

3. (Optional) Sửa lại commit trước đó (nếu chưa push):

   ```bash
   git commit --amend --reset-author --no-edit
   ```

**Output Verification:**
Chạy `git log`. Output nên có dạng:

```text
Author: Your Name <correct_email@example.com>
```

---

### References

- [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/)
- [Setting your commit email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-email-preferences/setting-your-commit-email-address)
- [GLOSSARY](../../resources/GLOSSARY.md)

### Navigation Footer ⭐ BẮT BUỘC

---

[⬅️ EXERCISES](./EXERCISES.md) | [📚 Mục lục](../../README.md) | [QUIZ ➡️](./QUIZ.md)
