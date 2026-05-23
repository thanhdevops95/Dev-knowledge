# Bài #12 — Sử Dụng `kubectl exec` (Chui Vào Container)

> 🎯 Command **debug power** — chui vào container đang chạy giống như SSH.

---

## 📋 Metadata

- **Bài số:** #12
- **Module:** 03-pod-and-kubectl
- **Cấp độ:** `BEGINNER`
- **Thời lượng video gốc:** ~2 phút
- **Prerequisites:** [Bài #11 — kubectl logs](02-kubectl-logs.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Mở **interactive shell** trong container đang chạy
- [ ] Chạy command đơn lẻ (one-shot) trong container
- [ ] Truy cập file system của container
- [ ] Biết khi nào dùng `bash` vs `sh`

---

## 📚 Nội Dung

### 1. Vì Sao Cần `kubectl exec`?

Trong dev/debug, bạn cần kiểm tra **bên trong container**:
- File config có đúng không?
- Code có đúng version không?
- Process đang chạy?
- Environment variables?
- Network kết nối được không?

`kubectl exec` chính là cánh cửa vào!

```
   Bạn (local machine)
        │
        │ kubectl exec
        ▼
   API Server → kubelet → Container Runtime
        │
        ▼
   ┌─── Container ─────┐
   │  $ ls             │
   │  $ cat config.yml │  ← Bạn đang ở ĐÂY
   │  $ env             │
   └───────────────────┘
```

---

### 2. Cú Pháp

```bash
kubectl exec [-it] <pod-name> [-c <container>] -- <command>
```

- `-i` = interactive (giữ stdin mở)
- `-t` = TTY (giả lập terminal)
- `-it` = thường đi cùng (cho shell tương tác)
- `--` = phân cách với command muốn chạy

---

### 3. Các Use Cases Phổ Biến

#### 🟢 Mở Interactive Shell (giống SSH)

```bash
# Pod có sh
kubectl exec -it app-1 -- sh

# Pod có bash (vd: ubuntu, debian image)
kubectl exec -it app-1 -- bash

# Pod multi-container
kubectl exec -it app-1 -c logger -- sh
```

Sau khi vào → shell prompt:

```bash
$ kubectl exec -it app-1 -- sh
/ # ls
bin   dev   etc   home   tmp   ...
/ # cat /etc/hosts
127.0.0.1   localhost
/ # exit
```

> 💡 **Mẹo:** Image `nginx:alpine` không có `bash`, chỉ có `sh`. Image `ubuntu` có cả 2.

#### 🟢 Chạy 1 Command (One-shot)

```bash
# List file trong /app
kubectl exec app-1 -- ls /app

# Cat 1 file
kubectl exec app-1 -- cat /app/config.json

# Xem env variable
kubectl exec app-1 -- env

# Test network
kubectl exec app-1 -- ping -c 3 google.com
kubectl exec app-1 -- curl http://other-service:8080
```

> Không cần `-it` cho one-shot command, nhưng vẫn được phép.

#### 🟢 Multi-line Command

```bash
kubectl exec -it app-1 -- sh -c "ls /app && cat /app/version.txt"
```

---

### 4. Use Case Hay: Debug DNS / Network

```bash
# Test DNS resolution
kubectl exec -it app-1 -- nslookup kubernetes.default.svc.cluster.local

# Test connect đến service khác
kubectl exec -it app-1 -- curl http://my-service.default.svc.cluster.local
```

> 💡 Image debug đầy đủ tools: `nicolaka/netshoot`. Khi cần troubleshoot mạng, deploy 1 Pod tạm với image này.

```bash
kubectl run -it --rm netshoot --image=nicolaka/netshoot -- bash
# bên trong có sẵn: dig, curl, nslookup, traceroute, tcpdump, iperf...
```

---

## 💻 Hands-On / Demo

```bash
# 1. Tạo Pod
kubectl run app-1 --image=nginx

# 2. Chui vào container
kubectl exec -it app-1 -- sh

# 3. Trong container — gõ thử các command:
ls
cat /etc/nginx/nginx.conf
ps aux
curl http://localhost
exit

# 4. One-shot version
kubectl exec app-1 -- ls /usr/share/nginx/html
kubectl exec app-1 -- cat /etc/os-release

# 5. Cleanup
kubectl delete pod app-1
```

**Output mẫu:**

```
$ kubectl exec app-1 -- cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"
NAME="Debian GNU/Linux"
VERSION_ID="12"
...
```

---

## ⚠️ Lưu Ý

- 🔒 **Production:** hạn chế `kubectl exec` — log lại ai exec vào container.
- 🔥 Một số image rất gọn (`distroless`, `scratch`) **KHÔNG có shell** → exec sh sẽ lỗi.
- 🔥 Multi-container Pod → bắt buộc `-c <container-name>`.
- ⚠️ Khi container crash, exec không vào được — phải dùng `kubectl logs --previous`.
- ⚠️ Mọi thay đổi bên trong container (vd: `vi config.yml`) sẽ **MẤT** khi Pod restart!

---

## ✅ Self-Check

1. **Lệnh nào mở shell tương tác trong Pod?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl exec -it <pod-name> -- sh
   # hoặc
   kubectl exec -it <pod-name> -- bash
   ```

   </details>

2. **Hai cờ `-i` và `-t` có tác dụng gì?**
   <details>
   <summary>Đáp án</summary>
   - `-i` (interactive): giữ stdin mở, để bạn gõ input
   - `-t` (TTY): giả lập terminal
   Đi cùng nhau cho shell tương tác.
   </details>

3. **Pod multi-container, lệnh thiếu gì sau đây sẽ lỗi: `kubectl exec -it app-1 -- sh`?**
   <details>
   <summary>Đáp án</summary>
   Thiếu `-c <container-name>` để chỉ định container nào.
   </details>

4. **Image nào KHÔNG có shell?**
   <details>
   <summary>Đáp án</summary>
   `distroless`, `scratch`, một số image bảo mật cao. Khi đó exec sh sẽ lỗi `executable file not found`.
   </details>

5. **Sửa file config bên trong container, restart Pod thì sao?**
   <details>
   <summary>Đáp án</summary>
   **Mất hết** — container ephemeral. Muốn config persistent → dùng ConfigMap, Secret, hoặc Volume.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #11 — kubectl logs](02-kubectl-logs.md)
- ➡️ [Bài #33 — Curl Pod (test cross-namespace)](04-curl-pod.md)

### Tài Nguyên

- 📖 [kubectl exec reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#exec)
- 📖 [netshoot image](https://github.com/nicolaka/netshoot)
- 📺 Video gốc: `Decopy_✅ #12 _ Sử Dụng kubectl exec..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"`exec` rất phổ biến nếu các bạn muốn chạy 1 script bên trong nội tại của container — hoặc xem code mình viết như thế nào."*

> 💬 *"Các bạn có thể `cat index.js` để xem phần code mình viết — debug nhanh khi nghi ngờ code sai."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
