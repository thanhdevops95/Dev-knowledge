# DOCKER

# Docker --help

```bash
docker --help

# Output:
Usage:  docker [OPTIONS] COMMAND

A self-sufficient runtime for containers

Common Commands:
  run         Create and run a new container from an image
  exec        Execute a command in a running container
  ps          List containers
  build       Build an image from a Dockerfile
  bake        Build from a file
  pull        Download an image from a registry
  push        Upload an image to a registry
  images      List images
  login       Authenticate to a registry
  logout      Log out from a registry
  search      Search Docker Hub for images
  version     Show the Docker version information
  info        Display system-wide information

Management Commands:
  agent*      Docker AI Agent Runner
  ai*         Docker AI Agent - Ask Gordon
  builder     Manage builds
  buildx*     Docker Buildx
  compose*    Docker Compose
  container   Manage containers
  context     Manage contexts
  debug*      Get a shell into any image or container
  desktop*    Docker Desktop commands
  dhi*        CLI for managing Docker Hardened Images
  extension*  Manages Docker extensions
  image       Manage images
  init*       Creates Docker-related starter files for your project
  manifest    Manage Docker image manifests and manifest lists
  mcp*        Docker MCP Plugin
  model*      Docker Model Runner
  network     Manage networks
  offload*    Docker Offload
  plugin      Manage plugins
  sandbox*    Docker Sandbox
  sbom*       View the packaged-based Software Bill Of Materials (SBOM) for an image
  scout*      Docker Scout
  system      Manage Docker
  volume      Manage volumes

Swarm Commands:
  swarm       Manage Swarm

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  commit      Create a new image from a container's changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
  diff        Inspect changes to files or directories on a container's filesystem
  events      Get real time events from the server
  export      Export a container's filesystem as a tar archive
  history     Show the history of an image
  import      Import the contents from a tarball to create a filesystem image
  inspect     Return low-level information on Docker objects
  kill        Kill one or more running containers
  load        Load an image from a tar archive or STDIN
  logs        Fetch the logs of a container
  pause       Pause all processes within one or more containers
  port        List port mappings or a specific mapping for the container
  rename      Rename a container
  restart     Restart one or more containers
  rm          Remove one or more containers
  rmi         Remove one or more images
  save        Save one or more images to a tar archive (streamed to STDOUT by default)
  start       Start one or more stopped containers
  stats       Display a live stream of container(s) resource usage statistics
  stop        Stop one or more running containers
  tag         Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE
  top         Display the running processes of a container
  unpause     Unpause all processes within one or more containers
  update      Update configuration of one or more containers
  wait        Block until one or more containers stop, then print their exit codes

Global Options:
      --config string      Location of client config files (default "/Users/rom/.docker")
  -c, --context string     Name of the context to use to connect to the daemon (overrides DOCKER_HOST env var and default
                           context set with "docker context use")
  -D, --debug              Enable debug mode
  -H, --host string        Daemon socket to connect to
  -l, --log-level string   Set the logging level ("debug", "info", "warn", "error", "fatal") (default "info")
      --tls                Use TLS; implied by --tlsverify
      --tlscacert string   Trust certs signed only by this CA (default "/Users/rom/.docker/ca.pem")
      --tlscert string     Path to TLS certificate file (default "/Users/rom/.docker/cert.pem")
      --tlskey string      Path to TLS key file (default "/Users/rom/.docker/key.pem")
      --tlsverify          Use TLS and verify the remote
  -v, --version            Print version information and quit

Run 'docker COMMAND --help' for more information on a command.

For more help on how to use Docker, head to https://docs.docker.com/go/guides/
```

## Giải thích nhanh (Cheatsheet)

### Công cụ chính: Docker CLI
- **docker**: CLI tool để quản lý containers, images, networks, volumes

### Common Commands - Làm việc với containers
- **docker run**: Tạo và chạy container mới từ image (lệnh quan trọng nhất)
- **docker exec**: Chạy command trong container đang chạy
- **docker ps**: Liệt kê containers (dùng `-a` để xem tất cả)
- **docker build**: Build image từ Dockerfile
- **docker pull**: Tải image từ registry (Docker Hub)
- **docker push**: Upload image lên registry
- **docker images**: Liệt kê local images
- **docker rm**: Xóa container
- **docker rmi**: Xóa image
- **docker stop/start/restart**: Điều khiển container lifecycle

### Management Commands - Quản lý Docker
- **docker compose**: Quản lý multi-container apps với docker-compose.yml
- **docker network**: Quản lý networks
- **docker volume**: Quản lý volumes (persistent storage)
- **docker system**: System-wide info và cleanup
- **docker context**: Quản lý contexts (kết nối đến different Docker daemons)
- **docker image**: Quản lý images (pull, tag, push, rm, ...)

### Các lệnh container khác
- **docker create**: Tạo container nhưng không chạy
- **docker commit**: Tạo image từ container changes (như snapshot)
- **docker cp**: Copy files giữa host và container
- **docker logs**: Xem logs của container
- **docker inspect**: Xem chi tiết JSON của container/image
- **docker stats**: Xem CPU, memory, network usage real-time

### Global Options
- `--config`: Thư mục config (mặc định ~/.docker)
- `-c, --context`: Chọn context/daemon để connect
- `-D, --debug`: Bật debug mode
- `-l, --log-level`: Set log level
- `-v, --version`: Show version
- TLS options: Dùng khi kết nối remote daemon với TLS

### Workflow cơ bản
```
1. docker pull <image>           # Tải image
2. docker run -p 8080:80 <image> # Chạy container (map port 8080 host → 80 container)
3. docker ps                     # Xem containers chạy
4. docker exec -it <id> /bin/bash # Vào container shell
5. docker stop <id>              # Dừng container
6. docker rm <id>                # Xóa container
```

---

## docker run

**Mục đích**: Tạo và chạy container mới từ image. Lệnh quan trọng nhất.

### Syntax cơ bản
```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```
- **IMAGE**: Tên image (bắt buộc), ví dụ: `nginx`, `ubuntu:latest`, `nginx:alpine`
- **COMMAND**: Ghi đè lệnh mặc định của image (optional)
- **ARG**: Arguments cho COMMAND

**Ví dụ đơn giản**:
```bash
docker run nginx                    # Chạy nginx với entrypoint mặc định
docker run ubuntu echo "Hello"      # Chạy ubuntu, thực thi echo thay vì bash
docker run alpine ls /              # Chạy alpine, list thư mục root
docker run -it ubuntu bash          # Interactive shell
```

### Basic Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-d, --detach` | Chạy container trong background | `docker run -d nginx` |
| `--name` | Đặt tên cho container | `docker run --name myapp nginx` |
| `--rm` | Tự động xóa container khi dừng | `docker run --rm alpine ls` |
| `-it` | Interactive + TTY (cho shell) | `docker run -it ubuntu bash` |
| `IMAGE` | Tên image (bắt buộc) | `nginx:alpine`, `ubuntu:latest` |
| `COMMAND` | Override entrypoint command | `docker run nginx ls /` |

### Networking Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-p, --publish` | Map port host:container | `docker run -p 8080:80 nginx` |
| `--network` | Chọn network | `docker run --network bridge nginx` |
| `--hostname` | Set hostname trong container | `docker run --hostname myhost alpine` |
| `--dns` | DNS server | `docker run --dns 8.8.8.8 alpine` |

### Storage Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-v, --volume` | Mount volume/directory | `docker run -v /host/path:/container/path` |
| `--mount` | Mount với cú pháp chi tiết | `docker run --mount type=bind,src=/data,dst=/app` |
| `--tmpfs` | Mount tmpfs (RAM) | `docker run --tmpfs /tmp` |

### Security Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `--user` | Chạy với user/UID | `docker run --user 1000 alpine` |
| `--cap-add` | Thêm Linux capability | `docker run --cap-add NET_ADMIN alpine` |
| `--cap-drop` | Loại bỏ capability | `docker run --cap-drop ALL alpine` |
| `--security-opt` | Tùy chọn bảo mật | `docker run --security-opt seccomp=unconfined` |
| `--privileged` | Privileged mode (toàn quyền host) | `docker run --privileged alpine` |

### Resource Limits
| Option | Mô tả | Example |
|--------|-------|---------|
| `--memory` | Giới hạn RAM | `docker run --memory 512m alpine` |
| `--cpus` | Giới hạn CPU cores | `docker run --cpus 1.5 alpine` |
| `--cpu-shares` | CPU weight (tương đối) | `docker run --cpu-shares 512 alpine` |

### Environment & Runtime
| Option | Mô tả | Example |
|--------|-------|---------|
| `-e, --env` | Set environment variable | `docker run -e NAME=value alpine` |
| `--env-file` | Load env từ file | `docker run --env-file .env alpine` |
| `--entrypoint` | Override entrypoint | `docker run --entrypoint sh alpine` |
| `--workdir` | Set working directory | `docker run --workdir /app alpine` |

### Logging
| Option | Mô tả | Example |
|--------|-------|---------|
| `--log-driver` | Log driver (json-file, syslog,...) | `docker run --log-driver json-file` |
| `--log-opt` | Log driver options | `docker run --log-opt max-size=10m` |

### Common Examples
```bash
# Chạy nginx với port mapping + detach
docker run -d -p 8080:80 --name webserver nginx

# Chạy container tương tác với shell
docker run -it ubuntu bash

# Mount local code vào container
docker run -v $(pwd):/app -w /app python:3.9 python script.py

# Resource limits
docker run -m 512m --cpus 1.0 nginx

# Network isolation
docker network create mynet
docker run --network mynet --name app1 alpine
docker run --network mynet --name app2 alpine
```
---

## docker exec

**Mục đích**: Chạy command trong container đang chạy. Không tạo container mới.

### Syntax cơ bản
```bash
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```
- **CONTAINER**: Container ID hoặc tên (bắt buộc)
- **COMMAND**: Command muốn chạy trong container
- **ARG**: Arguments cho command

**Ví dụ đơn giản**:
```bash
docker exec mycontainer ls /           # List files trong container
docker exec -it mycontainer bash       # Mở shell tương tác
docker exec mycontainer cat /etc/os-release  # Xem OS info
```

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-d, --detach` | Chạy command trong background | `docker exec -d mycontainer sh -c "while true; do echo hi; sleep 2; done"` |
| `-i, --interactive` | Giữ STDIN mở (cho input) | `docker exec -i mycontainer python script.py` |
| `-t, --tty` | Allocate pseudo-TTY (để có shell đẹp) | Kết hợp với `-i` làm `-it` |
| `-it` | Kết hợp cả `-i` và `-t` (phổ biến nhất) | `docker exec -it mycontainer bash` |
| `-e, --env` | Set environment variable | `docker exec -e NAME=value mycontainer env` |
| `--env-file` | Load env từ file | `docker exec --env-file .env mycontainer sh` |
| `-u, --user` | Chạy với user/UID cụ thể | `docker exec -u 1000 mycontainer id` |
| `-w, --workdir` | Set working directory | `docker exec -w /app mycontainer pwd` |
| `--privileged` | Give extended privileges | `docker exec --privileged mycontainer ip link` |

### Common Use Cases
```bash
# Vào container shell (phổ biến nhất)
docker exec -it <container_name> /bin/bash
# hoặc /bin/sh nếu container nhỏ (alpine)

# Chạy command một lần
docker exec mycontainer ps aux

# Xem logs của process (nếu không dùng docker logs)
docker exec mycontainer tail -f /var/log/app.log

# Kiểm tra network/disk
docker exec mycontainer netstat -tulpn
docker exec mycontainer df -h

# Copy file từ container (không dùng docker cp)
docker exec mycontainer cat /path/file > local_file

# Chạy script có input
docker exec -i mycontainer python /app/process.py < input.txt
```

### Notes
- Container phải đang **running** (không thể exec vào stopped/exited container)
- Không thể thay đổi container config (memory, CPU, ports...) - dùng `docker update` thay
- Nếu container dùng `USER` directive trong Dockerfile, exec sẽ chạy với user đó trừ khi dùng `-u`
- **Không dùng exec để start container** - dùng `docker start` thay

---

## docker ps

**Mục đích**: Liệt kê containers. Mặc định chỉ hiển thị running containers.

### Syntax cơ bản
```bash
docker ps [OPTIONS]
```

**Ví dụ đơn giản**:
```bash
docker ps                    # Xem containers đang chạy
docker ps -a                 # Xem TẤT CẢ containers (running + stopped)
docker ps -l                 # Xem container mới tạo nhất
docker ps -q                 # Chỉ hiển thị container IDs (dùng trong script)
```

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-a, --all` | Show tất cả containers (running + exited/stopped) | `docker ps -a` |
| `-f, --filter` | Lọc output theo điều kiện | `docker ps -f status=running` |
| `--format` | Format output với template | `docker ps --format "table {{.ID}}\t{{.Names}}"` |
| `-n, --last` | Hiển thị n containers mới tạo nhất | `docker ps -n 5` |
| `-l, --latest` | Hiển thị container mới tạo nhất | `docker ps -l` |
| `--no-trunc` | Không cắt ngắn output (hiển thị đầy đủ) | `docker ps --no-trunc` |
| `-q, --quiet` | Chỉ hiển thị container IDs | `docker ps -q` (dùng với xargs) |
| `-s, --size` | Hiển thị total file sizes | `docker ps -s` |

