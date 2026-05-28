# Scenarios: Module 08 - DEPLOYMENT

> **8 Tình huống Deployment thực tế trong Production**

---

## 🎬 Scenario 1: "Midnight Deployment Disaster"

### Tình huống

Deploy lúc 2 giờ sáng, site down, users phàn nàn.

### Vấn đề

- New code phụ thuộc DB column chưa tồn tại
- Migration chưa chạy

### Giải pháp

1. Emergency rollback
2. Chạy migration
3. Redeploy

### Phòng tránh

✅ Luôn migrate TRƯỚC deploy code  
✅ Test migration trên staging  
✅ Deploy checklist  

---

## 🔀 Scenario 2: "The Half-Deployed State"

### Tình huống

Deployment dừng giữa chừng. 2 servers v1.0, 1 server v2.0.

### Vấn đề

Users nhận inconsistent responses.

### Giải pháp

- Complete deployment tất cả 3 servers
- HOẶC rollback tất cả về v1.0

### Phòng tránh

✅ Automated all-or-nothing deployment  
✅ Atomic deployment scripts  

---

## ⚙️ Scenario 3: "The Config Mismatch"

### Tình huống

App crash trong production, works trong staging.

### Vấn đề

Production .env thiếu new required variables.

### Giải pháp

- Add missing env vars
- Restart service

### Phòng tránh

✅ Validate .env trước deployment  
✅ Environment diff check trong CI  

---

## 🔙 Scenario 4: "The Impossible Rollback"

### Tình huống

Cần rollback nhưng database migration không thể undo.

### Vấn đề

Đã drop column chứa important data.

### Giải pháp

- Restore từ backup (hours of downtime)

### Phòng tránh

✅ LUÔN forward-compatible migrations  
✅ Never drop trong production ngay lập tức  
✅ Two-step approach: deprecate → remove later  

---

## 💾 Scenario 5: "The Memory Leak Discovery"

### Tình huống

New version slowly consuming tất cả memory.

### Vấn đề

Memory leak trong new code.

### Giải pháp

1. Monitor shows memory climbing
2. Quick rollback
3. Fix trong v2.1

### Phòng tránh

✅ Canary deployment catches sớm!  
✅ Memory monitoring với alerts  

---

## ⏱️ Scenario 6: "The Zero-Downtime Failure"

### Tình huống

Cố gắng zero-downtime, nhưng users thấy 502 errors.

### Vấn đề

New version chưa healthy trước khi switch traffic.

### Giải pháp

- Add health check gates
- Đợi healthy trước switch

### Phòng tránh

✅ Health check PHẢI pass trước switch  
✅ Automated health verification  

---

## 🗄️ Scenario 7: "The Database Lock"

### Tình huống

Migration lock database 30 phút.

### Vấn đề

Long-running ALTER TABLE trên huge table.

### Giải pháp

- Dùng online schema change tools (pt-osc, gh-ost)
- Hoặc maintenance window

### Phòng tránh

✅ Test migrations trên production-size data!  
✅ Online DDL tools cho large tables  

---

## ✅ Scenario 8: "The Successful Blue-Green"

### Tình huống

Major version upgrade cần.

### Giải pháp hoàn hảo

1. Deploy v2.0 lên Green
2. Test thoroughly
3. Switch traffic
4. Monitor 24 giờ
5. Remove Blue

### Kết quả

- ZERO downtime
- Instant rollback sẵn sàng
- Users không nhận ra

---

## 🎓 KEY LESSONS

1. **Migrate TRƯỚC deploy code**
2. **Forward-compatible migrations**
3. **Health check gates**
4. **Rollback plan luôn sẵn sàng**
5. **Test với production-size data**
6. **Automate everything**
7. **Canary cho risky changes**
8. **Monitor sau mỗi deployment**
