# ❓ Frequently Asked Questions (FAQ)

> **Câu hỏi thường gặp về khóa học DevOps Mastery**

---

## 📚 Về khóa học

### Q: Khóa học này dành cho ai?

**A:** Khóa học phù hợp cho:

- Developers muốn chuyển sang DevOps
- System Administrators muốn học automation
- Students IT đang học về cloud
- Bất kỳ ai muốn học DevOps từ đầu

### Q: Cần kiến thức gì trước khi học?

**A:** Bạn nên có:

- Biết dùng máy tính cơ bản
- Hiểu programming concepts (không cần giỏi)
- Tiếng Anh đọc hiểu (documentation)

**Không cần:**

- Kinh nghiệm DevOps
- Linux experience (học trong course)
- Cloud experience

### Q: Học xong khóa này, tôi có thể apply việc được không?

**A:** Có, với điều kiện:

- Hoàn thành tất cả Labs
- Làm Capstone Project
- Build portfolio trên GitHub
- Thực hành thêm ngoài course

### Q: Mất bao lâu để hoàn thành khóa học?

**A:** Tùy vào thời gian bạn có:

- Full-time (8h/ngày): 3-4 tuần
- Part-time (2h/ngày): 3-4 tháng
- Casual (5h/tuần): 6-8 tháng

---

## 🔧 Về kỹ thuật

### Q: Tôi dùng Windows, có học được không?

**A:** Có! Bạn cần:

1. Cài WSL2 (Windows Subsystem for Linux)
2. Theo hướng dẫn trong SETUP_GUIDE.md
3. Hầu hết lệnh sẽ chạy trong WSL

### Q: Cần máy mạnh như thế nào?

**A:** Yêu cầu tối thiểu:

- RAM: 8GB (16GB recommended)
- Disk: 30GB trống
- CPU: Bất kỳ CPU modern

### Q: Có tốn tiền cloud không?

**A:**

- AWS Free Tier đủ cho hầu hết labs
- Một số labs advanced có thể tốn $5-20/tháng
- Nhớ tắt resources sau khi học

### Q: Docker không chạy, làm sao?

**A:** Xem troubleshooting:

1. Kiểm tra Docker Desktop đang chạy
2. WSL2 đã enable chưa
3. Virtualization trong BIOS
4. Xem SCENARIOS.md của Module 07

---

## 📖 Về nội dung

### Q: Labs có khó không?

**A:**

- Labs được thiết kế từ dễ đến khó
- Mỗi lab có step-by-step instructions
- Có expected output để verify
- Nếu stuck, search hoặc hỏi community

### Q: Scenarios là gì?

**A:**

- Tình huống thực tế gặp trong production
- Học troubleshooting skills
- Mỗi scenario có Problem → Investigation → Solution → Lesson

---

## 💼 Về career

### Q: Junior DevOps salary bao nhiêu?

**A:** (Vietnam, 2024)

- Hanoi/HCM: 12-20M VND/tháng
- Remote global: $800-1500/tháng
- Tăng nhanh sau 1-2 năm experience

### Q: Nên lấy certificate nào trước?

**A:** Theo thứ tự recommend:

1. AWS Cloud Practitioner (easiest)
2. Docker Certified Associate
3. CKA (Kubernetes)
4. Terraform Associate
5. AWS DevOps Professional (hardest)

### Q: DevOps vs SRE khác gì?

**A:**

- **DevOps**: Focus vào delivery pipeline, automation, collaboration
- **SRE**: Focus vào reliability, SLOs, incident management
- Skill overlap 70-80%
- Nhiều công ty dùng hai term thay thế nhau

---

## 🛠️ Troubleshooting

### Q: "Command not found"

**A:**

- Tool chưa được cài
- PATH chưa được set
- Chạy `which <command>` để check
- Re-run setup script

### Q: Docker permission denied

**A:**

```bash
sudo usermod -aG docker $USER
# Logout và login lại
```

### Q: kubectl không connect được cluster

**A:**

- Check `~/.kube/config`
- Cluster có đang chạy không
- Run `kubectl cluster-info`

### Q: Git push bị reject

**A:**

- Pull trước: `git pull --rebase`
- Check remote: `git remote -v`
- Authentication: HTTPS token hoặc SSH key

---

## 🤝 Cộng đồng

### Q: Có group chat không?

**A:**

- GitHub Discussions trong repo
- Reddit: r/devops
- Discord/Telegram communities (search online)

### Q: Làm sao contribute?

**A:**

1. Fork repo
2. Sửa/thêm nội dung
3. Submit Pull Request
4. Xem CONTRIBUTING.md

### Q: Tìm thấy lỗi, report ở đâu?

**A:**

- GitHub Issues
- PR fix luôn càng tốt

---

## 💡 Tips

### Q: Tips học hiệu quả?

**A:**

1. **Practice daily** - 1-2h/ngày tốt hơn 8h weekend
2. **Type commands** - Đừng copy-paste
3. **Break things** - Cố ý phá để học fix
4. **Take notes** - Document learnings của bạn
5. **Teach others** - Giải thích để hiểu sâu hơn

### Q: Resources bổ sung?

**A:**

- YouTube: TechWorld with Nana, NetworkChuck
- Udemy: Stephane Maarek, Mumshad
- Books: The Phoenix Project, SRE Book
- Practice: KillerCoda, Play with Docker/K8s

---

**Còn câu hỏi khác? Mở Issue trên GitHub!**