### Filtering (--filter)
Các filter phổ biến:
```bash
docker ps -f status=running       # Only running
docker ps -f status=exited        # Only exited
docker ps -f name=mycontainer     # Filter by name
docker ps -f id=abc123            # Filter by ID prefix
docker ps -f label=env=prod       # Filter by label
docker ps -f ancestor=nginx       # Filter by image
docker ps -f volume=/data         # Filter by volume
```

Status có thể: `created`, `restarting`, `running`, `removing`, `paused`, `exited`, `dead`

### Format Templates
```bash
# Custom table format
docker ps --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Status}}"

# JSON output (dùng với jq)
docker ps --format json | jq .

# Chỉ lấy specific fields
docker ps --format "{{.ID}} {{.Names}}"  # IDs and names only

# Built-in table (default)
docker ps --format table
```

### Common Use Cases
```bash
# Lấy container ID để dùng với các lệnh khác
CONTAINER_ID=$(docker ps -q -f name=myapp)

# Xem tất cả containers với full info
docker ps -a --no-trunc

# Tìm containers của specific image
docker ps -f ancestor=nginx

# Count running containers
docker ps -q | wc -l

# Xem containers tạo trong 24h qua
docker ps -a -f "until=24h"

# Export container list
docker ps -a --format "{{.ID}},{{.Image}},{{.Status}}" > containers.csv
```

### Notes
- Mặc định `docker ps` chỉ hiển thị **running** containers
- Container đã **exited** nhưng không bị rm vẫn hiển thị với `-a`
- Dùng `--no-trunc` để xem full command, ports, volumes (đã bị cắt)
- Filter `name=` match **substring**, không cần chính xác hoàn toàn

---

## docker build

**Mục đích**: Build image từ Dockerfile và context (files trong thư mục).

### Syntax cơ bản
```bash
docker build [OPTIONS] PATH | URL | -
```
- **PATH**: Thư mục chứa Dockerfile và files cần build (bắt buộc)
- **URL**: Git repository URL
- **-**: Đọc context từ STDIN

**Ví dụ đơn giản**:
```bash
docker build .                          # Build từ Dockerfile trong thư mục hiện tại
docker build -t myapp:latest .         # Build và tag image
docker build -f Dockerfile.prod .      # Dùng Dockerfile tên khác
docker build https://github.com/user/repo.git  # Build từ Git repo
```

### Build Context
- **Context**: Tất cả files trong PATH (hoặc URL) được gửi đến Docker daemon
- **.dockerignore**: File giống `.gitignore` - loại bỏ files không cần thiết
- Context được nén và gửi đến daemon, nên giữ nhỏ (không include node_modules, .git,...)

### Core Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-t, --tag` | Đặt tên và tag cho image | `docker build -t myapp:v1.0 .` |
| `-f, --file` | Chỉ định Dockerfile path | `docker build -f docker/Dockerfile .` |
| `--build-arg` | Set build-time variables | `docker build --build-arg NODE_ENV=production .` |
| `--target` | Build đến specific stage (multi-stage) | `docker build --target builder .` |
| `--no-cache` | Không dùng cache | `docker build --no-cache .` |
| `--pull` | Pull base image mới nhất trước khi build | `docker build --pull .` |
| `-q, --quiet` | Suppress output, chỉ print image ID | `docker build -q .` |
| `--platform` | Target platform (linux/amd64, linux/arm64) | `docker build --platform linux/arm64 .` |

### Output Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `--load` | Load image vào Docker daemon (default) | `docker build --load .` |
| `-o, --output` | Export output ra file/dir | `docker build -o type=local,dest=./out .` |
| `--push` | Push trực tiếp đến registry | `docker build --push -t user/app .` |

### Caching
| Option | Mô tả | Example |
|--------|-------|---------|
| `--cache-from` | Sử dụng cache từ external sources | `docker build --cache-from user/app:cache .` |
| `--cache-to` | Export cache | `docker build --cache-to type=local,dest=./cache .` |
| `--no-cache-filter` | Không cache specific stages | `docker build --no-cache-filter stage1 .` |

### Advanced
| Option | Mô tả | Example |
|--------|-------|---------|
| `--ssh` | Forward SSH agent vào build | `docker build --ssh default .` |
| `--secret` | Pass secrets vào build (không lưu trong image) | `docker build --secret id=mysecret,src=./secret.txt .` |
| `--label` | Set image labels (metadata) | `docker build --label maintainer=team@co.com .` |
| `--shm-size` | Set /dev/shm size cho RUN instructions | `docker build --shm-size=2g .` |

### Common Examples
```bash
# Build với tag
docker build -t myapp:latest .

# Build với multiple tags
docker build -t myapp:latest -t myapp:v1.0 .

# Build với build args
docker build --build-arg NODE_ENV=production --build-arg API_URL=https://api.example.com .

# Multi-stage: chỉ build final stage
docker build --target final .

# Build với specific Dockerfile
docker build -f Dockerfile.dev -t myapp:dev .

# Build và push ngay lập tức
docker build -t user/app:latest --push .

# Disable cache (clean build)
docker build --no-cache .

# Build với platform khác (cross-compile)
docker build --platform linux/arm64 -t myapp:arm64 .

# Build với SSH forwarding (dùng private repo trong Dockerfile)
docker build --ssh default .
```

### Build Process
1. **Context gửi đến daemon**: Tất cả files trong PATH được gửi
2. **Dockerfile đọc**: Các instructions được thực thi lần lượt
3. **Layer caching**: Mỗi instruction tạo layer, cache theo Dockerfile hash và file changes
4. **Final image**: Layers được combine thành image final

### Tips
- Mỗi `RUN`, `COPY`, `ADD` tạo **layer** mới →合理安排 thứ tự Dockerfile để tối ưu cache
- Dùng `.dockerignore` để giảm context size
- Build args không được lưu trong image layers (nhưng có trong history)
- Dùng `--progress=plain` để xem full output của RUN commands
- `docker buildx` hỗ trợ advanced features: multi-platform, cache export, BuildKit features

### Troubleshooting
```bash
# Xem chi tiết build steps
docker history myimage

# Xem full build logs
docker build --progress=plain .

# Debug cache misses
docker build --no-cache .

# Build với maximum verbosity
docker build --debug .
```

### Notes
- **docker build** thực chất là wrapper của **docker buildx build**
- BuildKit mặc định được bật trong Docker Desktop (nhưng có thể tắt)
- Image IDs là hash của layers, không phải tag
- `docker build` không tự động push - dùng `--push` hoặc `docker push` sau


---

## docker images

**Mục đích**: Liệt kê local images.

### Syntax cơ bản
```bash
docker images [OPTIONS] [REPOSITORY[:TAG]]
```
- **REPOSITORY[:TAG]**: Filter theo repository và/hoặc tag (optional)

**Ví dụ đơn giản**:
```bash
docker images                    # List tất cả images
docker images nginx              # Images có tên chứa "nginx"
docker images nginx:alpine       # Images cụ thể với tag
docker images -q                 # Chỉ IDs (dùng trong script)
```

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-a, --all` | Show tất cả images (bao gồm intermediate và dangling) | `docker images -a` |
| `--digests` | Hiển thị digests | `docker images --digests` |
| `-f, --filter` | Lọc output | `docker images -f dangling=true` |
| `--format` | Custom output format | `docker images --format "table {{.Repository}}\t{{.Tag}}"` |
| `--no-trunc` | Không cắt ngắn output | `docker images --no-trunc` |
| `-q, --quiet` | Chỉ hiển thị image IDs | `docker images -q` |
| `--tree` | List multi-platform images dạng tree (EXPERIMENTAL) | `docker images --tree` |

### Filtering (-f)
```bash
docker images -f dangling=true           # Chỉ dangling images (không có tag)
docker images -f reference='nginx:*'     # Images bắt đầu với nginx và có tag
docker images -f before=nginx:latest     # Images được tạo TRƯỚC nginx:latest
docker images -f since=ubuntu:20.04      # Images được tạo SAU ubuntu:20.04
docker images -f label=maintainer=team   # Images có label cụ thể
```

### Format Templates
```bash
# Custom columns
docker images --format "{{.ID}} {{.Repository}}:{{.Tag}}"

# JSON output
docker images --format json | jq .

# Table với custom headers
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

### Common Use Cases
```bash
# Xóa tất cả dangling images
docker images -f dangling=true -q | xargs docker rmi

# Tìm images lớn nhất
docker images --format "table {{.Repository}}\t{{.Size}}" | sort -k2 -h

# List images theo tên
docker images | grep nginx

# Lấy ID của specific image
IMAGE_ID=$(docker images -q nginx:alpine)

# Count local images
docker images -q | wc -l
```

### Image States
- **Dangling**: Images không có tag (thường là intermediate layers) - có thể xóa an toàn
- **Intermediate**: Layers được tạo trong multi-stage builds
- **Tagged**: Images có repository:tag

### Notes
- Repository = tên image (ví dụ: `nginx`, `ubuntu`, `myapp`)
- Tag = version/label (ví dụ: `latest`, `alpine`, `v1.0`)
- `docker images` mặc định **không** hiển thị dangling images
- Dùng `docker image prune` để xóa dangling images
- Size hiển thị là compressed size (không phải uncompressed)
- Digest là immutable identifier (sha256 hash) - khác với mutable tags

### Troubleshooting
```bash
# Xem chi tiết image (layers, config)
docker inspect nginx:alpine

# Xem history của image (các layers)
docker history nginx:alpine

# Prune unused images
docker image prune -a
```


---

## docker pull

**Mục đích**: Tải image từ registry (Docker Hub mặc định) về local.

### Syntax cơ bản
```bash
docker pull [OPTIONS] NAME[:TAG|@DIGEST]
```
- **NAME**: Repository name (ví dụ: `nginx`, `ubuntu`, `myuser/myapp`)
- **TAG**: Tag version (default: `latest`)
- **DIGEST**: Immutable content hash (sha256:...)

**Ví dụ đơn giản**:
```bash
docker pull nginx                    # Tải nginx:latest
docker pull nginx:alpine             # Tải specific tag
docker pull ubuntu:20.04            # Tải Ubuntu 20.04
docker pull myuser/app:v1.0         # Tải từ private registry
docker pull nginx@sha256:abc123...  # Tải bằng digest (immutable)
```

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-a, --all-tags` | Tải TẤT CẢ tags của repository | `docker pull -a ubuntu` |
| `--platform` | Tải image cho platform cụ thể | `docker pull --platform linux/arm64 nginx` |
| `-q, --quiet` | Suppress verbose output | `docker pull -q nginx` |

### Registry & Authentication
- **Default registry**: `docker.io` (Docker Hub)
- **Private registry**: `docker pull myregistry.com:5000/myapp:tag`
- **Authentication**: Dùng `docker login` trước khi pull từ private registry
- **Digest vs Tag**: Digest là immutable hash, tag có thể thay đổi

### Common Examples
```bash
# Pull latest
docker pull nginx

# Pull specific version
docker pull nginx:1.23
docker pull python:3.9-slim

# Pull all tags (cảnh báo: có thể rất nhiều!)
docker pull -a ubuntu

# Pull với authentication (đã login)
docker pull myuser/myapp:prod

# Pull từ custom registry
docker pull registry.example.com:5000/app:v2.0

# Pull multi-arch image (chọn platform)
docker pull --platform linux/arm64 debian:bullseye

# Pull và quiet
docker pull -q nginx:alpine > /dev/null
```

### Pull Process
1. **Resolve name**: Xác định registry, repository, tag
2. **Auth**: Kiểm tra credentials (nếu cần)
3. **Fetch manifest**: Lấy metadata về image và layers
4. **Download layers**: Tải từng layer (có thể reuse local layers)
5. **Store**: Lưu vào local image store

### Notes
- Pull **lưu vào local image store**, không tự động run
- Layers được cache - pull lần sau chỉ tải layers mới/changed
- `latest` tag thường là mới nhất nhưng **không đảm bảo** stable
- Digest (`@sha256:...`) là cách pull chính xác version
- Dùng `docker images` để xem images đã pull
- Pull failure: check network, auth, existence (`docker search`)
- Pull từ insecure registry: cần config `/etc/docker/daemon.json` với `"insecure-registries": ["myregistry:5000"]`

### Troubleshooting
```bash
# Pull với verbose để xem chi tiết
docker pull --debug nginx

# Kiểm tra login status
docker info | grep Username

# Logout nếu auth lỗi
docker logout

# Force re-pull (bỏ qua cache)
docker pull --disable-content-trust nginx
```

### Related Commands
- `docker push`: Upload image lên registry
- `docker login/logout`: Authenticate
- `docker search`: Tìm images trên Docker Hub
- `docker tag`: Đặt tag cho local image trước khi push


---

## docker push

**Mục đích**: Upload image từ local lên registry.

### Syntax cơ bản
```bash
docker push [OPTIONS] NAME[:TAG]
```
- **NAME[:TAG]**: Image name và tag (phải có registry prefix nếu không phải Docker Hub)

**Ví dụ đơn giản**:
```bash
docker push myuser/myapp            # Push myuser/myapp:latest
docker push myuser/myapp:v1.0       # Push specific tag
docker push nginx:alpine            # Push đến Docker Hub (cần login)
```

### Requirements
- **Đã login** vào registry (dùng `docker login`)
- **Image có tên đúng** (phải có registry/username prefix)
- **Tag đã tồn tại** trong local (dùng `docker images` để check)
- **Quyền write** trên repository (nếu là private)

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-a, --all-tags` | Push tất cả tags của image | `docker push -a myuser/myapp` |
| `--platform` | Push platform-specific manifest | `docker push --platform linux/arm64 myapp` |
| `-q, --quiet` | Suppress verbose output | `docker push -q myapp` |

