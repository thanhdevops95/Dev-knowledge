# OS Concepts

> **Tags:** `os` `process` `thread` `concurrency` `linux` `fundamentals`
> **Level:** Intermediate | **Prerequisite:** `cs/01-how-computers-work.md`

---

## 1. Process vs Thread

### Process
- **Process** là một chương trình đang chạy — có không gian địa chỉ riêng (virtual address space), file descriptors, signals handlers.
- Tạo process: `fork()` (Unix) — tạo bản sao (copy-on-write), `exec()` — thay thế image.
- **Context switch** giữa processes rất tốn kém: phải lưu/khôi phục toàn bộ CPU registers, MMU state, flush TLB.

### Thread
- **Thread** (lightweight process) chia sẻ address space, file descriptors với process cha.
- Linux không có "thread" thực sự — dùng `clone()` với flags `CLONE_VM | CLONE_FS | CLONE_FILES | CLONE_SIGHAND`.
- Context switch giữa threads cùng process: nhẹ hơn (chỉ cần lưu registers + stack pointer).

```
Process A                Process B
┌─────────────┐          ┌─────────────┐
│ Code        │          │ Code        │
│ Data        │          │ Data        │ ← Separate address space
│ Heap        │          │ Heap        │
│ Stack T1    │          │ Stack T1    │
│ Stack T2    │          └─────────────┘
└─────────────┘
  T1 và T2 share heap/code/data
```

### Khi nào dùng Process vs Thread?

| | Process | Thread |
|---|---|---|
| Isolation | ✅ Hoàn toàn tách biệt | ❌ Share memory |
| Overhead | ❌ Nặng | ✅ Nhẹ |
| Communication | IPC (pipes, sockets, shm) | Shared memory (cẩn thận race condition) |
| Crash impact | Không ảnh hưởng nhau | Crash 1 thread → crash cả process |
| Use case | Web servers (nginx), microservices | CPU-bound tasks trong 1 service |

---

## 2. Process Scheduling — Linux CFS

**Completely Fair Scheduler (CFS)** — scheduler mặc định của Linux từ 2.6.23.

### Nguyên lý
- Mỗi process có `vruntime` (virtual runtime) — thời gian CPU đã dùng, cân chỉnh theo priority (nice value).
- CFS luôn chọn process có **`vruntime` nhỏ nhất** để chạy tiếp.
- Dùng **Red-Black Tree** (self-balancing BST) để lưu các runnable tasks — O(log n) để tìm min.

```
vruntime được cập nhật:
  new_vruntime = old_vruntime + actual_runtime × (NICE_0_LOAD / task_weight)

nice -20 → weight cao → vruntime tăng chậm → được chạy nhiều hơn
nice +19 → weight thấp → vruntime tăng nhanh → ít được chạy hơn
```

### Scheduler states
```
TASK_RUNNING     — đang chạy hoặc sẵn sàng chạy (in runqueue)
TASK_INTERRUPTIBLE  — đang ngủ, có thể bị signal đánh thức
TASK_UNINTERRUPTIBLE — đang ngủ, KHÔNG bị signal (vd: chờ disk I/O) → là "D" trong ps
TASK_STOPPED     — bị SIGSTOP
TASK_ZOMBIE      — đã kết thúc nhưng parent chưa wait()
```

### Lệnh hữu ích
```bash
ps aux                    # Xem tất cả processes
ps -eLf                   # Xem threads (LWP column)
top -H                    # Hiện threads trong top
nice -n 10 ./program      # Chạy với nice value +10
renice -n -5 -p $PID      # Thay đổi nice value của PID đang chạy
chrt -f 50 ./program      # Chạy với real-time priority (FIFO, priority 50)
```

---

## 3. Inter-Process Communication (IPC)

### 3.1 Pipe (Anonymous Pipe)
```bash
ls -la | grep ".md"   # Shell pipe
```
```c
// C code
int fd[2];
pipe(fd);   // fd[0] = read end, fd[1] = write end
// Chỉ hoạt động giữa parent-child processes
```
- **Unidirectional**, kernel-buffered (~64KB default).
- Khi pipe full → writer bị block; khi pipe empty → reader bị block.

### 3.2 Named Pipe (FIFO)
```bash
mkfifo /tmp/mypipe
echo "hello" > /tmp/mypipe &   # writer
cat /tmp/mypipe                  # reader
```
- Hoạt động giữa **bất kỳ processes** nào (không cần quan hệ parent-child).
- Là file trong filesystem nhưng data không persist.

