# 💪 Exercises: Docker Advanced

> **Self-practice exercises for Advanced Docker.**
>
> *Bài tập tự luyện Docker nâng cao.*

---

## Exercise 1: Multi-stage Optimization ⭐⭐

Given the following Dockerfile:

*(Có Dockerfile sau:)*

```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
```

**Task**: Rewrite with:

*(Viết lại với:)*

1. Multi-stage build
2. Alpine base
3. Non-root user
4. Health check
5. Target size < 150MB

---

## Exercise 2: BuildKit Advanced ⭐⭐

Create a Dockerfile using:

*(Tạo Dockerfile sử dụng:)*

1. Cache mount for npm *(Cache mount cho npm)*
2. Secret mount for private npm registry *(Secret mount cho private npm registry)*
3. Build args for version *(Build args cho version)*
4. Multiple build targets (dev, test, prod)

---

## Exercise 3: Security Audit ⭐⭐⭐

Given the following image, find and fix security issues:

*(Cho image sau, tìm và fix security issues:)*

```dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y nodejs npm
COPY . /app
WORKDIR /app
ENV API_KEY=supersecret123
RUN npm install
EXPOSE 3000
CMD ["npm", "start"]
```

---

## Exercise 4: Image Size Challenge ⭐⭐⭐

Given this Go application:

*(Có Go application sau:)*

```go
package main
import "fmt"
func main() {
    fmt.Println("Hello DevOps!")
}
```

**Task**: Create a Docker image with size < 10MB

*(Tạo Docker image với size < 10MB)*

---

## Exercise 5: Layer Analysis ⭐⭐

Analyze image layers:

*(Phân tích image layers:)*

1. Use `docker history` *(Sử dụng `docker history`)*
2. Install and use `dive` *(Cài đặt và sử dụng `dive`)*
3. Identify wasted space
4. Optimize and compare *(Optimize và compare)*

---

## Exercise 6: Resource Management ⭐⭐⭐

Write docker-compose.yml with:

*(Viết docker-compose.yml với:)*

1. Memory limits for each service *(Memory limits cho mỗi service)*
2. CPU limits
3. Restart policies
4. Health checks
5. Logging configuration

---

## 📝 Checklist

- [ ] Exercise 1: Multi-stage Optimization
- [ ] Exercise 2: BuildKit Advanced
- [ ] Exercise 3: Security Audit
- [ ] Exercise 4: Image Size Challenge
- [ ] Exercise 5: Layer Analysis
- [ ] Exercise 6: Resource Management

---

**[← Back to README](./README.md)** | **[View Solutions →](./SOLUTIONS.md)**