### Push Workflow
```bash
# 1. Build image với đúng tên
docker build -t myuser/myapp:v1.0 .

# 2. Login vào registry (Docker Hub hoặc private)
docker login docker.io  # Docker Hub
docker login myregistry.com:5000  # Private registry

# 3. Push
docker push myuser/myapp:v1.0

# 4. Verify (trên website/registry)
# Xem image tại: https://hub.docker.com/r/myuser/myapp
```

### Common Examples
```bash
# Push đến Docker Hub
docker tag myapp:local myusername/myapp:latest
docker push myusername/myapp:latest

# Push tất cả tags
docker tag myapp:latest myuser/app:v1.0
docker tag myapp:latest myuser/app:v1.0.1
docker push -a myuser/app

# Push với multiple tags cùng lúc
docker build -t myapp:latest -t myuser/app:prod .
docker push myuser/app:latest
docker push myuser/app:prod

# Push đến private registry
docker tag myapp myregistry:5000/myapp:v2.0
docker push myregistry:5000/myapp:v2.0

# Push multi-arch image (buildx)
docker buildx build --platform linux/amd64,linux/arm64 --push -t myuser/app:multi .
```

### Tags & Repositories
- **Docker Hub**: `username/repo:tag`
- **Official images**: `nginx:alpine` (không cần username)
- **Private registry**: `registry:port/username/repo:tag`
- **Tag không được push**: Nếu image chỉ có `latest` mà bạn push `myapp:v1.0`, nó sẽ error

### Notes
- Push **chỉ upload layers mới/changed** (có cache)
- Image **phải tồn tại local** trước khi push
- Không thể push **dangling images** (images không có tag) - cần tag trước
- Multi-stage build: chỉ layer cuối (target) được push, các layer trung gian không
- Push digest (`@sha256:...`) không được hỗ trợ - push theo tag

### Troubleshooting
```bash
# Error: denied (auth lỗi)
docker logout && docker login

# Error: repository does not exist
docker tag local:tag username/repo:tag  # Tag đúng tên

# Error: unauthorized (không có quyền)
# Kiểm tra: docker info | grep Username
# Đăng nhập lại với user có quyền push

# Push but không thấy trên Docker Hub?
# → Check: đang push đúng registry chưa?
# → Check: tag có đúng không?
```

### Security Considerations
- **Never push sensitive data**: Image layers lưu permanently - dùng `.dockerignore` và multi-stage
- **Use secrets carefully**: `--secret` không được push lên registry (chỉ trong build)
- **Scan images**: `docker scan myapp:latest` trước khi push
- **Private registries**: Dùng TLS, authentication, và audit logs

### Related Commands
- `docker login/logout`: Authenticate
- `docker tag`: Đặt tag cho image trước khi push
- `docker pull`: Tải image từ registry
- `docker buildx build --push`: Build và push trong 1 lệnh


---

## docker login

**Mục đích**: Xác thực (authenticate) đến registry (Docker Hub hoặc private).

### Syntax cơ bản
```bash
docker login [OPTIONS] [SERVER]
```
- **SERVER**: Registry URL (default: `docker.io` - Docker Hub)

**Ví dụ đơn giản**:
```bash
docker login                    # Login Docker Hub (prompt username/password)
docker login myregistry.com     # Login private registry
echo "mypassword" | docker login -u myuser --password-stdin  # Non-interactive
```

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-u, --username` | Username (hoặc email cho Docker Hub cũ) | `docker login -u myuser` |
| `-p, --password` | Password hoặc PAT (Personal Access Token) | `docker login -u myuser -p mytoken` |
| `--password-stdin` | Đọc password từ STDIN (an toàn hơn) | `echo $TOKEN | docker login -u myuser --password-stdin` |

### Authentication Methods
1. **Interactive** (prompt):
```bash
docker login
Username: myuser
Password: ********
Login Succeeded
```

2. **Non-interactive** (script):
```bash
# Dùng PAT (Personal Access Token) thay password
docker login -u myuser -p ghp_xxxxx

# Hoặc password-stdin (recommended)
echo "$DOCKER_TOKEN" | docker login -u myuser --password-stdin
```

3. **Config file** (manual edit):
- File: `~/.docker/config.json`
- Thêm credentials:
```json
{
  "auths": {
    "https://index.docker.io/v1/": {
      "auth": "base64(username:password)"
    }
  }
}
```

### Docker Hub Specifics
- **Username**: Docker Hub username
- **Password**: Docker Hub password HOẶC **PAT** (Personal Access Token)
- **PAT**: Tạo tại https://hub.docker.com/settings/security
- Vì Docker Hub đã tắt password authentication từ 2023, **phải dùng PAT**

### Private Registries
```bash
# Self-hosted registry
docker login registry.example.com:5000
docker push registry.example.com:5000/myapp:tag

# AWS ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com

# Google GCR
gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://gcr.io

# Azure ACR
az acr login --name myregistry
```

### Security Best Practices
- **KHÔNG hardcode password** trong scripts/dockerfiles
- Dùng **--password-stdin** hoặc environment variables:
```bash
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USER" --password-stdin
```
- Dùng **PAT** thay password (có thể revoke riêng từng token)
- Store credentials trong **secret manager** (AWS Secrets Manager, HashiCorp Vault,...)
- Logout khi dùng shared machines: `docker logout`

### Common Issues
```bash
# Error: credentials mismatch
# → Username/password sai, hoặc dùng email thay username

# Error: unauthorized: authentication required
# → Chưa login, hoặc login đến wrong registry

# Error: invalid username/password
# → Docker Hub: dùng PAT thay password

# Login thành công nhưng push lỗi?
# → Kiểm tra repository tồn tại và user có quyền push

# Login persists sau reboot?
# → Credentials lưu trong ~/.docker/config.json, có thể xóa file để logout
```

### Check Login Status
```bash
# Xem accounts đã login
docker info | grep Username

# Hoặc đọc config file
cat ~/.docker/config.json | jq '.auths'

# Test push/pull (thử pull 1 image nhỏ)
docker pull hello-world
```

### Logout
```bash
docker logout                    # Logout Docker Hub
docker logout myregistry.com     # Logout specific registry

# Xóa tất cả credentials
rm ~/.docker/config.json
```

### Notes
- Credentials được lưu trong `~/.docker/config.json` (hoặc `%USERPROFILE%\.docker\config.json` trên Windows)
- Docker Desktop có UI cho login/logout
- `docker login` không cần thiết cho **public images** (pull/push đến Docker Hub public repos)
- Private registry: cần login trước khi pull/push
- Token có thể có **expiry** - cần renew


---

## docker logout

**Mục đích**: Đăng xuất (logout) khỏi registry.

### Syntax cơ bản
```bash
docker logout [SERVER]
```
- **SERVER**: Registry URL (default: Docker Hub `docker.io`)

**Ví dụ đơn giản**:
```bash
docker logout                    # Logout Docker Hub
docker logout myregistry.com     # Logout private registry
docker logout localhost:5000     # Logout local registry
```

### Usage
| Command | Mô tả |
|---------|-------|
| `docker logout` | Logout khỏi Docker Hub (default) |
| `docker logout myregistry.com` | Logout khỏi specific registry |
| `docker logout --help` | Help |

### What Happens on Logout?
- Xóa **credentials** của registry cụ thể khỏi `~/.docker/config.json`
- Credentials (auth token) được xóa, không còn access
- **Không** xóa images đã pull - images vẫn giữ nguyên local
- Các lần pull/push tiếp theo sẽ yêu cầu login lại

### Common Use Cases
```bash
# Logout Docker Hub
docker logout

# Logout nhiều registries
docker logout
docker logout myregistry.com
docker logout gcr.io

# Trên CI/CD: cleanup credentials sau build
docker logout

# Switch user/account
docker logout
docker login -u otheruser

# Revoke token nếu nghi ngờ compromised
docker logout
# → Token cũ bị vô hiệu hóa (nếu server hỗ trợ revocation)
```

### Security Considerations
- **Shared machines**: Luôn logout sau khi dùng xong
- **CI/CD pipelines**: Nên logout sau khi push/pull để cleanup credentials
- **Rotate credentials**: Nếu suspected leak, logout cũ → login với token mới
- Credentials trong `config.json` base64 encoded nhưng **KHÔNG encrypted** - xóa file để chắc chắn

### Check Current Logins
```bash
# Xem registries đã login
cat ~/.docker/config.json | jq '.auths'

# Hoặc simple grep
grep -A2 'auths' ~/.docker/config.json

# Test (thử pull private image - sẽ fail nếu chưa login)
docker pull private-registry/myapp:tag
```

### Troubleshooting
```bash
# Logout không hoạt động?
# → Check config file location: docker info | grep "Docker Root Dir"
# → Manual delete: rm ~/.docker/config.json

# Multiple accounts: Docker Hub
# → Docker Hub chỉ cho phép 1 account/login tại một time
# → Phải logout trước khi login account khác

# Logout nhưng vẫn không push được?
# → Có thể đang dùng credential helper (store trong keychain/credential manager)
# → Check: cat ~/.docker/config.json | grep credStore
# → Xóa credentials từ credential helper (keychain, Windows Credential Manager,...)
```

### Notes
- **docker logout** chỉ xóa auth credentials, không xóa images, containers, volumes
- Không cần logout cho **public images** (không cần auth)
- Private registry tự quản lý session/token expiry
- Config file path:
  - Linux/Mac: `~/.docker/config.json`
  - Windows: `%USERPROFILE%\.docker\config.json`
- Credential helpers: có thể store credentials trong OS keychain thay vì plain file

### Related Commands
- `docker login`: Authenticate
- `docker info`: Xem thông tin Docker (bao gồm login status)
- `docker pull/push`: Sẽ yêu cầu login nếu chưa auth


---

## docker search

**Mục đích**: Tìm images trên Docker Hub.

### Syntax cơ bản
```bash
docker search [OPTIONS] TERM
```
- **TERM**: Từ khóa tìm kiếm (repository name, description,...)

**Ví dụ đơn giản**:
```bash
docker search nginx               # Tìm images có "nginx"
docker search python              # Tìm Python images
docker search "nodejs"            # Tìm Node.js
docker search nginx --limit 5     # Giới hạn 5 kết quả
```

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-f, --filter` | Lọc kết quả theo tiêu chí | `docker search -f is-automated=true nginx` |
| `--format` | Format output tùy chỉnh | `docker search --format "{{.Name}}\t{{.StarCount}}" nginx` |
| `--limit` | Giới hạn số kết quả | `docker search --limit 10 python` |
| `--no-trunc` | Không cắt ngắn output | `docker search --no-trunc nginx` |

### Filter Options (`-f`)
```bash
docker search -f is-automated=true TERM    # Chỉ automated builds
docker search -f is-official=true TERM     # Chỉ official images
docker search -f stars=1000 TERM           # Stars >= 1000
docker search -f name=nginx TERM           # Tên chính xác match
docker search -f description=python TERM   # Match trong description
```

**Available filters**: `is-automated`, `is-official`, `stars`, `name`, `description`

### Output Columns
Default output hiển thị:
- **NAME**: Image name (username/repo)
- **DESCRIPTION**: Mô tả ngắn
- **STARS**: Số lượt star (độ phổ biến)
- **OFFICIAL**: `[OK]` nếu là official image
- **AUTOMATED**: `[OK]` nếu là automated build

### Format Templates
```bash
# Simple list of names
docker search nginx --format "{{.Name}}"

# Name + stars
docker search python --format "table {{.Name}}\t{{.StarCount}}"

# JSON output
docker search nodejs --format json | jq .

# Custom columns
docker search redis --format "{{.Name}} ({{.StarCount}}⭐): {{.Description}}"
```

### Common Use Cases
```bash
# Tìm official image
docker search -f is-official=true python

# Tìm images phổ biến (stars > 1000)
docker search -f stars=1000 nginx

# Tìm automated builds (trusted builds)
docker search -f is-automated=true node

# Lấy top 5 images cho 1 keyword
docker search --limit 5 postgres

# Lọc và sort by stars
docker search nginx --format "{{.Name}}\t{{.StarCount}}" | sort -k2 -rn | head -10

# Kiểm tra tồn tại của image
docker search myimage > /dev/null && echo "Found" || echo "Not found"
```

### Official Images
- **Official images**: Maintained bởi Docker (như `nginx`, `python`, `ubuntu`, `node`,...)
- Đánh dấu `[OK]` trong cột OFFICIAL
- Recommended cho production vì được bảo trì, scan security
- Danh sách: https://hub.docker.com/search?q=&type=image&image_filter=official

### Automated Builds
- **Automated builds**: Build tự động khi push code vào GitHub/Bitbucket
- Đánh dấu `[OK]` trong cột AUTOMATED
- Thường có `[ck]` prefix trong image name (ví dụ: `[ck] library/nginx`)
- Tin cậy hơn manual builds

### Understanding Stars
- **Stars** là proxy cho popularity/trust
- Không phải chất lượng - có thể fake stars
- Combine với `is-official` và `is-automated` để đánh giá
- Kiểm tra `Description` và `Dockerfile` trên GitHub link