### 3.3 Unix Domain Socket
```python
# Server
import socket, os
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.bind('/tmp/my.sock')
sock.listen(1)
conn, _ = sock.accept()

# Client
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('/tmp/my.sock')
sock.send(b"hello")
```
- Nhanh hơn TCP (không qua network stack).
- Docker daemon, PostgreSQL, Redis đều dùng Unix sockets.

### 3.4 Shared Memory
```c
// POSIX shared memory
int fd = shm_open("/myshm", O_CREAT|O_RDWR, 0666);
ftruncate(fd, SIZE);
void *ptr = mmap(NULL, SIZE, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
// Cần semaphore/mutex để đồng bộ!
```
- **Nhanh nhất** — zero-copy, không qua kernel cho mỗi message.
- Nguy hiểm: cần đồng bộ cẩn thận, dễ corruption.

### 3.5 Signal
```python
import signal

def handler(signum, frame):
    print(f"Received signal {signum}")

signal.signal(signal.SIGTERM, handler)  # Graceful shutdown
signal.signal(signal.SIGINT, handler)   # Ctrl+C
signal.signal(signal.SIGUSR1, handler)  # Custom signal
```

| Signal | Số | Mô tả |
|---|---|---|
| SIGTERM | 15 | Graceful terminate (có thể catch) |
| SIGKILL | 9 | Force kill (KHÔNG thể catch/ignore) |
| SIGINT | 2 | Ctrl+C |
| SIGHUP | 1 | Hangup — reload config (nginx dùng) |
| SIGSEGV | 11 | Segmentation fault |
| SIGCHLD | 17 | Child process exited |

### So sánh IPC

| Method | Speed | Complexity | Cross-machine |
|---|---|---|---|
| Pipe | Nhanh | Đơn giản | ❌ |
| FIFO | Nhanh | Đơn giản | ❌ |
| Unix Socket | Rất nhanh | Trung bình | ❌ |
| Shared Memory | Nhanh nhất | Phức tạp | ❌ |
| TCP Socket | Chậm hơn | Trung bình | ✅ |
| Message Queue | Trung bình | Đơn giản | ✅ (distributed) |

---

## 4. File System — inode

### inode là gì?
- **inode** (index node) = metadata của file, lưu trong inode table.
- **Không** chứa tên file hay data — chỉ chứa: permissions, owner (UID/GID), timestamps, size, và **block pointers**.

```
Filename → inode number → inode → data blocks
  "foo.txt"     12345     ┌──────────────────┐     ┌──────┐
                          │ mode: 0644        │ ──▶ │ data │
                          │ uid: 1000         │     └──────┘
                          │ size: 4096        │
                          │ blocks: [10,11,12]│
                          └──────────────────┘
```

### Hard link vs Soft link
```bash
ln file.txt hardlink.txt      # Hard link: cùng inode
ln -s file.txt symlink.txt    # Symlink: inode khác, trỏ đến path

stat file.txt    # Xem inode number: "Inode: 12345"
ls -i            # Hiện inode numbers
```
- **Hard link**: xóa file gốc → hard link vẫn truy cập được (cùng inode, data chỉ bị xóa khi link count = 0).
- **Symlink**: xóa file gốc → symlink bị broken.

### Filesystem types
```
ext4    — Linux default, journaling, max 1EB volume
XFS     — High-performance, large files, RHEL default
Btrfs   — CoW, snapshots, RAID, checksumming
tmpfs   — In-memory, mất khi reboot (/tmp, /dev/shm)
procfs  — Virtual FS, /proc — thông tin về processes
sysfs   — Virtual FS, /sys — thông tin hardware/kernel
```

---

## 5. cgroups & Namespaces (Cơ sở của Docker)

### Namespaces — Isolation
Linux namespaces cô lập tài nguyên giữa các groups of processes:

| Namespace | Flag | Isolates |
|---|---|---|
| **PID** | CLONE_NEWPID | Process IDs — container thấy PID 1 là process của nó |
| **Network** | CLONE_NEWNET | Network interfaces, routes, iptables |
| **Mount** | CLONE_NEWNS | Filesystem mounts — container có / riêng |
| **UTS** | CLONE_NEWUTS | hostname, domain name |
| **IPC** | CLONE_NEWIPC | Shared memory, semaphores |
| **User** | CLONE_NEWUSER | UID/GID mapping — root trong container ≠ root trên host |

```bash
# Xem namespaces của process
ls -la /proc/$PID/ns/

# Chạy command trong namespace mới
unshare --pid --fork --mount-proc bash

# nsenter — vào namespace của container đang chạy
nsenter -t $PID -n -u    # vào network + UTS namespace
```

### cgroups — Resource Limits
**Control Groups** giới hạn tài nguyên (CPU, memory, I/O, network):

