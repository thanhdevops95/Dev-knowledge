# 📋 DevOps Cheatsheets

> **Quick reference cho các công cụ DevOps phổ biến**

---

## Mục lục

1. [Linux Commands](#linux-commands)
2. [Docker Commands](#docker-commands)
3. [Kubernetes Commands](#kubernetes-commands)
4. [Git Commands](#git-commands)
5. [Networking Commands](#networking-commands)
6. [Shell Scripting](#shell-scripting)

---

## Linux Commands

### Navigation & Files

```bash
pwd                     # Print working directory
ls -la                  # List all files with details
cd /path/to/dir         # Change directory
cd ..                   # Go up one level
cd ~                    # Go to home directory

mkdir -p dir/subdir     # Create nested directories
touch file.txt          # Create empty file
cp -r src dest          # Copy recursively
mv old new              # Move/rename
rm -rf dir              # Remove directory (CAREFUL!)
```

### File Content

```bash
cat file                # View entire file
less file               # View with pagination
head -20 file           # First 20 lines
tail -20 file           # Last 20 lines
tail -f file            # Follow live updates
grep "pattern" file     # Search in file
grep -r "pattern" dir   # Search recursively
```

### Permissions

```bash
chmod 755 file          # rwxr-xr-x
chmod +x file           # Add execute
chmod -R 644 dir        # Recursive
chown user:group file   # Change owner
```

### Process Management

```bash
ps aux                  # All processes
top / htop              # Live process monitor
kill PID                # Kill by PID
kill -9 PID             # Force kill
pkill name              # Kill by name
nohup cmd &             # Run in background
```

### Disk & Memory

```bash
df -h                   # Disk usage
du -sh dir              # Directory size
free -h                 # Memory usage
ncdu                    # NCurses disk usage
```

### Networking

```bash
ip addr                 # Show IP addresses
ping host               # Test connectivity
curl -I url             # HTTP headers
netstat -tuln           # Open ports
ss -tuln                # Open ports (modern)
```

---

## Docker Commands

### Images

```bash
docker images                        # List images
docker pull image:tag               # Pull image
docker build -t name:tag .          # Build image
docker rmi image                    # Remove image
docker image prune -a               # Remove unused
```

### Containers

```bash
docker ps                           # Running containers
docker ps -a                        # All containers
docker run -d --name c image        # Run detached
docker run -it image bash           # Run interactive
docker run -p 8080:80 image         # Port mapping
docker run -v /host:/container img  # Volume mount

docker stop container               # Stop container
docker start container              # Start container
docker restart container            # Restart
docker rm container                 # Remove container
docker rm -f container              # Force remove

docker logs container               # View logs
docker logs -f container            # Follow logs
docker exec -it container bash      # Execute in container
docker inspect container            # Container details
```

### Docker Compose

```bash
docker compose up -d                # Start all services
docker compose down                 # Stop all services
docker compose down -v              # Stop + remove volumes
docker compose logs                 # View logs
docker compose logs -f service      # Follow service logs
docker compose ps                   # List services
docker compose exec service cmd     # Execute in service
docker compose build                # Rebuild images
docker compose pull                 # Pull images
```

### Cleanup

```bash
docker system prune                 # Clean unused
docker system prune -a --volumes    # Clean everything
docker volume prune                 # Clean volumes
docker network prune                # Clean networks
```

---

## Kubernetes Commands

### Cluster Info

```bash
kubectl cluster-info
kubectl get nodes
kubectl get namespaces
```

### Pods

```bash
kubectl get pods                    # List pods
kubectl get pods -o wide            # With more info
kubectl get pods -n namespace       # In namespace
kubectl get pods --all-namespaces   # All namespaces
kubectl describe pod name           # Pod details
kubectl logs pod-name               # View logs
kubectl logs -f pod-name            # Follow logs
kubectl exec -it pod-name -- bash   # Exec into pod
kubectl delete pod pod-name         # Delete pod
```

### Deployments

```bash
kubectl get deployments
kubectl create deployment name --image=image
kubectl scale deployment name --replicas=3
kubectl set image deployment/name container=image:tag
kubectl rollout status deployment/name
kubectl rollout history deployment/name
kubectl rollout undo deployment/name
kubectl delete deployment name
```

### Services

```bash
kubectl get services
kubectl expose deployment name --port=80 --type=NodePort
kubectl delete service name
kubectl port-forward service/name 8080:80
```

### Apply & Delete

```bash
kubectl apply -f file.yaml
kubectl apply -f directory/
kubectl delete -f file.yaml
kubectl get all
```

### Debug

```bash
kubectl describe pod pod-name
kubectl logs pod-name --previous
kubectl get events --sort-by='.lastTimestamp'
kubectl top nodes
kubectl top pods
```

---

## Git Commands

### Setup

```bash
git config --global user.name "Name"
git config --global user.email "email@example.com"
```

### Basic Workflow

```bash
git init                            # Initialize repo
git clone url                       # Clone repo
git status                          # Check status
git add .                           # Stage all
git add file                        # Stage file
git commit -m "message"             # Commit
git push origin branch              # Push
git pull origin branch              # Pull
```

### Branches

```bash
git branch                          # List branches
git branch name                     # Create branch
git checkout name                   # Switch branch
git checkout -b name                # Create & switch
git switch name                     # Switch (modern)
git switch -c name                  # Create & switch (modern)
git merge branch                    # Merge branch
git branch -d name                  # Delete branch
```

### Undo

```bash
git restore file                    # Discard changes
git restore --staged file           # Unstage
git reset HEAD~1                    # Undo last commit (keep changes)
git reset --hard HEAD~1             # Undo last commit (discard)
git revert commit                   # Create undo commit
```

### Stash

```bash
git stash                           # Stash changes
git stash save "message"            # Stash with message
git stash list                      # List stashes
git stash pop                       # Apply and remove
git stash apply                     # Apply and keep
git stash drop                      # Remove stash
```

### Remote

```bash
git remote -v                       # List remotes
git remote add origin url           # Add remote
git fetch origin                    # Fetch changes
git pull origin branch              # Fetch + merge
git push -u origin branch           # Push with upstream
```

---

## Networking Commands

### DNS & Connectivity

```bash
ping host                           # Test connectivity
traceroute host                     # Trace route
mtr host                            # Better traceroute
nslookup domain                     # DNS lookup
dig domain                          # Detailed DNS
dig +short domain                   # Quick DNS
host domain                         # Simple DNS
```

### Ports & Connections

```bash
ss -tuln                            # Open ports
netstat -tuln                       # Open ports (legacy)
lsof -i :port                       # What's using port
curl -I url                         # HTTP headers
curl -v url                         # Verbose request
nc -zv host port                    # Check port open
```

### Firewall (UFW)

```bash
ufw status                          # Firewall status
ufw enable                          # Enable firewall
ufw allow 22                        # Allow SSH
ufw allow 80,443/tcp                # Allow HTTP/HTTPS
ufw deny 23                         # Deny telnet
ufw delete allow 80                 # Remove rule
```

---

## Shell Scripting

### Basics

```bash
#!/bin/bash                         # Shebang
set -euo pipefail                   # Strict mode

# Variables
NAME="value"
echo "$NAME"
echo "${NAME}_suffix"

# Arguments
$0                                  # Script name
$1, $2                              # First, second arg
$#                                  # Number of args
$@                                  # All args
$?                                  # Exit code
```

### Conditionals

```bash
if [ "$a" = "$b" ]; then
    echo "equal"
elif [ "$a" -gt "$b" ]; then
    echo "greater"
else
    echo "less"
fi

# File tests
[ -f file ]                         # Is file
[ -d dir ]                          # Is directory
[ -e path ]                         # Exists
[ -r file ]                         # Readable
[ -w file ]                         # Writable
[ -x file ]                         # Executable
```

### Loops

```bash
# For loop
for i in {1..10}; do
    echo "$i"
done

for file in *.txt; do
    echo "$file"
done

# While loop
while [ condition ]; do
    echo "loop"
done

# Read file
while IFS= read -r line; do
    echo "$line"
done < file.txt
```

### Functions

```bash
my_function() {
    local var=$1
    echo "Hello, $var"
    return 0
}

result=$(my_function "World")
```

---

## Quick Reference Card

### Common Ports

| Port | Service |
|------|---------|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 27017 | MongoDB |

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 301 | Moved Permanently |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Error |
| 502 | Bad Gateway |
| 503 | Service Unavailable |

### File Permissions

```
r = 4  w = 2  x = 1

755 = rwxr-xr-x
644 = rw-r--r--
777 = rwxrwxrwx
600 = rw-------
```

---

**💡 Bookmark this page for quick reference!**