### Practical Search Strategy
```bash
# 1. Tìm official image trước
docker search -f is-official=true TERM

# 2. Nếu không có official, tìm automated
docker search -f is-automated=true TERM

# 3. Kiểm tra stars (> 100 là tốt)
docker search -f stars=100 TERM

# 4. Kiểm tra update frequency (xem description, Dockerfile)
# → Click link trên Docker Hub

# 5. Pull và test trước khi dùng production
docker pull image:tag
docker run --rm image:tag <test command>
```

### Limitations
- **Chỉ search Docker Hub** (không search private registries)
- **Chỉ tìm theo NAME/DESCRIPTION** (không search labels, stars filter nâng cao)
- **Rate limited**: Docker Hub có rate limit cho anonymous (30 requests/6h)
- **Không search tags cụ thể** - chỉ search repository names
- **Không verify image content** - search chỉ cho metadata

### Notes
- Docker Hub là default registry, nhưng `docker search` **chỉ tìm trên Docker Hub**, không tìm trên private registries
- Search **không yêu cầu login** (anonymous)
- Kết quả sắp xếp theo ** relevance** (không phải stars hay updated)
- Dùng web UI cho search nâng cao: https://hub.docker.com/
- `docker search` đang bị deprecated? Docker khuyến cáo dùng web UI

### Troubleshooting
```bash
# Error: rate limit exceeded
# → Login: docker login
# → Hoặc đợi 6h, hoặc dùng proxy

# No results found?
# → Thử keyword đơn giản hơn (không dặc hiệu quá)
# → Check spelling

# Output too long?
# → Dùng --format để filter columns
# → Dùng --limit để giới hạn
```


---

## docker version

**Mục đích**: Hiển thị thông tin version của Docker client và daemon.

### Syntax cơ bản
```bash
docker version [OPTIONS]
```

**Ví dụ đơn giản**:
```bash
docker version                    # Xem version đầy đủ
docker version --format '{{.Server.Version}}'  # Chỉ version của daemon
docker version -f '{{.Client.Version}}'       # Chỉ version của client
```

### Output Structure
Default output gồm 2 phần:
```
Client:  Docker Engine - Community
 Version:           24.0.5
 API version:       1.43
...
 
Server: Docker Engine - Community
 Engine:
  Version:          24.0.5
  API version:      1.43 (minimum version 1.12)
...
```

- **Client**: Docker CLI version
- **Server**: Docker daemon (Engine) version
- API version: Compatibility version giữa client và daemon

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-f, --format` | Format output với template | `docker version -f '{{.Server.Version}}'` |

### Common Use Cases
```bash
# Chỉ xem Docker Engine version
docker version --format '{{.Server.Version}}'

# Xem cả client và server version (compact)
docker version --format 'Client: {{.Client.Version}}\nServer: {{.Server.Version}}'

# Xem API version
docker version -f '{{.Client.APIVersion}}'

# Xem tất cả info dạng JSON (cho parsing)
docker version --format json | jq

# Check Docker Desktop vs Docker Engine
docker version | grep -i desktop
```

### Version Compatibility
- **Client và Server API version** cần tương thích
- Client có thể mới hơn Server (nhưng không quá nhiều)
- Nếu lỗi version mismatch, upgrade/downgrade client hoặc server
- Kiểm tra compatibility matrix: https://docs.docker.com/engine/release-notes/

### Format Templates
```bash
# Client version only
docker version -f '{{.Client.Version}}'

# Server version only  
docker version -f '{{.Server.Version}}'

# Both versions
docker version -f 'Client: {{.Client.Version}}\nServer: {{.Server.Version}}'

# Full JSON
docker version -f '{{json .}}' | jq

# Custom fields
docker version -f 'Go version: {{.Server.GoVersion}}\nOS/Arch: {{.Server.Platform.Name}}/{{.Server.Platform.Architecture}}'
```

### What Each Field Means
| Field | Mô tả |
|-------|-------|
| `Client.Version` | Docker CLI version |
| `Client.APIVersion` | Docker API version của client |
| `Server.Version` | Docker daemon version |
| `Server.APIVersion` | Docker API version của daemon |
| `Server.GoVersion` | Go compiler version (daemon) |
| `Server.Platform.Name` | OS (docker desktop, linux, windows,...) |
| `Server.Platform.Architecture` | CPU arch (amd64, arm64,...) |
| `Server.Platform.OS` | Operating system |
| `Server.Platform.Variant` | CPU variant (nếu có) |

### Troubleshooting
```bash
# Lỗi: "client is newer than server"
# → Client version quá mới so với daemon
# → Giải pháp: downgrade Docker CLI, hoặc upgrade daemon

# Check Docker Desktop version (GUI)
docker version | grep -i desktop

# Check if Docker is running
docker version 2>&1 | grep -q "Server:" && echo "Docker daemon running" || echo "Docker daemon NOT running"

# Get detailed info (including version)
docker info
```

### Notes
- `docker version` **không yêu cầu** daemon đang chạy (client-only info)
- `docker info` **yêu cầu** daemon chạy (kết nối đến daemon)
- Docker Desktop: Client và Server version thường cùng nhau
- Docker Engine (Linux): Có thể client và server khác version
- API version được chăng theo major.minor (ví dụ: 1.43)

### Related Commands
- `docker info`: Chi tiết về daemon (cũng show version)
- `docker system info`: System-wide info
- `docker compose version`: Docker Compose version (riêng biệt)


---

## docker info

**Mục đích**: Hiển thị thông tin system-wide về Docker daemon.

### Syntax cơ bản
```bash
docker info [OPTIONS]
```

**Ví dụ đơn giản**:
```bash
docker info                    # Xem tất cả thông tin
docker info --format '{{.OSType}}'  # Chỉ OS type
docker info | grep -i storage  # Filter thông tin
```

### Output Structure
Output chia thành nhiều sections:
- **Client**: Docker CLI info
- **Server**: Docker daemon info (nếu running)
- **System**: Containers, images, volumes, networks counts
- **Storage Driver**: Cách Docker lưu trữ data
- **Docker Root Dir**: Thư mục Docker data
- **Plugins**: Network, volume, authorization plugins
- **Default Runtime**: Runtime mặc định (runc,...)
- **Security Options**: AppArmor, SELinux, seccomp
- **Logging Driver**: Default logging driver
- **Cgroup Driver**: cgroup v1 hay v2
- **OSType**: OS architecture (linux, windows)
- **Index Server**: Registry index (Docker Hub)

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-f, --format` | Format output với template | `docker info -f '{{.ServerVersion}}'` |

### Common Use Cases
```bash
# Xem Docker daemon có chạy không (kết nối được không)
docker info > /dev/null 2>&1 && echo "Docker running" || echo "Docker not running"

# Kiểm tra storage driver
docker info | grep "Storage Driver"

# Kiểm tra Docker root directory
docker info | grep "Docker Root Dir"

# Xem số containers/images đang có
docker info | grep -E "Containers|Images|Volumes|Networks"

# Xem cgroup driver (quan trọng cho Kubernetes)
docker info | grep "Cgroup Driver"

# Get specific field (scripting)
docker info -f '{{.ServerVersion}}'
docker info -f '{{.OSType}}'
docker info -f '{{.ID}}'  # Docker daemon ID

# Đếm số lượng
docker info --format '{{json .}}' | jq '.Containers, .Images, .Volumes, .Networks'
```

### Format Templates
```bash
# JSON output (để parse)
docker info --format json | jq '.'

# Specific fields
docker info -f 'Docker Root Dir: {{.DockerRootDir}}'
docker info -f 'Default Runtime: {{.DefaultRuntime}}'

# Go template với condition
docker info -f '{{if .Swarm.LocalNodeState}}{{.Swarm.LocalNodeState}}{{end}}'
```

### Key Information Explained
| Section | Mô tả |
|---------|-------|
| **Storage Driver** | Cách Docker lưu layers (overlay2, aufs, devicemapper, zfs,...). overlay2 là phổ biến nhất trên Linux |
| **Docker Root Dir** | Thư mục chứa Docker data (default: `/var/lib/docker`) |
| **Default Runtime** | Runtime để chạy containers (runc, containerd, cri-o) |
| **Cgroup Driver** | Cgroup driver cho containers (cgroupfs hoặc systemd) |
| **OSType** | OS architecture (linux, windows) - quan trọng cho multi-platform |
| **Index Server** | Docker Hub URL (có thể change nếu dùng private registry mirror) |
| **Plugins** | Các plugin đã install (network, volume, authorization) |
| **Security Options** | Security features (AppArmor, SELinux, seccomp, no-new-privileges) |
| **Logging Driver** | Default logging driver (json-file, syslog, journald, fluentd,...) |
| **Runtimes** | Available runtimes list |

### Troubleshooting với docker info
```bash
# Docker không chạy?
docker info 2>&1 | grep -q "Is the docker daemon running" && echo "Daemon not running"

# Storage driver issue?
docker info | grep "Storage Driver"
# → Nếu là devicemapper, có thể performance issue (nên dùng overlay2)

# Cgroup driver mismatch (Kubernetes issue)?
docker info | grep "Cgroup Driver"
# → K8s yêu cầu systemd, Docker mặc định là cgroupfs

# Không đủ disk space?
docker info | grep "Docker Root Dir"
df -h $(docker info -f '{{.DockerRootDir}}')

# Quota issue?
docker info | grep "Space Reservation"
```

### Notes
- `docker info` yêu cầu **Docker daemon đang chạy** (khác `docker version`)
- Output rất dài, dùng `--format` hoặc `grep` để filter
- Docker Desktop: info khác Linux Docker Engine (có thêm WSL2, Hyper-V info)
- Swarm info: nếu node là Swarm cluster member, có thêm Swarm sections
- Some fields deprecated/removed trong versions mới

### Related Commands
- `docker version`: Chỉ version info (không yêu cầu daemon chạy)
- `docker system df`: Disk usage summary
- `docker stats`: Resource usage real-time
- `docker info --format json | jq`: Parse info trong scripts


---

## docker compose

**Mục đích**: Define và run multi-container applications với Docker Compose file.

### Syntax cơ bản
```bash
docker compose [OPTIONS] COMMAND [ARGS...]
```
- **COMMAND**: Subcommand (up, down, ps, logs, build,...)
- Compose file mặc định: `docker-compose.yml` hoặc `compose.yaml`

**Ví dụ đơn giản**:
```bash
docker compose up -d           # Start all services (detached)
docker compose down           # Stop và remove
docker compose ps             # List services/containers
docker compose logs -f        # Follow logs tất cả services
```

### Global Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-f, --file` | Chỉ định Compose file(s) | `docker compose -f docker-compose.yml up` |
| `-p, --project-name` | Project name (default: directory name) | `docker compose -p myapp up` |
| `--profile` | Enable specific profiles | `docker compose --profile debug up` |
| `--env-file` | Specify env file (default: .env) | `docker compose --env-file .env.dev up` |
| `--compatibility` | Compatibility mode (legacy) | `docker compose --compatibility up` |

### Core Commands

| Command | Mô tả | Example |
|---------|-------|---------|
| **up** | Create và start services | `docker compose up -d` |
| **down** | Stop và remove containers/networks | `docker compose down` |
| **ps** | List containers của project | `docker compose ps` |
| **logs** | Xem logs của services | `docker compose logs -f web` |
| **build** | Build hoặc rebuild services | `docker compose build` |
| **exec** | Execute command trong service | `docker compose exec web bash` |
| **run** | Run one-off command | `docker compose run --rm web python manage.py migrate` |
| **pull** | Pull service images | `docker compose pull` |
| **push** | Push service images | `docker compose push` |
| **stop** | Stop services (không remove) | `docker compose stop` |
| **start** | Start stopped services | `docker compose start` |
| **restart** | Restart services | `docker compose restart` |
| **rm** | Remove stopped containers | `docker compose rm` |

### docker compose up (Quan trọng nhất)
```bash
# Start trong foreground (logs hiển thị)
docker compose up

# Start detached (background)
docker compose up -d

# Build trước khi start
docker compose up --build

# Chỉ start specific services
docker compose up web db

# Start với scale (multiple instances)
docker compose up --scale web=3 --scale worker=2

# Remove containers cũ trước khi start
docker compose up --force-recreate

# Start với specific profile
docker compose --profile debug up

# Recreate nếu config thay đổi
docker compose up --renew-anon-volumes
```

**`up` flags**:
| Flag | Mô tả |
|------|-------|
| `-d, --detach` | Run in background |
| `--build` | Build images trước khi start |
| `--no-deps` | Không start services phụ thuộc |
| `--force-recreate` | Recreate containers ngay cả khi config không đổi |
| `--no-recreate` | Không recreate nếu container đã tồn tại |
| `--no-start` | Create containers nhưng không start |
| `--remove-orphans` | Xóa containers không còn trong compose file |
| `--scale SERVICE=NUM` | Scale specific service |

### docker compose down
```bash
# Stop và remove containers, networks
docker compose down

# Remove cả volumes (cẩn thận - data mất!)
docker compose down -v

# Remove images (cautious!)
docker compose down --rmi all      # Remove all images
docker compose down --rmi local    # Remove only local (unpushed) images

# Keep networks (chỉ stop containers)
docker compose down --remove-orphans
```

