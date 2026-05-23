# Quiz: Module 08 - DEPLOYMENT

> **20 Câu Trắc Nghiệm Kiểm Tra Kiến Thức Deployment**

**Thời gian:** 20 phút  
**Đạt:** 14/20 (70%)

---

## 📝 CÂU HỎI

**Câu 1:** Strategy tốt nhất cho zero-downtime deployment?

- A) Stop old, start new
- B) Blue-green deployment
- C) Đợi nửa đêm
- D) Tell users để chờ

**Câu 2:** Rolling deployment làm gì?

- A) Update tất cả cùng lúc
- B) Update từng instance một
- C) Roll back changes
- D) Rotate logs

**Câu 3:** Canary deployment nghĩa là:

- A) Deploy cho 100% users
- B) Deploy cho % nhỏ users trước
- C) Deploy với birds
- D) Deploy on weekends

**Câu 4:** systemd `Restart=always` làm gì?

- A) Restart một lần
- B) Auto-restart khi crash và boot
- C) Không restart
- D) Restart daily

**Câu 5:** Environment variables best practice:

- A) Hardcode trong code
- B) .env files + gitignore
- C) GitHub public
- D) Share trên Slack

**Câu 6:** Health check healthy HTTP code:

- A) 500
- B) 404
- C) 200
- D) 301

**Câu 7:** Database migration nên:

- A) DROP immediately
- B) Forward-compatible
- C) Skip backup
- D) Only in production

**Câu 8:** Quick rollback cần:

- A) Previous version ready
- B) Rewrite entire code
- C) Full database restore
- D) Manager approval

**Câu 9:** Blue-green dùng:

- A) 1 server
- B) 2 parallel environments
- C) 3 environments
- D) Color coding

**Câu 10:** Zero-downtime key requirement:

- A) Stop all first
- B) Health checks + gradual switch
- C) Maintenance page
- D) Email users

**Câu 11:** Trước deploy new version, nên:

- A) Pray
- B) Test on staging
- C) Skip tests
- D) Deploy Friday 5pm

**Câu 12:** Deployment script nên:

- A) Manual steps only
- B) Fully automated với rollback
- C) No error handling
- D) Run as root always

**Câu 13:** After deployment, first thing:

- A) Go home
- B) Monitor logs và metrics
- C) Delete old version
- D) Celebrate

**Câu 14:** Environment file (.env) nên:

- A) Commit to git
- B) In .gitignore
- C) Email to team
- D) Post on Slack

**Câu 15:** systemd service logs xem bằng:

- A) `cat logs`
- B) `journalctl -u service_name`
- C) `docker logs`
- D) `nginx logs`

**Câu 16:** Best time to deploy risky changes:

- A) Friday 5pm
- B) Monday morning với team ready
- C) Midnight alone
- D) During holiday

**Câu 17:** Migration breaks old code, solution:

- A) Force users update
- B) Two-step migration approach
- C) Skip migration
- D) Hope for best

**Câu 18:** Canary percentage thường bắt đầu:

- A) 100%
- B) 1-5%
- C) 50%
- D) 0%

**Câu 19:** Rollback script nên:

- A) Be complex
- B) Simple và tested
- C) Manual only
- D) Require database changes

**Câu 20:** Health check endpoint nên check:

- A) Only HTTP response
- B) Database + dependencies + resources
- C) User count
- D) Server location

---

## 📊 ĐÁP ÁN

1. B
2. B
3. B
4. B
5. B
6. C
7. B
8. A
9. B
10. B
11. B
12. B
13. B
14. B
15. B
16. B
17. B
18. B
19. B
20. B

---

## 🎯 THANG ĐIỂM

- **18-20:** Deployment Expert ⭐⭐⭐
- **15-17:** Proficient ⭐⭐
- **14:** Pass ⭐
- **<14:** Cần review
