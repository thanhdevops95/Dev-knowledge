# 🔑 Solutions: Golang

> **Solutions for Golang Exercises**
>
> *Lời giải cho bài tập Golang.*

---

## Exercise 1: Hello CLI

```go
// main.go
package main

import (
	"flag"
	"fmt"
)

func main() {
	name := flag.String("name", "World", "Name to greet")
	flag.Parse()
	fmt.Printf("Hello, %s!\n", *name)
}
```

---

## Exercise 2: File Counter

```go
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	dir := "."
	if len(os.Args) > 1 {
		dir = os.Args[1]
	}

	counts := make(map[string]int)

	filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
		if err != nil || info.IsDir() {
			return nil
		}
		ext := filepath.Ext(path)
		if ext == "" {
			ext = "no-ext"
		}
		counts[ext]++
		return nil
	})

	json.NewEncoder(os.Stdout).Encode(counts)
}
```

---

## Exercise 3: Health Check Server

```go
package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
	})
	mux.HandleFunc("/ready", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]string{"status": "ready"})
	})

	server := &http.Server{Addr: ":8080", Handler: mux}

	go func() {
		log.Println("Server starting on :8080")
		server.ListenAndServe()
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	server.Shutdown(ctx)
	log.Println("Server stopped")
}
```

---

> 💡 **Note:** These are reference solutions. Your implementation may differ.
>
> *Lưu ý: Đây là lời giải tham khảo. Cách triển khai của bạn có thể khác.*

---

**[← Back to README](./README.md)**
