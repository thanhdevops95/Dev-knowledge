# ⚡ QUICK REFERENCE - CHEAT SHEET

## 📌 MỤC ĐÍCH
Tài liệu tham khảo nhanh các lệnh thường dùng trong khóa học. Bookmark file này để tra cứu!

---

## 🐳 DOCKER COMMANDS

### Container Management
```bash
# Xem containers đang chạy
docker ps

# Xem tất cả containers (cả đã dừng)
docker ps -a

# Chạy container
docker run -d --name my-app -p 8080:80 nginx

# Dừng container
docker stop my-app

# Khởi động lại
docker restart my-app

# Xóa container
docker rm my-app

# Xóa container đang chạy (force)
docker rm -f my-app

# Xem log
docker logs my-app

# Xem log realtime
docker logs -f my-app

# Vào trong container (interactive shell)
docker exec -it my-app sh
# hoặc
docker exec -it my-app bash
```

### Image Management
```bash
# Xem danh sách images
docker images

# Build image
docker build -t my-image:v1 .

# Build với Dockerfile khác
docker build -t my-image:v1 -f Dockerfile.dev .

# Pull image từ Docker Hub
docker pull nginx:alpine

# Push image lên Docker Hub
docker push username/my-image:v1

# Xóa image
docker rmi my-image:v1

# Xóa tất cả images không dùng
docker image prune -a
```

### Network
```bash
# Tạo network
docker network create my-network

# Xem danh sách networks
docker network ls

# Xem chi tiết network
docker network inspect my-network

# Kết nối container vào network
docker network connect my-network my-container

# Xóa network
docker network rm my-network
```

### Volume
```bash
# Tạo volume
docker volume create my-volume

# Xem danh sách volumes
docker volume ls

# Xem chi tiết volume
docker volume inspect my-volume

# Xóa volume
docker volume rm my-volume

# Xóa tất cả volumes không dùng
docker volume prune
```

### System Cleanup
```bash
# Xóa tất cả containers đã dừng
docker container prune

# Xóa tất cả images không dùng
docker image prune -a

# Xóa tất cả volumes không dùng
docker volume prune

# Xóa tất cả (containers, images, volumes, networks)
docker system prune -a --volumes
```

---

## 🐳 DOCKER COMPOSE COMMANDS

```bash
# Khởi động tất cả services (detached mode)
docker compose up -d

# Khởi động và rebuild images
docker compose up -d --build

# Xem log tất cả services
docker compose logs

# Xem log 1 service cụ thể
docker compose logs backend

# Xem log realtime
docker compose logs -f

# Xem trạng thái services
docker compose ps

# Dừng tất cả services
docker compose stop

# Dừng và xóa containers
docker compose down

# Dừng, xóa containers + volumes
docker compose down -v

# Restart 1 service
docker compose restart backend

# Chạy lệnh trong service
docker compose exec backend sh

# Pull images mới nhất
docker compose pull

# Xem config đã parse
docker compose config
```

---

## ☸️ KUBERNETES (kubectl) COMMANDS

### Pod Management
```bash
# Xem tất cả pods
kubectl get pods

# Xem pods với thông tin chi tiết
kubectl get pods -o wide

# Xem pods trong namespace cụ thể
kubectl get pods -n monitoring

# Xem chi tiết pod
kubectl describe pod my-pod

# Xem log pod
kubectl logs my-pod

# Xem log container cụ thể trong pod
kubectl logs my-pod -c container-name

# Xem log realtime
kubectl logs -f my-pod

# Vào trong pod
kubectl exec -it my-pod -- sh

# Xóa pod
kubectl delete pod my-pod

# Xóa pod ngay lập tức (force)
kubectl delete pod my-pod --force --grace-period=0
```

### Deployment Management
```bash
# Xem deployments
kubectl get deployments

# Tạo deployment từ file
kubectl apply -f deployment.yaml

# Xem chi tiết deployment
kubectl describe deployment my-deployment

# Scale deployment
kubectl scale deployment my-deployment --replicas=5

# Cập nhật image
kubectl set image deployment/my-deployment container-name=new-image:v2

# Xem lịch sử rollout
kubectl rollout history deployment/my-deployment

# Rollback về version trước
kubectl rollout undo deployment/my-deployment

# Xóa deployment
kubectl delete deployment my-deployment
```

### Service Management
```bash
# Xem services
kubectl get services
# hoặc
kubectl get svc

# Tạo service
kubectl apply -f service.yaml

# Xem chi tiết service
kubectl describe service my-service

# Xóa service
kubectl delete service my-service

# Port forward (truy cập service từ local)
kubectl port-forward service/my-service 8080:80
```

### Namespace
```bash
# Xem namespaces
kubectl get namespaces

# Tạo namespace
kubectl create namespace my-namespace

# Xóa namespace (cẩn thận!)
kubectl delete namespace my-namespace

# Set namespace mặc định
kubectl config set-context --current --namespace=my-namespace
```