### docker compose exec (như docker exec)
```bash
# Exec vào service
docker compose exec web bash

# Exec với user
docker compose exec -u www-data web ls /var/www

# Exec với TTY (interactive)
docker compose exec -it db psql -U postgres

# Exec với env
docker compose exec -e DEBUG=1 web python app.py
```

### docker compose run (one-off)
```bash
# Run command một lần (tạo container tạm)
docker compose run --rm web python manage.py test

# Run với different image (override)
docker compose run --no-deps --entrypoint sh web

# Run với env từ file
docker compose run --env-file .env.test web pytest

# Override service config
docker compose run -e NODE_ENV=test web npm test
```

### docker compose logs
```bash
# Follow logs tất cả services
docker compose logs -f

# Follow logs của 1 service
docker compose logs -f web

# Show logs với timestamps
docker compose logs -f -t

# Show last N lines
docker compose logs --tail=100 web

# Since timeframe (e.g., 5m ago)
docker compose logs --since 5m

# Show logs của tất cả services (dùng với -f)
docker compose logs -f --tail=0
```

### Service Configuration (compose.yml)
```yaml
version: '3.8'
services:
  web:
    image: nginx:alpine
    build: ./web
    ports:
      - "8080:80"
    volumes:
      - ./code:/app
    environment:
      - ENV=prod
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network

volumes:
  db-data:

networks:
  app-network:
```

### Common Workflows
```bash
# Development cycle
docker compose up -d          # Start
docker compose logs -f web    # Xem logs
docker compose exec web bash  # Vào container
docker compose down           # Stop

# CI/CD pipeline
docker compose build --pull   # Build với base images mới nhất
docker compose push           # Push images
docker compose down -v        # Cleanup

# Debug
docker compose config         # Validate compose file
docker compose up --debug     # Start với debug logs
docker compose logs --tail=100  # Xem logs gần đây
```

### Notes
- `docker compose` là **plugin** chính thức, thay thế `docker-compose` (Python)
- Compose file versions: 1, 2, 3, 3.8 (compatibility theo Docker Engine version)
- Project name: mặc định là thư mục hiện tại, dùng `-p` để override
- `.env` file: Tự động load nếu có (key=value pairs)
- Network: Mặc định tạo bridge network `<project>_default`
- Volumes: Named volumes được define trong `volumes:` section
- Depends_on: Không đợi service "ready" - chỉ đợi container start
- Health checks: Dùng `healthcheck` trong service config
- Restart policies: `restart: unless-stopped` (production)

### Troubleshooting
```bash
# Validate compose file
docker compose config

# View resolved config (with defaults)
docker compose config --resolve-image-digests

# Check compose version
docker compose version

# View all resources (containers, networks, volumes)
docker compose ls
docker compose ps -a

# Cleanup (remove all stopped)
docker compose down --remove-orphans
docker volume prune -f
docker network prune -f
```

### Differences: docker compose vs docker-compose
| Feature | docker compose (plugin) | docker-compose (Python) |
|---------|------------------------|------------------------|
| Installation | Docker Desktop/cli plugin | pip install |
| Performance | Native Go (nhanh hơn) | Python |
| Features | BuildKit, profiles, watch | Limited |
| Compatibility | Mostly compatible | Older features |
| Recommendation | ✅ Dùng mới | Legacy |


---

## docker network

**Mục đích**: Quản lý Docker networks - isolation và communication giữa containers.

### Why Networks?
- Mỗi container mặc định kết nối đến **bridge network** `bridge`
- Containers trên cùng network có thể communicate với nhau qua tên service
- Networks giúp **isolate** containers (không thể ping sang network khác)
- Different networks cho different app tiers (frontend, backend, db)

### Commands Overview
| Subcommand | Mô tả | Example |
|------------|-------|---------|
| `create` | Tạo network mới | `docker network create mynet` |
| `ls` | List networks | `docker network ls` |
| `inspect` | Xem chi tiết network | `docker network inspect mynet` |
| `connect` | Connect container vào network | `docker network connect mynet container` |
| `disconnect` | Ngắt kết nối khỏi network | `docker network disconnect mynet container` |
| `rm` | Xóa network | `docker network rm mynet` |
| `prune` | Xóa unused networks | `docker network prune` |

### docker network create
```bash
# Tạo bridge network (default)
docker network create mynetwork

# Tạo với subnet cụ thể
docker network create --subnet=192.168.100.0/24 mynet

# Tạo với gateway
docker network create --gateway=192.168.100.1 --subnet=192.168.100.0/24 mynet

# Tạo network cho IPv6
docker network create --ipv6 --subnet=2001:db8::/64 mynet6

# Tạo internal network (no external access)
docker network create --internal internal-net

# Tạo attachable network (non-swarm)
docker network create --attachable mynet

# Tạo với driver options
docker network create -o "com.docker.network.bridge.name"="br0" mynet
```

**Network drivers**:
- **bridge**: Default, isolated network trên single host
- **host**: Container dùng host's network stack (no isolation)
- **overlay**: Multi-host networks (Swarm mode)
- **macvlan**: Gán MAC address trực tiếp (legacy apps)
- **none**: No network

### docker network ls
```bash
# List tất cả networks
docker network ls

# Filter theo driver
docker network ls -f driver=bridge

# Filter theo name
docker network ls -f name=mynet

# Format output
docker network ls --format "table {{.ID}}\t{{.Name}}\t{{.Driver}}"
```

### docker network inspect
```bash
# Xem chi tiết network
docker network inspect mynet

# Xem containers trên network
docker network inspect mynet --format '{{json .Containers}}' | jq

# JSON output
docker network inspect mynet --format json | jq '.IPAM.Config'
```

**Inspect output includes**:
- **ID**: Network ID
- **Name**: Network name
- **Driver**: bridge/host/overlay/...
- **Scope**: local, swarm, global
- **EnableIPv6**: IPv6 enabled?
- **IPAM**: IP address management (subnet, gateway, IP range)
- **Containers**: List containers connected (với IDs và IPs)
- **Options**: Driver-specific options

### docker network connect/disconnect
```bash
# Connect running container vào network
docker network connect mynet mycontainer

# Connect với static IP
docker network connect --ip 192.168.100.10 mynet mycontainer

# Disconnect container
docker network disconnect mynet mycontainer

# Force disconnect (kill connections)
docker network disconnect -f mynet mycontainer
```

**Note**: Container có thể connect đến **multiple networks**. Mỗi network interface có IP riêng.

### docker network rm
```bash
# Xóa network (phải không có container đang dùng)
docker network rm mynet

# Xóa nhiều networks
docker network rm net1 net2 net3

# Error: network has active endpoints
# → Disconnect containers trước: docker network disconnect
```

### docker network prune
```bash
# Xóa tất cả unused networks
docker network prune

# Force (no prompt)
docker network prune -f
```

**Unused networks**: Không có container nào connect (dangling)

### Network Driver Details

#### Bridge Network (Default)
- Tạo virtual bridge `docker0` (hoặc custom)
- Containers nhận IP từ subnet (default: `172.17.0.0/16`)
- NAT qua host IP cho external access
- Communication qua **network namespace isolation**

```bash
# Default bridge network
docker network create mybridge
docker run -d --name app1 --network mybridge nginx
docker run -it --network mybridge alpine ping app1  # Ping by name!
```

#### Host Network
- Container **chia sẻ** host's network namespace
- Không có isolation, port mapping không cần thiết
- Performance tốt hơn (no NAT)

```bash
docker run --network host nginx  # Nginx chạy port 80 trực tiếp trên host
```

#### Overlay Network (Swarm)
- Multi-host networking (Swarm cluster)
- Encapsulation (VXLAN) giữa các host
- Requires Swarm mode: `docker swarm init`

```bash
docker network create --driver overlay myoverlay
```

### Common Examples
```bash
# Tạo app network riêng
docker network create app-net

# Chạy containers cùng network
docker run -d --name db --network app-net postgres
docker run -d --name web --network app-net -p 8080:80 myapp

# Container có thể ping nhau qua tên
docker exec web ping db  # Works!

# Xem IP của container
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web

# Connect container tồn tại vào network
docker network connect app-net existing-container

# Isolate container (chỉ internal network)
docker network create --internal isolated
docker run --network isolated alpine

# Cleanup unused networks
docker network prune -f
```

### Troubleshooting
```bash
# Container không ping được nhau?
# → Check cùng network không: docker network inspect
# → Check firewall rules
# → Check if using bridge vs host

# Port không reachable từ outside?
# → Check port mapping: docker ps (PORTS column)
# → Check firewall: ufw, firewalld, iptables

# IP conflict?
# → Custom subnet đã dùng chưa?
# → Check: docker network inspect

# Cannot remove network?
# → Containers vẫn connect: docker network disconnect
# → Or use: docker network rm -f (force)
```

### Notes
- **Default bridge** (`bridge`) không hỗ trợ automatic DNS resolution - phải dùng `--link` (deprecated) hoặc `--network` custom
- **Custom bridge** networks hỗ trợ automatic service discovery (ping by name)
- **Host network**: Không thể port map (`-p` ignored), container dùng port trực tiếp
- **Network namespaces**: Mỗi network là namespace riêng, containers cùng network có thể communicate
- **iptables**: Docker tự động tạo iptables rules cho NAT và firewall
- **Performance**: Host > Bridge > Overlay (vì overhead)

### Security Considerations
- **Network segmentation**: Dùng separate networks cho different security zones
- **Internal-only networks**: `--internal` cho DB, không expose ra outside
- **No external access**: Default bridge block incoming từ outside (trừ ports mapped)
- **Overlay networks**: Encrypted by default (in Swarm mode)
- **Macvlan**: Direct L2 access - cẩn thận với security


---

## docker volume

**Mục đích**: Quản lý volumes - persistent storage cho containers.

### Why Volumes?
- **Persist data** khi container dừng/xóa (không như bind mounts trên host)
- **Performance** tốt hơn bind mounts (trên some platforms)
- **Portable**: Volumes có thể move giữa containers
- **Backup/restore**: Dễ dàng backup volumes
- **Managed bởi Docker**: Không cần tự quản lý thư mục host

### Commands Overview
| Subcommand | Mô tả | Example |
|------------|-------|---------|
| `create` | Tạo volume mới | `docker volume create myvol` |
| `ls` | List volumes | `docker volume ls` |
| `inspect` | Xem chi tiết volume | `docker volume inspect myvol` |
| `rm` | Xóa volume | `docker volume rm myvol` |
| `prune` | Xóa unused volumes | `docker volume prune` |

### docker volume create
```bash
# Tạo volume với driver mặc định (local)
docker volume create myvol

# Tạo với driver cụ thể
docker volume create --driver local myvol

# Tạo với options (mountpoint, device,...)
docker volume create -o o=size=10G,device=/dev/sdb myvol

# Tạo volume cho特定 use case
docker volume create --label env=prod db-data
```

**Volume drivers** (nâng cao):
- **local**: Default, thư mục trên host (`/var/lib/docker/volumes/...`)
- **nfs**: NFS mount
- **cifs**: SMB/CIFS share
- **cloud** (aws, azure, gcp): Cloud storage backends
- **third-party**: Portworx, RexRay, Convoy,...

### docker volume ls
```bash
# List tất cả volumes
docker volume ls

# Filter theo driver
docker volume ls -f driver=local

# Filter theo label
docker volume ls -f label=env=prod

# Filter theo name
docker volume ls -f name=myvol

# Format output
docker volume ls --format "table {{.Name}}\t{{.Driver}}"
```

### docker volume inspect
```bash
# Xem chi tiết volume
docker volume inspect myvol

# Xem mountpoint (path trên host)
docker volume inspect -f '{{.Mountpoint}}' myvol

# Xem labels
docker volume inspect -f '{{json .Labels}}' myvol | jq

# Xem tất cả options
docker volume inspect myvol --format '{{json .Options}}' | jq
```

**Inspect output includes**:
- **Name**: Volume name
- **Driver**: Volume driver (local, nfs, ...)
- **Mountpoint**: Path trên host (cho driver=local)
- **Labels**: Volume labels (key=value)
- **Scope**: local, global
- **Options**: Driver-specific options

### docker volume rm
```bash
# Xóa volume (volume phải không có container dùng)
docker volume rm myvol

# Xóa nhiều volumes
docker volume rm vol1 vol2 vol3

# Force remove (Docker Desktop/Windows sometimes)
docker volume rm -f myvol  # Not always supported
```

**Lưu ý**: Volume không tự động xóa khi container xóa. Phải xóa thủ công hoặc dùng `docker compose down -v`.

### docker volume prune
```bash
# Xóa tất cả unused volumes (không có container mount)
docker volume prune

# Force (no prompt)
docker volume prune -f

# Chỉ prune với filter
docker volume prune -f --filter "label!=keep"
```

### Mount Volumes vào Containers
```bash
# Tạo volume
docker volume create db-data

# Mount vào container (docker run)
docker run -d -v db-data:/var/lib/postgresql/data postgres

# Hoặc dùng --mount (recommended)
docker run -d --mount source=db-data,target=/var/lib/postgresql/data postgres

# Multiple volumes
docker run -d \
  -v db-data:/var/lib/postgresql/data \
  -v logs:/var/log/postgresql \
  postgres
```

