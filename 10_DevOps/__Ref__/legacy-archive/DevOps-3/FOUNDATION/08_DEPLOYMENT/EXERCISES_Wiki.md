# Exercises: Module 08 - DEPLOYMENT

> **Bài tập kiểm tra kiến thức Deployment**

**Tổng điểm:** 150  
**Thời gian:** 60 phút  
**Đạt:** 105/150 (70%)

---

## PHẦN A: TRẮC NGHIỆM (30 điểm)

**Câu 1:** Deployment strategy tốt nhất cho zero-downtime?

- A) Stop old, start new
- B) Blue-green deployment
- C) Delete và recreate
- D) Manual file copy

**Câu 2:** Rolling deployment là gì?

- A) Update tất cả instances cùng lúc
- B) Update từng instance một
- C) Roll back changes
- D) Rotate logs

**Câu 3:** Canary deployment nghĩa là:

- A) Deploy cho tất cả users
- B) Deploy cho % nhỏ users trước
- C) Deploy chỉ ban đêm
- D) Deploy bằng chim

**Câu 4:** systemd restart policy `Restart=always`:

- A) Restart một lần
- B) Restart khi crash và boot
- C) Không bao giờ restart
- D) Restart hàng ngày

**Câu 5:** Environment variables nên:

- A) Hardcode trong code
- B) Trong .env files (gitignored)
- C) Trong public repos
- D) Share công khai

**Câu 6:** Health check HTTP code cho healthy:

- A) 500
- B) 404
- C) 200
- D) 301

**Câu 7:** Database migration best practice:

- A) Drop tables trực tiếp
- B) Forward-compatible changes
- C) Không backup
- D) Chỉ test production

**Câu 8:** Quick rollback cần:

- A) Previous version sẵn sàng
- B) Rewrite code
- C) Database restore
- D) User permission

**Câu 9:** Blue-green sử dụng:

- A) 1 environment
- B) 2 environments đồng thời
- C) 3 environments
- D) Màu sắc cho vui

**Câu 10:** Zero-downtime yêu cầu chính:

- A) Stop tất cả services
- B) Health checks + gradual switch
- C) Maintenance window
- D) User notification

---

## PHẦN B: SCENARIOS (60 điểm)

**Câu 11: Debug Failed Deployment (15 điểm)**

Tình huống:

```
New version deployed, nhưng:
- Health check returns 500
- Users getting errors
```

**Tasks:**

- Identify nguyên nhân
- Fix issue
- Verify fix
- Prevent trong tương lai

---

**Câu 12: Implement Blue-Green (15 điểm)**

Setup blue-green cho Flask app:

- Cả 2 versions chạy
- NGINX switch traffic
- Instant rollback

---

**Câu 13: Database Migration (15 điểm)**

Add `email` column vào users table:

- Không break old code
- Safe rollback plan
- Step-by-step process

---

**Câu 14: Rollback Script (15 điểm)**

Viết automated rollback script:

- Switch về previous version
- Restart services
- Verify health
- Log actions

---

## PHẦN C: PRACTICAL (60 điểm)

**Câu 15: Deployment Script (20 điểm)**

Viết deploy.sh:

- Pull latest code
- Install dependencies
- Run migrations
- Restart service
- Health check
- Rollback on failure

---

**Câu 16: Health Check Endpoint (15 điểm)**

Implement /health kiểm tra:

- Database connection
- Redis connection
- Disk space
- Returns 200 nếu healthy

---

**Câu 17: systemd Service (15 điểm)**

Tạo production systemd service:

- Auto-restart on crash
- Logs to file
- Starts on boot
- Uses environment file

---

**Câu 18: NGINX Blue-Green Config (10 điểm)**

Configure NGINX:

- Blue on port 5001
- Green on port 5002
- Easy traffic switch

---

## 📊 THANG ĐIỂM

- **135-150:** Deployment Expert ⭐⭐⭐
- **120-134:** Proficient ⭐⭐
- **105-119:** Competent ⭐
- **<105:** Cần review lại

**Xem SOLUTIONS.md để check đáp án!**