### Apply/Delete Resources
```bash
# Apply tất cả files trong folder
kubectl apply -f k8s/

# Apply 1 file
kubectl apply -f deployment.yaml

# Xóa resources từ file
kubectl delete -f deployment.yaml

# Xóa tất cả resources trong namespace
kubectl delete all --all -n my-namespace
```

### Debugging
```bash
# Xem events
kubectl get events --sort-by=.metadata.creationTimestamp

# Xem resource usage
kubectl top nodes
kubectl top pods

# Xem logs của pod đã crash
kubectl logs my-pod --previous

# Describe để xem lỗi
kubectl describe pod my-pod
```

---

## 🔧 GIT COMMANDS

```bash
# Clone repo
git clone https://gitlab.com/username/repo.git

# Xem trạng thái
git status

# Thêm file vào staging
git add .
git add filename.txt

# Commit
git commit -m "Message"

# Push lên remote
git push origin main

# Pull từ remote
git pull origin main

# Xem lịch sử commit
git log
git log --oneline

# Tạo branch mới
git checkout -b feature-branch

# Chuyển branch
git checkout main

# Merge branch
git merge feature-branch

# Xem remote
git remote -v

# Thêm remote
git remote add origin https://...
```

---

## 🐍 PYTHON COMMANDS

```bash
# Kiểm tra version
python --version
python3 --version

# Tạo virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Deactivate venv
deactivate

# Cài packages
pip install flask
pip install -r requirements.txt

# Xem packages đã cài
pip list
pip freeze

# Tạo requirements.txt
pip freeze > requirements.txt

# Chạy Python file
python app.py
```

---

## 🔷 GO COMMANDS

```bash
# Kiểm tra version
go version

# Khởi tạo module
go mod init github.com/username/project

# Tải dependencies
go get github.com/gin-gonic/gin

# Tải tất cả dependencies trong go.mod
go mod download

# Dọn dẹp dependencies không dùng
go mod tidy

# Chạy code
go run main.go

# Build binary
go build -o app main.go

# Chạy tests
go test ./...

# Format code
go fmt ./...

# Kiểm tra lỗi
go vet ./...
```

---

## 🗄️ MYSQL COMMANDS

```bash
# Kết nối MySQL (trong container)
docker exec -it mysql-container mysql -u root -p

# Trong MySQL shell:
# Xem databases
SHOW DATABASES;

# Chọn database
USE todo_db;

# Xem tables
SHOW TABLES;

# Xem cấu trúc table
DESCRIBE todos;

# Query data
SELECT * FROM todos;
SELECT * FROM todos WHERE completed = true;

# Insert data
INSERT INTO todos (id, title, completed) VALUES ('123', 'Test', false);

# Update data
UPDATE todos SET completed = true WHERE id = '123';

# Delete data
DELETE FROM todos WHERE id = '123';

# Thoát
EXIT;
```

---

## 🔍 CURL COMMANDS (API Testing)

```bash
# GET request
curl http://localhost:8080/api/todos

# GET với headers
curl -H "Authorization: Bearer token123" http://localhost:8080/api/todos

# POST request (JSON)
curl -X POST http://localhost:8080/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"New Todo"}'

# PUT request
curl -X PUT http://localhost:8080/api/todos/123 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated","completed":true}'

# DELETE request
curl -X DELETE http://localhost:8080/api/todos/123

# Hiển thị headers trong response
curl -i http://localhost:8080/api/todos

# Chỉ hiển thị status code
curl -o /dev/null -s -w "%{http_code}\n" http://localhost:8080/api/todos

# Lưu response vào file
curl http://localhost:8080/api/todos -o response.json

# Follow redirects
curl -L http://localhost:8080/api/todos
```

---

## 🛠️ SYSTEM COMMANDS

### Kiểm tra Port
```bash
# Windows
netstat -ano | findstr :8080

# macOS/Linux
lsof -i :8080
netstat -tuln | grep 8080
```

### Kill Process
```bash
# Windows
taskkill /PID 1234 /F

# macOS/Linux
kill -9 1234
```

### Xem Resource Usage
```bash
# CPU, RAM
top
htop  # (nếu đã cài)

# Disk
df -h

# Docker resource
docker stats
```

---

## 📝 TIPS & TRICKS

### Alias hữu ích (thêm vào ~/.bashrc hoặc ~/.zshrc)
```bash
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kl='kubectl logs'
alias dc='docker compose'
alias dps='docker ps'
alias dim='docker images'
```

### Xem IP của container
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container-name
```

### Copy file vào/ra container
```bash
# Copy vào container
docker cp local-file.txt container-name:/path/in/container/

# Copy ra khỏi container
docker cp container-name:/path/in/container/file.txt ./local-path/
```

---

**💡 Pro Tip:** Bấm `Ctrl + R` trong terminal để search lịch sử lệnh đã chạy!