### docker-compose.yml với volumes
```yaml
services:
  db:
    image: postgres
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./backups:/backups  # Bind mount (host path)

volumes:
  db-data:  # Named volume (Docker managed)
    driver: local
    labels:
      env: prod
```

### Bind Mounts vs Named Volumes
| Feature | Named Volume | Bind Mount |
|---------|--------------|------------|
| **Location** | Managed bởi Docker (`/var/lib/docker/volumes/`) | Any host path |
| **Portability** | ✅ Có thể dùng trên any host | ❌ Phụ thuộc host path |
| **Performance** | ✅ Tốt (trên Windows/Mac) | Tốt (trên Linux) |
| **Backup** | ✅ Dễ (docker volume commands) | ❌ Phải quản lý thủ công |
| **Permissions** | Docker tự quản lý | Phải handle permission host |
| **Use case** | Database data, app state | Config files, source code, logs |

**Example**:
```bash
# Named volume (Docker managed)
docker volume create app-data
docker run -v app-data:/app/data myapp

# Bind mount (host directory)
docker run -v /home/user/data:/app/data myapp

# Read-only bind mount
docker run -v /config:/etc/app:ro myapp
```

### Backup & Restore
```bash
# Backup volume
docker run --rm -v myvol:/source -v $(pwd):/backup alpine \
  tar czf /backup/myvol-backup.tar.gz -C /source .

# Restore volume
docker run --rm -v myvol:/target -v $(pwd):/backup alpine \
  sh -c "cd /target && tar xzf /backup/myvol-backup.tar.gz"

# List volume contents
docker run --rm -v myvol:/data alpine ls -la /data
```

### Common Examples
```bash
# Database persistent storage
docker volume create pg-data
docker run -d -v pg-data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=secret postgres

# Application logs (persistent)
docker volume create app-logs
docker run -d -v app-logs:/var/log/myapp myapp

# Share volume giữa containers
docker volume create shared
docker run -d -v shared:/data --name container1 alpine sh -c "echo hello > /data/file"
docker run --rm -v shared:/data alpine cat /data/file  # Output: hello

# Development: Mount source code (bind mount preferred)
docker run -d -v $(pwd):/app -p 3000:3000 node:18 npm start

# Cleanup unused volumes
docker volume prune -f
```

### Troubleshooting
```bash
# Volume full?
docker system df -v  # Show volume sizes

# Permission denied?
# → Check SELinux/AppArmor
# → Use :z or :Z flag for SELinux relabel
docker run -v /host/path:/container:z myapp

# Volume not mounting?
docker inspect container | grep -A5 Mounts

# Cannot remove volume?
# → Container đang dùng: docker ps | grep volume name
# → Stop container: docker stop container
# → Or force remove: docker rm -vf container

# Performance slow (Mac/Windows)?
# → Named volumes faster than bind mounts
# → Consider docker-sync or Mutagen for dev
```

### Notes
- Volumes **persist** sau khi container bị xóa (trừ khi dùng `--rm`)
- Docker Desktop (Mac/Windows): volumes stored trong VM (Linux), không phải host filesystem trực tiếp
- **tmpfs mounts**: Temporary storage trong memory (không persist)
  ```bash
  docker run --tmpfs /tmp alpine
  ```
- `docker-compose down -v`: Xóa volumes định nghĩa trong compose file
- Volume drivers: Có thể dùng remote storage (NFS, cloud storage)
- **Read-only volumes**: `-v volume:/path:ro`
- **Volume claims** (Kubernetes): Different concept (PersistentVolumeClaim)

### Security Considerations
- **Volumes có thể escape container**: Mount sensitive host dirs (cẩn thận với bind mounts)
- **SELinux**: Dùng `:z` (shared) hoặc `:Z` (private) labels
- **No root**: Run container với non-root user, nhưng volume permission có thể issue
- **Data encryption**: Volumes không encrypted by default - dùng driver có encryption hoặc encrypt filesystem

### Best Practices
- **Named volumes** cho stateful apps (databases)
- **Bind mounts** cho development (source code, configs)
- **Read-only** khi chỉ cần read access
- **Labels** để organize volumes (env, app, backup schedule)
- **Backup regularly**: Volumes là single point of failure
- **Size limits**: Dùng driver options (thick/thin provisioning) nếu cần


---

## docker system

**Mục đích**: System-wide management của Docker - cleanup, disk usage, events.

### Commands Overview
| Subcommand | Mô tả | Example |
|------------|-------|---------|
| `df` | Show Docker disk usage | `docker system df` |
| `events` | Real-time events từ daemon | `docker system events --format '{{.Type}} {{.Action}}'` |
| `info` | System-wide info (alias `docker info`) | `docker system info` |
| `prune` | Remove unused data (images, containers, volumes, networks) | `docker system prune` |

### docker system df (Disk Usage)
```bash
# Show disk usage summary
docker system df

# Show với verbose (detailed)
docker system df -v

# Output format
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          50        10        15GB      10GB
Containers      20        5         500MB     300MB
Local Volumes  30        8         20GB      15GB
Build Cache    100       20        5GB       4GB
```

**Columns**:
- **TOTAL**: Total objects (images, containers, volumes, build cache)
- **ACTIVE**: Objects đang được sử dụng (running containers, pulled images,...)
- **SIZE**: Tổng dung lượng chiếm dụng
- **RECLAIMABLE**: Dung lượng có thể reclaim bằng prune (unused objects)

### docker system prune (Cleanup)
```bash
# Prune tất cả unused objects (images, containers, networks, volumes)
docker system prune

# Prune với các options cụ thể
docker system prune --all                    # Prune all (default filters)
docker system prune --volumes               # Include volumes
docker system prune --filter "until=24h"    # Only older than 24h

# Force prune (no prompt)
docker system prune -af
docker system prune -a --volumes -f
```

**Prune behavior**:
- **Images**: Remove dangling và unused tagged images
- **Containers**: Remove stopped containers
- **Networks**: Remove unused networks
- **Volumes**: Chỉ prune nếu dùng `--volumes`
- **Build cache**: Remove build cache không dùng

### docker system prune (More Control)
```bash
# Prune cụ thể từng loại
docker image prune        # Chỉ images
docker container prune    # Chỉ containers
docker volume prune       # Chỉ volumes
docker network prune      # Chỉ networks
docker builder prune      # Chỉ build cache

# Prune với filters
docker system prune --filter "until=24h"       # Older than 24h
docker system prune --filter "label!=keep"    # Exclude labeled
docker system prune --filter "until=10m"      # Last 10 minutes
docker system prune --filter "until=2024-01-01"  # Before date
```

### docker system events (Monitoring)
```bash
# Follow tất cả events real-time
docker system events

# Filter theo type
docker system events --filter 'type=container'
docker system events --filter 'type=image'
docker system events --filter 'type=volume'
docker system events --filter 'type=network'

# Filter theo action
docker system events --filter 'event=create'
docker system events --filter 'event=destroy'
docker system events --filter 'event=die'
docker system events --filter 'event=start'
docker system events --filter 'event=stop'

# Filter theo container
docker system events --filter 'container=abc123'

# Format output
docker system events --format '{{.Time}} {{.Type}} {{.Action}} {{.ID}}'
docker system events --format json | jq

# Events đến một thời điểm cụ thể
docker system events --since '2024-01-01T00:00:00'
docker system events --until '10m'  # Past 10 minutes only
```

**Common event types**:
- `container`: create, destroy, die, kill, pause, restart, start, stop, unpause
- `image`: pull, push, tag, untag, delete, import, save, load, remove
- `volume`: create, mount, unmount, delete, destroy
- `network`: create, connect, disconnect, destroy, remove
- `daemon`: configure, reload

### Common Workflows
```bash
# 1. Check disk usage trước khi cleanup
docker system df -v

# 2. Prune unused (safe cleanup)
docker system prune -a --volumes  # CAUTION: xóa volumes!

# 3. Verify sau prune
docker system df

# Monitor events (debug)
docker system events --filter 'event=die' &

# Cleanup cũ hơn 7 ngày
docker system prune --filter "until=168h" -f
```

### Safety & Best Practices
```bash
# NEVER prune production volumes
docker system prune --volumes  # ❌ DANGER: Có thể mất data!

# Safer: Prune từng loại
docker system prune -a          # Prune images, containers, networks
# → Volumes không bị xóa

# Backup volumes trước khi prune volumes
docker run --rm -v myvol:/data -v $(pwd):/backup alpine \
  tar czf /backup/myvol-backup.tar.gz -C /data .

# Use filters để tránh mất data mới
docker system prune --filter "until=168h"  # Chỉ > 7 ngày

# Label volumes quan trọng và exclude khỏi prune
docker volume create --label keep=true important-data
docker system prune --filter "label!=keep"
```

### Disk Usage Breakdown
```bash
# Detailed breakdown by images
docker system df -v --format json | jq '.Images'

# Largest images
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}" | sort -k2 -h | tail -10

# Largest volumes
docker volume ls --format "{{.Name}}" | while read vol; do
  size=$(docker run --rm -v $vol:/data alpine du -sm /data 2>/dev/null | cut -f1)
  echo "$size MB\t$vol"
done | sort -rn | head -10

# Stopped containers (có thể prune)
docker ps -a --filter "status=exited" --format "{{.ID}} {{.CreatedAt}} {{.Status}}"
```

### Troubleshooting
```bash
# Disk full?
df -h
docker system df -v

# Cannot prune because volumes in use?
# → Stop containers trước: docker stop $(docker ps -q)
# → Or remove containers: docker rm -f $(docker ps -aq)

# Prune không giải phóng nhiều?
# → Check volumes: docker volume ls (lớn nhất)
# → Check build cache: docker builder du
# → Check dangling images: docker images -f dangling=true

# Reclaim space nhanh
docker system prune -a --volumes -f  # NGHIÊM TÚC: xóa tất cả unused
docker builder prune -af             # Clear build cache
docker image prune -a -f             # Clear all unused images
```

### Automation (Cron Job)
```bash
# Weekly cleanup (dont prune volumes!)
0 2 * * 0 docker system prune -a -f

# Monthly deep clean (with volumes - cẩn thận!)
0 3 1 * * docker system prune -a --volumes -f

# Daily cleanup cũ hơn 30 ngày
0 4 * * * docker system prune --filter "until=720h" -f
```

### Notes
- `docker system df` chỉ **estimate** - actual usage có thể khác (filesystem overhead)
- `prune` **không xóa**:
  - Running containers
  - Images đang dùng bởi containers
  - Volumes đang mount
  - Networks đang dùng
- `docker system prune -a` xóa cả **tagged images** không dùng (not just dangling)
- **Build cache** (builder prune) có thể lớn nếu build thường xuyên
- `docker system prune` **không prompt** với `-f` (dangerous!)
- **Never prune** volumes có data quan trọng (DB data)
- Docker Desktop: Giới hạn disk space trong Settings → Resources

### Related Commands
- `docker image prune`: Prune images only
- `docker container prune`: Prune containers only
- `docker volume prune`: Prune volumes only
- `docker builder prune`: Prune build cache only
- `docker network prune`: Prune networks only
- `docker system df`: Disk usage summary


---

## docker image

**Mục đích**: Quản lý Docker images (alias của các lệnh riêng lẻ như `docker images`, `docker rmi`, `docker tag`,...).

### Commands Overview
| Subcommand | Equivalent | Mô tả |
|------------|------------|-------|
| `ls` | `docker images` | List images |
| `rm` | `docker rmi` | Remove images |
| `prune` | `docker image prune` | Remove unused images |
| `tag` | `docker tag` | Create tag/repository name |
| `inspect` | `docker inspect` | Detailed info |
| `history` | `docker history` | Show layer history |
| `pull` | `docker pull` | Download from registry |
| `push` | `docker push` | Upload to registry |
| `build` | `docker build` | Build from Dockerfile |
| `load` | `docker load` | Load from tar archive |
| `save` | `docker save` | Save to tar archive |
| `import` | `docker import` | Import from tarball (no Dockerfile) |

### Quick Reference (sử dụng các subcommand)
```bash
# List
docker image ls

# Remove
docker image rm nginx:alpine
docker image rm -f $(docker images -q -f dangling=true)  # Force remove dangling

# Tag
docker image tag source:tag target:tag
docker image tag myapp:latest myregistry/myapp:v1.0

# Inspect
docker image inspect nginx:alpine
docker image inspect --format '{{.Architecture}}' nginx

# History (layers)
docker image history nginx:alpine

# Pull/Push
docker image pull nginx:alpine
docker image push myuser/myapp:latest

# Build
docker image build -t myapp:latest .

# Save/Load (backup/transfer)
docker image save -o myapp.tar myapp:latest
docker image load -i myapp.tar

# Prune
docker image prune -a  # Remove all unused (not just dangling)
```

### Differences: docker image vs standalone
- **`docker images`** = **`docker image ls`**
- **`docker rmi`** = **`docker image rm`**
- **`docker tag`** = **`docker image tag`**
- **`docker pull`** = **`docker image pull`**
- **`docker push`** = **`docker image push`**
- **`docker history`** = **`docker image history`**

✅ **Recommendation**: Dùng `docker image` commands vì consistent, nhưng standalone commands vẫn works và phổ biến hơn.