```bash
# cgroups v2 (systemd-based)
# Xem cgroup của process
cat /proc/$PID/cgroup

# Docker tự động tạo cgroups:
# /sys/fs/cgroup/memory/docker/$CONTAINER_ID/memory.limit_in_bytes
docker run --memory=512m --cpus=2.0 nginx

# Systemd cgroup
systemctl set-property httpd.service MemoryMax=512M CPUQuota=200%
```

---

## 6. Virtual Memory

```
Virtual Address Space (per process, 64-bit: 128TB)
┌─────────────────┐ 0xFFFFFFFFFFFFFFFF
│  Kernel Space   │ (mỗi process đều map kernel ở đây)
├─────────────────┤ 0x0000800000000000
│  Stack          │ ↓ grows down
│  ...            │
│  Heap           │ ↑ grows up (malloc/mmap)
│  BSS            │ uninitialized global vars
│  Data           │ initialized global vars
│  Text (Code)    │ read-only executable
└─────────────────┘ 0x0000000000000000
```

### Page Fault
1. CPU truy cập virtual address → MMU tra page table
2. Nếu page không có trong RAM → **page fault** → kernel ISR
3. Kernel tìm page trong swap/file → load vào RAM → update page table
4. Resume instruction

### Memory-mapped files
```python
import mmap

with open("bigfile.bin", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    data = mm[0:100]    # Đọc như bytes, kernel tự quản lý pages
    mm.close()
```

---

## 7. System Calls

```
User Space:  printf("hello") → glibc → write() wrapper
              ─────────────────────────────────────────
Kernel Space:  sys_write() → VFS → filesystem driver → disk
```

```bash
# Trace system calls của một process
strace ls /tmp
strace -p $PID         # Attach to running process
strace -c ls           # Count syscalls (statistics)

# Kết quả strace:
execve("/usr/bin/ls", ["ls"], ...) = 0
openat(AT_FDCWD, "/tmp", O_RDONLY|O_DIRECTORY) = 3
getdents64(3, ..., 32768) = ...
write(1, "file1.txt\n", 10) = 10
```

---

## 8. Cheatsheet nhanh

```bash
# Processes
ps aux                   # All processes
ps -eLf                  # All threads
pgrep -f nginx           # Find PID by name
kill -SIGTERM $PID       # Graceful kill
kill -9 $PID             # Force kill
pkill -f "python app"    # Kill by name

# CPU & Memory
top / htop               # Live monitor
vmstat 1                 # Memory stats every 1s
free -h                  # RAM usage
cat /proc/$PID/status    # Process details

# File Descriptors
lsof -p $PID             # Files opened by process
lsof -i :8080            # What's listening on port 8080
ulimit -n                # Max open files per process

# Cgroups
systemd-cgtop            # Live cgroup resource usage
cat /sys/fs/cgroup/memory/.../memory.usage_in_bytes
```

---

## 9. Glossary

| Thuật ngữ | Giải thích |
|---|---|
| **PCB** | Process Control Block — kernel struct lưu state của process |
| **Context switch** | Lưu CPU state của process cũ, load state của process mới |
| **Scheduler** | Kernel module quyết định process nào chạy tiếp |
| **vruntime** | Virtual runtime dùng bởi CFS để cân bằng CPU time |
| **inode** | Metadata của file, không chứa tên hay data |
| **Page fault** | CPU truy cập page không có trong RAM |
| **cgroup** | Giới hạn tài nguyên cho group of processes |
| **Namespace** | Cô lập tài nguyên hệ thống giữa processes |
| **Zombie** | Process đã chết nhưng entry còn trong process table |
| **Orphan** | Process có parent đã chết, được adopt bởi init (PID 1) |

---

## 10. Bài tập thực hành

1. **Process lifecycle**: Viết C program dùng `fork()`, `exec()`, `wait()` — tạo child process chạy `ls -la`.
2. **IPC with pipe**: Tạo parent-child communication qua pipe.
3. **Named pipe**: Tạo 2 Python scripts giao tiếp qua FIFO.
4. **strace exploration**: Chạy `strace -c python3 -c "import requests"` — xem syscalls nào tốn nhiều nhất.
5. **cgroup limit**: Dùng Docker, chạy `stress --vm 1 --vm-bytes 1G` trong container với `--memory=512m`, quan sát OOM kill.
6. **inode discovery**: `ls -i /etc/hosts` → `stat /etc/hosts` → tìm hiểu hard link count.

---

*Tài liệu liên quan: `cs/03-concurrency-parallelism.md` | `linux/01-linux-essentials.md` | `linux/02-linux-administration.md`*