### Notes
- `docker image` commands tương đương với standalone counterparts
- See individual command sections trong cheatsheet này cho chi tiết:
  - `docker images` (section `docker images`)
  - `docker rmi` (alias `docker image rm`)
  - `docker tag` (section `docker tag`)
  - `docker pull/push` (sections `docker pull`, `docker push`)
  - `docker build` (section `docker build`)
  - `docker history`, `docker inspect`, `docker save`, `docker load`, `docker import`

### When to Use Which?
| Task | Command |
|------|---------|
| List images | `docker images` (shorter) hoặc `docker image ls` |
| Remove image | `docker rmi` (shorter) hoặc `docker image rm` |
| Tag image | `docker tag` (shorter) hoặc `docker image tag` |
| Pull/push | `docker pull/push` (shorter) hoặc `docker image pull/push` |

**Takeaway**: Dùng gì cũng được, nhưng community thường dùng standalone commands (không có `image` prefix).


---

## docker container

**Mục đích**: Quản lý containers (command group - alias của các lệnh riêng lẻ).

### Equivalent Standalone Commands
| docker container | Equivalent | Section trong cheatsheet |
|------------------|------------|--------------------------|
| `ls` | `docker ps` | `docker ps` |
| `run` | `docker run` | `docker run` |
| `exec` | `docker exec` | `docker exec` |
| `rm` | `docker rm` | (see below) |
| `stop/start/restart` | `docker stop/start/restart` | (see below) |
| `logs` | `docker logs` | (see below) |
| `inspect` | `docker inspect` | (see below) |
| `stats` | `docker stats` | (see below) |
| `kill` | `docker kill` | (see below) |
| `pause/unpause` | `docker pause/unpause` | (see below) |
| `commit` | `docker commit` | (see below) |
| `cp` | `docker cp` | (see below) |
| `create` | `docker create` | (see below) |
| `port` | `docker port` | (see below) |

### Các lệnh chưa có section riêng

#### docker container rm (Remove containers)
```bash
# Remove một container
docker container rm mycontainer

# Remove nhiều containers
docker container rm container1 container2

# Force remove (running container)
docker container rm -f mycontainer  # Same as docker kill + rm

# Remove tất cả stopped containers
docker container rm $(docker container ls -aq -f status=exited)

# Prune tất cả stopped containers
docker container prune
```

#### docker container stop/start/restart
```bash
# Stop container (graceful SIGTERM)
docker container stop mycontainer
docker container stop -t 30 mycontainer  # Wait 30s before SIGKILL

# Start stopped container
docker container start mycontainer

# Restart container (stop rồi start)
docker container restart mycontainer
docker container restart -t 10 mycontainer  # Wait 10s between

# Stop all running containers
docker container stop $(docker container ls -q)
```

#### docker container logs
```bash
# Show logs
docker container logs mycontainer

# Follow logs (real-time)
docker container logs -f mycontainer

# Show với timestamps
docker container logs -t mycontainer

# Show last N lines
docker container logs --tail 100 mycontainer

# Since timeframe
docker container logs --since 10m mycontainer

# Until timeframe
docker container logs --until 5m mycontainer

# Show logs từ specific container ID prefix
docker container logs abc123
```

#### docker container inspect
```bash
# Full JSON details
docker container inspect mycontainer

# Specific field
docker container inspect -f '{{.State.Running}}' mycontainer
docker container inspect -f '{{.NetworkSettings.IPAddress}}' mycontainer
docker container inspect -f '{{.Mounts}}' mycontainer

# Multiple fields
docker container inspect -f '{{.Name}} {{.State.Status}} {{.Config.Image}}' mycontainer
```

#### docker container stats (Resource usage)
```bash
# Real-time stats cho tất cả containers
docker container stats

# Stats cho specific container
docker container stats mycontainer

# Format output (custom)
docker container stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# No stream (one-time snapshot)
docker container stats --no-stream

# Format JSON
docker container stats --format json | jq
```

**Stats columns**:
- **CONTAINER**: Container name/ID
- **CPU %**: CPU usage percentage
- **MEM USAGE / LIMIT**: Memory used / limit
- **MEM %**: Memory percentage
- **NET I/O**: Network input/output
- **BLOCK I/O**: Block device I/O
- **PIDS**: Number of processes

#### docker container kill
```bash
# Kill container (SIGKILL - force)
docker container kill mycontainer

# Kill với specific signal
docker container kill -s SIGTERM mycontainer
docker container kill -s SIGINT mycontainer
docker container kill -s SIGHUP mycontainer

# Kill nhiều containers
docker container kill container1 container2

# Kill all running containers
docker container kill $(docker container ls -q)
```

**kill vs stop**:
- `stop`: Graceful shutdown (SIGTERM → wait → SIGKILL)
- `kill`: Immediate SIGKILL (force)

#### docker container pause/unpause
```bash
# Pause container (freeze all processes)
docker container pause mycontainer

# Unpause container
docker container unpause mycontainer

# Unpause nhiều containers
docker container unpause container1 container2
```

**Lưu ý**: `pause` dùng cgroups freezer - tất cả processes trong container bị frozen. Không dùng với critical services.

#### docker container commit
```bash
# Create image từ container changes
docker container commit mycontainer mynewimage:tag

# Commit với author và message
docker container commit -a "Alice" -m "Updated config" mycontainer myimage:v2

# Pause container trước khi commit (recommended)
docker container pause mycontainer
docker container commit mycontainer myimage:v2
docker container unpause mycontainer

# Include specific changes (not all)
docker container commit --change='ENV DEBUG=true' mycontainer myimage:debug
```

**Use cases**:
- Snapshot container state (debug, troubleshooting)
- Create base image từ running container
- Save changes sau khi troubleshoot

**Không dùng commit trong production** - nên rebuild với Dockerfile.

#### docker container cp (Copy files)
```bash
# Copy từ container → host
docker container cp mycontainer:/path/to/file ./local/path

# Copy từ host → container
docker container cp ./local/file mycontainer:/path/in/container

# Copy directory
docker container cp mycontainer:/app ./app-backup
docker container cp ./config mycontainer:/etc/app

# Copy với sudo (nếu permission issue)
sudo docker container cp mycontainer:/root/file ./
```

**Tips**:
- Container không cần chạy để copy (dừng vẫn được)
- Preserves permissions, ownership
- Nhanh với small files, chậm với large directories

#### docker container create (Create but not start)
```bash
# Create container (not running)
docker container create --name myapp nginx

# Create với options
docker container create \
  --name myapp \
  -p 8080:80 \
  -v data:/var/lib \
  -e ENV=prod \
  nginx:alpine

# Create rồi start
docker container create --name myapp nginx
docker container start myapp

# Create với command override
docker container create --name test alpine echo "Hello World"
docker container start test  # Will print "Hello World" rồi exit
```

**create vs run**:
- `docker create`: Tạo container nhưng không start (dùng để prepare)
- `docker run`: Tạo và start ngay

#### docker container port
```bash
# Xem port mapping của container
docker container port mycontainer

# Specific port
docker container port mycontainer 80
docker container port mycontainer 443

# Output format
docker container port mycontainer 80 --format "{{.HostPort}}"
```

**Example output**:
```
80/tcp -> 0.0.0.0:8080
443/tcp -> 0.0.0.0:8443
```

#### docker container top (Processes inside)
```bash
# List processes trong container
docker container top mycontainer

# Custom format
docker container top mycontainer -o pid,comm

# Similar to ps inside container
docker container top mycontainer aux
```

**Equivalent**: `docker exec mycontainer ps aux`

#### docker container attach
```bash
# Attach vào running container's STDIN/STDOUT/STDERR
docker container attach mycontainer

# Attach với SIG forwarding
docker container attach --sig-proxy=true mycontainer

# Detach với key sequence (default: Ctrl+p Ctrl+q)
docker container attach mycontainer
# Press: Ctrl+p, Ctrl+q để detach (không stop container)
```

**attach vs exec**:
- `attach`: Kết nối vào **main process** (PID 1) - input/output stream
- `exec`: Tạo **new process** trong container (không ảnh hưởng main process)

**Use attach khi**:
- Container chạy interactive process (bash, python REPL,...)
- Muốn xem logs trực tiếp từ main process

**Use exec khi**:
- Container đang chạy background process
- Muốn vào shell để debug

#### docker container diff
```bash
# Show changes in container's filesystem
docker container diff mycontainer

# Output:
# A /etc/newfile      (Added)
# C /etc/config       (Changed)
# D /tmp/oldfile      (Deleted)
```

**Use case**: Xem container đã thay đổi gì so với base image.

#### docker container export
```bash
# Export container's filesystem as tar
docker container export mycontainer -o mycontainer-fs.tar

# Export to stdout (pipe)
docker container export mycontainer | gzip > mycontainer-fs.tar.gz

# Import exported tar as image
docker image import mycontainer-fs.tar mynewimage:tag
```

**export vs save**:
- `export`: Container filesystem (no history, no metadata)
- `save`: Image với layers, history, metadata (recommended)

#### docker container wait
```bash
# Block until container stops, then print exit code
docker container wait mycontainer

# Wait nhiều containers
docker container wait container1 container2

# Use trong scripts
EXIT_CODE=$(docker container wait mycontainer)
echo "Container exited with code $EXIT_CODE"

# Wait với timeout (cần wrapper)
timeout 30s docker container wait mycontainer
```

**Use case**: Scripts cần biết khi container exit.

#### docker container update (Live update)
```bash
# Update container config (running)
docker container update \
  --cpu-shares 512 \
  --memory 512M \
  --restart on-failure:3 \
  mycontainer

# Update kernel params
docker container update --kernel-memory 256M mycontainer

# Update restart policy
docker container update --restart unless-stopped mycontainer
```

**Limitations**: Chỉ update subset của config (memory, cpu, restart). Không thể update:
- Port mappings
- Volume mounts
- Network
- Image

**Require**: Container đang running (hoặc paused).

#### docker container prune
```bash
# Remove tất cả stopped containers
docker container prune

# Force (no prompt)
docker container prune -f

# With filter
docker container prune --filter "until=24h"
docker container prune --filter "label!=keep"
```

### Notes on docker container commands
- Tất cả `docker container X` có equivalent `docker X` (không cần `container`)
- Community thường dùng `docker ps`, `docker rm`, `docker logs` (không có prefix `container`)
- `docker container` commands chỉ là wrapper consistent
- Xem help cho từng subcommand: `docker container COMMAND --help`

### Container Lifecycle
```
create → start → (running) → stop → rm
         ↑
      restart
      pause/unpause
      update (config)
      exec (run commands)
      attach (connect)
```


---

## docker events

**Mục đích**: Stream real-time events từ Docker daemon - monitoring và debugging.

### Syntax cơ bản
```bash
docker events [OPTIONS]
```

**Ví dụ đơn giản**:
```bash
docker events                    # Stream tất cả events (Ctrl+C để stop)
docker events --filter 'event=die'  # Only die events
docker events --since 10m        # Events từ 10 phút trước
docker events --format '{{.Time}} {{.Action}} {{.ID}}'  # Custom format
```

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `-f, --filter` | Lọc events theo type/action/... | `docker events -f type=container` |
| `--format` | Format output với template | `docker events --format '{{.Type}} {{.Action}}'` |
| `--since` | Events từ timestamp/relative | `docker events --since 1h` |
| `--until` | Events đến timestamp/relative | `docker events --until 5m` |

### Event Types & Actions
Docker events có nhiều **types** và **actions**:

#### Container Events
| Type | Action | Meaning |
|------|--------|---------|
| `container` | `create` | Container được tạo |
| `container` | `destroy` | Container bị xóa |
| `container` | `die` | Container dừng (process exit) |
| `container` | `kill` | Container bị kill (SIGKILL) |
| `container` | `pause` | Container paused |
| `container` | `start` | Container start |
| `container` | `stop` | Container stop (graceful) |
| `container` | `unpause` | Container unpaused |
| `container` | `restart` | Container restart |

#### Image Events
| Type | Action | Meaning |
|------|--------|---------|
| `image` | `pull` | Image pulled từ registry |
| `image` | `push` | Image pushed lên registry |
| `image` | `tag` | Image tagged |
| `image` | `untag` | Image untagged |
| `image` | `delete` | Image deleted |
| `image` | `import` | Image imported |
| `image` | `save` | Image saved |
| `image` | `load` | Image loaded |

#### Volume Events
| Type | Action | Meaning |
|------|--------|---------|
| `volume` | `create` | Volume tạo |
| `volume` | `mount` | Volume mount vào container |
| `volume` | `unmount` | Volume unmount |
| `volume` | `destroy` | Volume xóa |

#### Network Events
| Type | Action | Meaning |
|------|--------|---------|
| `network` | `create` | Network tạo |
| `network` | `connect` | Container connect vào network |
| `network` | `disconnect` | Container disconnect khỏi network |
| `network` | `destroy` | Network xóa |

#### Daemon Events
| Type | Action | Meaning |
|------|--------|---------|
| `daemon` | `configure` | Daemon config thay đổi |
| `daemon` | `reload` | Daemon reload config |

### Filtering
```bash
# theo type
docker events --filter 'type=container'
docker events --filter 'type=image'
docker events --filter 'type=volume'
docker events --filter 'type=network'
docker events --filter 'type=daemon'

# theo action
docker events --filter 'event=start'
docker events --filter 'event=stop'
docker events --filter 'event=die'
docker events --filter 'event=create'
docker events --filter 'event=destroy'

# theo container
docker events --filter 'container=abc123'
docker events --filter 'container=mycontainer'

# theo image
docker events --filter 'image=nginx'

# theo volume
docker events --filter 'volume=myvol'

# theo network
docker events --filter 'network=mynet'

# Combine filters (AND)
docker events --filter 'type=container' --filter 'event=die'
docker events --filter 'type=container' --filter 'container=myapp'
```

### Format Templates
```bash
# Simple format
docker events --format '{{.Time}} {{.Type}} {{.Action}} {{.ID}}'

# JSON
docker events --format json | jq .

# Table
docker events --format "table {{.Time}}\t{{.Type}}\t{{.Action}}\t{{.ID}}"

# Custom với actor name
docker events --format '{{.Time}} {{.Actor.Name}} {{.Action}}'

# Chỉ specific fields
docker events --format '{{.Action}} - {{if eq .Type "container"}}{{.Actor.Name}}{{end}}'
```

### Time-based Filtering
```bash
# Events trong 5 phút gần đây
docker events --since 5m

# Events trong 1 giờ qua
docker events --since 1h

# Events từ specific time
docker events --since '2024-01-01T00:00:00'

# Events đến 10 phút tới (stream until)
docker events --until 10m

# Events trong 1 ngày cụ thể
docker events --since '2024-01-01' --until '2024-01-02'
```

**Time format**:
- Relative: `5m`, `1h`, `2d` (minutes, hours, days)
- Absolute: `2024-01-01T15:04:05` (RFC3339)
- Timestamp: `@1704038400` (unix timestamp)

### Common Use Cases
```bash
# Monitor container lifecycle (debug)
docker events --filter 'type=container' --filter 'event=die'

# Track image pulls
docker events --filter 'type=image' --filter 'event=pull' --format '{{.Time}} {{.Actor.Name}} pulled'

# Watch volume mounts
docker events --filter 'type=volume' --filter 'event=mount'

# Audit: Xem ai tạo/delete resource
docker events --format '{{.Time}} {{.Actor.Name}} {{.Action}} {{.ID}}' | grep -E 'create|delete'

# Log events to file (background)
docker events --format json > docker-events.log &

# Count events by type
docker events --since 1h --format '{{.Type}}' | sort | uniq -c

# Debug specific container
docker events --filter 'container=myapp' --since 1h

# Check when image was last pulled
docker events --filter 'type=image' --filter 'event=pull' --since 7d | tail -1
```

### Practical Examples
```bash
#!/bin/bash
# Monitor container crashes
docker events --filter 'type=container' --filter 'event=die' --format '{{.Actor.Name}} died at {{.Time}}' |
while read line; do
  echo "[ALERT] $line" | tee -a /var/log/docker-crashes.log
  # Send notification
  curl -X POST -H "Content-Type: application/json" -d "{\"text\":\"$line\"}" $SLACK_WEBHOOK
done

# Track all create/delete events (audit trail)
docker events --format json 2>/dev/null | while read -r event; do
  action=$(echo "$event" | jq -r '.Action')
  if [[ "$action" =~ ^(create|delete)$ ]]; then
    echo "$(date): $event" >> /var/log/docker-audit.log
  fi
done
```

### Output Format
Default output:
```
2024-01-15T10:30:45.123456789Z container create abc123 (image=nginx, name=myapp)
2024-01-15T10:30:46.987654321Z container start abc123
2024-01-15T10:31:00.111111111Z container die abc123 (exitCode=0)
```

**Fields**:
- **Time**: Event timestamp (nanosecond precision)
- **Type**: Event type (container, image, volume, network, daemon)
- **Action**: Event action (create, start, stop, die, ...)
- **Actor**: Object gây ra event (ID, attributes)
- **ID**: Resource ID (container/image/...)
- **From**: Image name (cho container events)
- **Name**: Container/service name (nếu có)

### Notes
- `docker events` **stream indefinitely** until Ctrl+C
- Events **real-time** với nanosecond precision
- Events **not persistent** - chỉ streaming, không lưu history (dùng audit log nếu cần)
- `--since` và `--until` có thể dùng với **past events** (Docker lưu events trong memory)
- Max events retained: phụ thuộc vào daemon config (mặc định ~1000 events)
- `docker system events` là alias của `docker events`
- Events **local only** - không có remote API (trừ remote Docker contexts)

### Troubleshooting
```bash
# No events?
# → Docker daemon có thể đang chạy nhưng không có activity
# → Check: docker ps, docker images

# Events quá nhiều?
# → Filter theo type/action: docker events -f type=container
# → Reduce noise: filter specific container

# Miss events?
# → Events chỉ available trong recent buffer
# → Use --since để lấy events từ quá khứ (nếu còn trong buffer)

# Cannot connect to daemon?
# → Check Docker daemon running: docker info
# → Check permissions: docker events yêu cầu read access
```

### Related Commands
- `docker ps`: List running containers (snapshot, not events)
- `docker logs`: Container logs (application output)
- `docker system df`: Disk usage (not events)
- `docker inspect`: Detailed info (not events)
- `docker compose logs`: Compose app logs (not daemon events)

### Use Cases Summary
| Use Case | Command |
|----------|---------|
| Debug container crashes | `docker events -f type=container -f event=die` |
| Track image activity | `docker events -f type=image` |
| Monitor volume mounts | `docker events -f type=volume` |
| Audit trail (create/delete) | `docker events --format json` |
| Real-time monitoring | `docker events --filter 'type=container'` |
| Post-mortem analysis | `docker events --since "1h ago"` |


---

## docker history

**Mục đích**: Hiển thị lịch sử layers của image - các layers đã được tạo ra trong build process.

### Syntax cơ bản
```bash
docker history [OPTIONS] IMAGE
```
- **IMAGE**: Image name hoặc ID (bắt buộc)

**Ví dụ đơn giản**:
```bash
docker history nginx:alpine
docker history myapp:latest
docker history -H ubuntu:20.04
```

### Options
| Option | Mô tả | Example |
|--------|-------|---------|
| `--format` | Format output với template | `docker history --format "table {{.ID}}\t{{.CreatedBy}}" nginx` |
| `-H, --human` | Human-readable sizes (default: true) | `docker history -H nginx` |
| `--no-trunc` | Không cắt ngắn command/description | `docker history --no-trunc nginx` |
| `--platform` | Show history cho platform cụ thể | `docker history --platform linux/arm64 nginx` |
| `-q, --quiet` | Chỉ hiển thị layer IDs | `docker history -q nginx` |

### Understanding Output
Default output columns:
```
IMAGE          CREATED       SIZE      COMMENT
abcd1234       2 weeks ago   5.61MB    /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon off;"]
efgh5678       2 weeks ago   142MB     /bin/sh -c #(nop)  EXPOSE 80
ijkl9012       2 weeks ago   61.9MB    /bin/sh -c #(nop)  ENTRYPOINT ["/docker-entrypoint.…
mnop3456       2 weeks ago   5.62MB    /bin/sh -c #(nop)  STOPSIGNAL SIGTERM
qrst7890       2 weeks ago   1.33MB    /bin/sh -c #(nop)  LABEL maintainer=NGINX Docker…
uvwx1234       2 weeks ago   37.6MB    /bin/sh -c apt-get update && apt-get install -…
yzab5678       2 weeks ago   125MB     /bin/sh -c #(nop)  FROM debian:bullseye-slim
```

**Columns**:
- **IMAGE**: Layer ID (short)
- **CREATED**: Thời gian tạo layer
- **SIZE**: Size của layer (compressed)
- **CREATED BY**: Command tạo layer (Dockerfile instruction)
- **COMMENT** (optional): Comment từ build

### Reading History (Bottom to Top)
Lịch sử đọc từ **dưới lên** (oldest → newest):
1. **Bottom** (dưới cùng): Base image (`FROM debian:bullseye-slim`)
2. **Middle**: Các layers trung gian (`RUN apt-get...`, `COPY ...`, `ADD ...`)
3. **Top** (trên cùng): Final layer với `CMD`, `ENTRYPOINT`, `LABEL`, `EXPOSE`

**Example**:
```
yzab5678   2 weeks ago   125MB     /bin/sh -c #(nop)  FROM debian:bullseye-slim
uvwx1234   2 weeks ago   37.6MB    /bin/sh -c apt-get update && apt-get install -…
...
abcd1234   2 weeks ago   5.61MB    /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon off;"]
```
→ Base: debian:bullseye-slim → apt-get install nginx → CMD nginx

### Common Commands in History
Các Dockerfile instructions xuất hiện trong history:
- `FROM <image>`: Base image layer (duy nhất)
- `RUN <command>`: Execute command (tạo layer mới)
- `COPY <src> <dst>`: Copy files (tạo layer)
- `ADD <src> <dst>`: Copy + auto-extract tar (tạo layer)
- `ENV <key>=<value>`: Set environment (tạo layer)
- `WORKDIR <path>`: Set working directory (tạo layer)
- `EXPOSE <port>`: Expose port (metadata, không tạo layer thực sự)
- `CMD ["executable"]`: Default command (final layer)
- `ENTRYPOINT ["executable"]`: Entrypoint (final layer)
- `LABEL <key>=<value>`: Metadata (tạo layer)
- `USER <name>`: Set user (tạo layer)
- `VOLUME ["/path"]`: Define volume (metadata)
- `ARG <name>`: Build argument (nếu dùng trong RUN, tạo layer)

### Format Templates
```bash
# Simple ID + command
docker history --format "{{.ID}} {{.CreatedBy}}" nginx

# Table với custom columns
docker history --format "table {{.CreatedSince}}\t{{.Size}}\t{{.CreatedBy}}"

# JSON output
docker history --format json nginx | jq '.[] | {id: .ID, cmd: .CreatedBy}'

# Chỉ layer IDs
docker history -q nginx

# Human-readable + no truncate
docker history --no-trunc -H nginx
```

### Common Use Cases
```bash
# Xem layer chain của image
docker history nginx:alpine

# Tìm layer chứa specific file/command
docker history --no-trunc nginx | grep "apt-get"

# Xem size của từng layer (optimize Dockerfile)
docker history -H myapp:latest

# Tìm base image
docker history myapp | tail -1

# Debug: Xem layer nào tạo file/directory
docker history --no-trunc myapp | grep "COPY"

# Compare images (find differences)
docker history image1 > history1.txt
docker history image2 > history2.txt
diff history1.txt history2.txt

# Get layer ID của specific layer
LAYER_ID=$(docker history -q nginx | head -1)

# Xem image size breakdown
docker history -H --format "table {{.Size}}\t{{.CreatedBy}}" myapp | sort -k2 -h
```

### Layer Caching & Optimization
**Đọc history để optimize Dockerfile**:
- **Large layers** → Có thể nén (combine RUN commands, clean up trong cùng layer)
- **Many layers** → Mỗi layer có overhead, nhưng cache tốt
- **Layer order**: Put things that change **last** (app code), stable things **first** (base, dependencies)

**Example optimization**:
```dockerfile
# BAD: Separate RUN commands (nhiều layers, cache miss)
RUN apt-get update
RUN apt-get install -y python3
RUN pip install -r requirements.txt

# GOOD: Combine (1 layer, cache tốt hơn)
RUN apt-get update && apt-get install -y python3 && \
    pip install -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Cache-friendly: dependencies trước, code sau
COPY requirements.txt .
RUN pip install -r requirements.txt  # Cached nếu requirements không đổi
COPY . .                            # Thay đổi mỗi lần code thay đổi
```

### Multi-stage Builds
Multi-stage builds tạo **multiple intermediate images**:
```bash
docker history myapp
# Output sẽ show:
# - Stage 1: builder (large, with build tools)
# - Stage 2: runner (small, chỉ runtime)
```

Xem `--target` stage:
```bash
docker history --target builder myapp  # History của builder stage
docker history myapp                  # History của final stage
```

### Troubleshooting
```bash
# Image không có history?
# → Image là external/different format (some registries)
# → Try: docker inspect (layers khác)

# History quá dài?
# → Dockerfile quá nhiều instructions
# → Tối ưu: combine RUN commands

# Layer sizes lớn bất thường?
# → Check CreatedBy: có file nào copy nhầm không?
# → Có thể có leftover files (apt cache, temp files)

# Cannot see full command?
# → Dùng --no-trunc
docker history --no-trunc nginx
```

### Notes
- `docker history` chỉ show **layers** của image (không show container changes)
- Layers là **read-only** và **immutable** (sau khi tạo, không sửa được)
- Layer size là **compressed** size (không phải uncompressed)
- `docker history` **không** xem container differences (dùng `docker diff` thay)
- Image ID (sha256) là hash của **final layer** configuration
- Layers được cache theo **instruction hash** + **file changes**
- `docker history` **không** thể xem layers của **dangling images** nếu không có tag (dùng ID)
- `--platform` để xem multi-platform manifest layers

### Related Commands
- `docker inspect`: Detailed image metadata (including layers)
- `docker images`: List images
- `docker build`: Create image với history
- `docker diff`: Show filesystem changes in container (khác layer history)
- `docker save/load`: Export/import image với layers

### Layer Deep Dive
Mỗi layer là:
- **Immutable**: Không thể sửa sau khi tạo
- **Stackable**: Layers chồng lên nhau (copy-on-write)
- **Cached**: Layers được reuse nếu unchanged
- **Compressed**: Stored compressed, uncompressed khi chạy

**Layer filesystem**: Upperdir (read-write layer) + thư viện read-only layers

