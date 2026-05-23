# Go Advanced — Interfaces, Generics, HTTP, Testing

> **Tags:** `go` `interfaces` `generics` `http` `testing` `context` `errors`
> **Level:** Advanced | **Prerequisite:** `go/01-go-basics.md` `go/02-go-concurrency.md`

---

## 1. Interfaces — The Go Way

```go
// Interfaces: implicit implementation (no "implements" keyword)

// Define interface
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Interface composition (embedding)
type ReadWriter interface {
    Reader
    Writer
}

type Closer interface {
    Close() error
}

type ReadWriteCloser interface {
    ReadWriter
    Closer
}

// io.ReadWriter is from standard library — any type that implements
// Read and Write implicitly satisfies it

// Use interfaces for dependency injection
type Logger interface {
    Info(msg string, args ...any)
    Error(msg string, args ...any)
    Debug(msg string, args ...any)
}

type UserService struct {
    repo   UserRepository   // Interface — not concrete type!
    logger Logger           // Interface — swappable in tests
    cache  Cache
}

// Interface for repository (database abstraction)
type UserRepository interface {
    FindByID(ctx context.Context, id int64) (*User, error)
    FindByEmail(ctx context.Context, email string) (*User, error)
    Create(ctx context.Context, user *User) error
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id int64) error
}

// Accepting interfaces, returning concrete types
// Don't return interfaces unless you have to — caller should decide
func NewUserService(repo UserRepository, logger Logger) *UserService {
    return &UserService{repo: repo, logger: logger}
}

// Empty interface (any in Go 1.18+)
func printAnything(v any) {   // any == interface{}
    fmt.Printf("%T: %v\n", v, v)
}

// Type assertion
func handleEvent(event any) {
    switch e := event.(type) {
    case *OrderCreated:
        handleOrderCreated(e)
    case *UserRegistered:
        handleUserRegistered(e)
    default:
        log.Printf("Unknown event: %T", e)
    }
}

// Safe type assertion (no panic)
if user, ok := v.(*User); ok {
    fmt.Println(user.Name)
}
```

---

## 2. Generics (Go 1.18+)

```go
// Generic function
func Map[T, U any](slice []T, f func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = f(v)
    }
    return result
}

func Filter[T any](slice []T, predicate func(T) bool) []T {
    var result []T
    for _, v := range slice {
        if predicate(v) {
            result = append(result, v)
        }
    }
    return result
}

func Reduce[T, U any](slice []T, initial U, f func(U, T) U) U {
    result := initial
    for _, v := range slice {
        result = f(result, v)
    }
    return result
}

// Usage
names := Map(users, func(u User) string { return u.Name })
admins := Filter(users, func(u User) bool { return u.Role == "admin" })
total := Reduce(orders, 0.0, func(sum float64, o Order) float64 { return sum + o.Amount })

// Type constraints
type Number interface {
    ~int | ~int32 | ~int64 | ~float32 | ~float64
}

func Sum[T Number](nums []T) T {
    var total T
    for _, n := range nums {
        total += n
    }
    return total
}

// Generic struct
type Result[T any] struct {
    Value T
    Err   error
}

func (r Result[T]) Unwrap() (T, error) {
    return r.Value, r.Err
}

func (r Result[T]) IsOK() bool {
    return r.Err == nil
}

// Generic cache with type safety
type Cache[K comparable, V any] struct {
    mu    sync.RWMutex
    items map[K]V
}

func NewCache[K comparable, V any]() *Cache[K, V] {
    return &Cache[K, V]{items: make(map[K]V)}
}

func (c *Cache[K, V]) Get(key K) (V, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()
    v, ok := c.items[key]
    return v, ok
}

func (c *Cache[K, V]) Set(key K, value V) {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.items[key] = value
}
```

---

## 3. Error Handling — Best Practices

```go
// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation error: field %s: %s", e.Field, e.Message)
}

// Error wrapping (Go 1.13+)
import "errors"

var (
    ErrNotFound   = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrConflict   = errors.New("conflict")
)

func GetUser(ctx context.Context, id int64) (*User, error) {
    user, err := db.QueryRow(ctx, "SELECT * FROM users WHERE id = $1", id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, fmt.Errorf("user %d: %w", id, ErrNotFound)  // %w = wrap
        }
        return nil, fmt.Errorf("GetUser: %w", err)   // Add context
    }
    return user, nil
}

// Unwrap errors
err := GetUser(ctx, 123)
if errors.Is(err, ErrNotFound) {
    // handle not found
}

var valErr *ValidationError
if errors.As(err, &valErr) {
    // handle validation error, access valErr.Field
}

// Sentinel errors pattern
type AppError struct {
    Code    string
    Message string
    Err     error   // Wrapped underlying error
}

func (e *AppError) Error() string { return e.Message }
func (e *AppError) Unwrap() error { return e.Err }

func NewNotFoundError(entity string, id any) *AppError {
    return &AppError{
        Code:    "NOT_FOUND",
        Message: fmt.Sprintf("%s with id %v not found", entity, id),
        Err:     ErrNotFound,
    }
}

// Error handling in HTTP handlers
func (h *Handler) GetUser(w http.ResponseWriter, r *http.Request) {
    id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
    
    user, err := h.service.GetUser(r.Context(), id)
    if err != nil {
        var appErr *AppError
        if errors.As(err, &appErr) {
            switch appErr.Code {
            case "NOT_FOUND":
                http.Error(w, appErr.Message, http.StatusNotFound)
            case "UNAUTHORIZED":
                http.Error(w, appErr.Message, http.StatusUnauthorized)
            default:
                http.Error(w, "Internal server error", http.StatusInternalServerError)
            }
            return
        }
        h.logger.Error("unexpected error", "err", err)
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }
    
    json.NewEncoder(w).Encode(user)
}
```

---

## 4. HTTP Server with net/http + Chi

```go
package main

import (
    "encoding/json"
    "net/http"
    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
)

type Server struct {
    router  *chi.Mux
    service UserService
    logger  *slog.Logger
}

func NewServer(service UserService, logger *slog.Logger) *Server {
    s := &Server{
        router:  chi.NewRouter(),
        service: service,
        logger:  logger,
    }
    s.setupRoutes()
    return s
}

func (s *Server) setupRoutes() {
    r := s.router
    
    // Global middleware
    r.Use(middleware.RequestID)      // Add X-Request-ID header
    r.Use(middleware.RealIP)         // Get real IP behind proxy
    r.Use(middleware.Logger)         // Request logging
    r.Use(middleware.Recoverer)      // Recover from panics
    r.Use(middleware.Timeout(60 * time.Second))
    r.Use(corsMiddleware)
    
    // Routes
    r.Get("/health", s.healthCheck)
    
    r.Route("/api/v1", func(r chi.Router) {
        r.Use(s.authMiddleware)       // Group-level middleware
        
        r.Route("/users", func(r chi.Router) {
            r.Get("/", s.listUsers)
            r.Post("/", s.createUser)
            r.Route("/{id}", func(r chi.Router) {
                r.Use(s.userCtx)      // Load user into context
                r.Get("/", s.getUser)
                r.Put("/", s.updateUser)
                r.Delete("/", s.deleteUser)
            })
        })
    })
}

func (s *Server) listUsers(w http.ResponseWriter, r *http.Request) {
    // Parse query params
    page, _ := strconv.Atoi(r.URL.Query().Get("page"))
    if page < 1 { page = 1 }
    
    users, err := s.service.ListUsers(r.Context(), page, 20)
    if err != nil {
        s.respondError(w, r, err)
        return
    }
    
    s.respondJSON(w, http.StatusOK, map[string]any{
        "users": users,
        "page":  page,
    })
}

func (s *Server) createUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        s.respondError(w, r, &AppError{Code: "BAD_REQUEST", Message: "invalid JSON"})
        return
    }
    
    if err := req.Validate(); err != nil {
        s.respondError(w, r, err)
        return
    }
    
    user, err := s.service.CreateUser(r.Context(), req)
    if err != nil {
        s.respondError(w, r, err)
        return
    }
    
    s.respondJSON(w, http.StatusCreated, user)
}

// Helper methods
func (s *Server) respondJSON(w http.ResponseWriter, status int, v any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    if err := json.NewEncoder(w).Encode(v); err != nil {
        s.logger.Error("failed to encode response", "err", err)
    }
}

func (s *Server) respondError(w http.ResponseWriter, r *http.Request, err error) {
    var appErr *AppError
    if errors.As(err, &appErr) {
        s.respondJSON(w, appErr.HTTPStatus(), map[string]string{
            "error": appErr.Message,
            "code":  appErr.Code,
        })
        return
    }
    
    s.logger.Error("unexpected error", "err", err, "path", r.URL.Path)
    s.respondJSON(w, http.StatusInternalServerError, map[string]string{
        "error": "internal server error",
    })
}

// Graceful shutdown
func main() {
    server := &http.Server{
        Addr:         ":8080",
        Handler:      s.router,
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }
    
    go func() {
        if err := server.ListenAndServe(); err != http.ErrServerClosed {
            log.Fatal(err)
        }
    }()
    
    // Wait for interrupt signal
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, os.Interrupt, syscall.SIGTERM)
    <-quit
    
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    
    if err := server.Shutdown(ctx); err != nil {
        log.Fatal("Server forced to shutdown:", err)
    }
    
    log.Println("Server exited gracefully")
}
```

---

## 5. Testing

```go
package service_test

import (
    "context"
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
    "github.com/stretchr/testify/mock"
)

// Mock repository
type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) FindByID(ctx context.Context, id int64) (*User, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func (m *MockUserRepository) Create(ctx context.Context, user *User) error {
    return m.Called(ctx, user).Error(0)
}

// Test with mocks
func TestGetUser(t *testing.T) {
    t.Run("returns user when found", func(t *testing.T) {
        mockRepo := new(MockUserRepository)
        svc := NewUserService(mockRepo, newTestLogger())
        
        expected := &User{ID: 1, Name: "Alice", Email: "alice@example.com"}
        mockRepo.On("FindByID", mock.Anything, int64(1)).Return(expected, nil)
        
        user, err := svc.GetUser(context.Background(), 1)
        
        require.NoError(t, err)
        assert.Equal(t, expected, user)
        mockRepo.AssertExpectations(t)
    })
    
    t.Run("returns not found error when user does not exist", func(t *testing.T) {
        mockRepo := new(MockUserRepository)
        svc := NewUserService(mockRepo, newTestLogger())
        
        mockRepo.On("FindByID", mock.Anything, int64(999)).Return(nil, ErrNotFound)
        
        _, err := svc.GetUser(context.Background(), 999)
        
        require.Error(t, err)
        assert.True(t, errors.Is(err, ErrNotFound))
    })
}

// Table-driven tests (idiomatic Go)
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "alice@example.com", false},
        {"valid email with subdomain", "alice@mail.example.com", false},
        {"empty email", "", true},
        {"missing @", "aliceexample.com", true},
        {"missing domain", "alice@", true},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := validateEmail(tt.email)
            if tt.wantErr {
                assert.Error(t, err)
            } else {
                assert.NoError(t, err)
            }
        })
    }
}

// HTTP handler tests
func TestGetUserHandler(t *testing.T) {
    mockRepo := new(MockUserRepository)
    server := NewServer(NewUserService(mockRepo, newTestLogger()), newTestLogger())
    
    user := &User{ID: 1, Name: "Alice"}
    mockRepo.On("FindByID", mock.Anything, int64(1)).Return(user, nil)
    
    req := httptest.NewRequest(http.MethodGet, "/api/v1/users/1", nil)
    w := httptest.NewRecorder()
    
    server.router.ServeHTTP(w, req)
    
    assert.Equal(t, http.StatusOK, w.Code)
    
    var response User
    err := json.NewDecoder(w.Body).Decode(&response)
    require.NoError(t, err)
    assert.Equal(t, user.Name, response.Name)
}

// Integration tests with real DB
func TestIntegration(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping integration test in short mode")
    }
    
    db := setupTestDB(t)   // Create real test DB
    t.Cleanup(func() { teardownTestDB(t, db) })
    
    repo := NewPostgresUserRepository(db)
    svc := NewUserService(repo, newTestLogger())
    
    // Test with real database
    user, err := svc.CreateUser(context.Background(), CreateUserRequest{
        Email: "test@example.com",
        Name:  "Test User",
    })
    require.NoError(t, err)
    
    found, err := svc.GetUser(context.Background(), user.ID)
    require.NoError(t, err)
    assert.Equal(t, user.Email, found.Email)
}

// Benchmarks
func BenchmarkGetUser(b *testing.B) {
    // Setup once
    svc := setupBenchmarkService(b)
    ctx := context.Background()
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, _ = svc.GetUser(ctx, int64(i%1000+1))
    }
}
```

---

## 6. Context — Cancellation & Values

```go
// Context propagation
func processRequest(ctx context.Context, userID int64) error {
    // Create derived context with timeout
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()   // Always cancel to prevent leak!
    
    // Check if already cancelled
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
    }
    
    // Pass context to all downstream calls
    user, err := db.GetUser(ctx, userID)  // DB respects cancellation
    if err != nil {
        return fmt.Errorf("get user: %w", err)
    }
    
    // Concurrent operations with context
    g, gctx := errgroup.WithContext(ctx)
    
    var orders []Order
    g.Go(func() error {
        var err error
        orders, err = orderService.GetOrders(gctx, userID)
        return err
    })
    
    var profile Profile
    g.Go(func() error {
        var err error
        profile, err = profileService.GetProfile(gctx, userID)
        return err
    })
    
    if err := g.Wait(); err != nil {
        return err  // One failed, both cancelled
    }
    
    return nil
}

// Context values — request-scoped data (use sparingly)
type contextKey string
const (
    userIDKey    contextKey = "userID"
    requestIDKey contextKey = "requestID"
)

func withUserID(ctx context.Context, userID int64) context.Context {
    return context.WithValue(ctx, userIDKey, userID)
}

func userIDFromContext(ctx context.Context) (int64, bool) {
    id, ok := ctx.Value(userIDKey).(int64)
    return id, ok
}

// Middleware pattern
func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        user, err := validateToken(token)
        if err != nil {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        
        ctx := withUserID(r.Context(), user.ID)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

---

## 7. Struct Embedding & Composition

```go
// Embedding (NOT inheritance — composition)
type Base struct {
    ID        int64
    CreatedAt time.Time
    UpdatedAt time.Time
}

type User struct {
    Base          // Embed Base (promotes Base's methods + fields)
    Email    string
    Name     string
}

// User.ID, User.CreatedAt available directly
user := User{
    Base:  Base{ID: 1, CreatedAt: time.Now()},
    Email: "alice@example.com",
}
fmt.Println(user.ID)          // 1 (promoted from Base)
fmt.Println(user.CreatedAt)   // (promoted from Base)

// Embed interfaces
type AuditLogger interface {
    Log(action string, userID int64)
}

type Service struct {
    AuditLogger    // Embed interface — allows swapping implementation
    db UserRepository
}

// Method overriding via promotion
type CachedRepo struct {
    UserRepository         // Embed the interface
    cache *redis.Client
}

func (c *CachedRepo) FindByID(ctx context.Context, id int64) (*User, error) {
    // Check cache first
    if user, err := c.getFromCache(ctx, id); err == nil {
        return user, nil
    }
    // Fallback to embedded UserRepository
    user, err := c.UserRepository.FindByID(ctx, id)
    if err != nil {
        return nil, err
    }
    c.setCache(ctx, id, user)
    return user, nil
}
```

---

## 8. slog — Structured Logging (Go 1.21+)

```go
import "log/slog"

// Setup
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
    AddSource: true,    // Include file:line
}))
slog.SetDefault(logger)

// Usage
slog.Info("user created",
    "user_id", user.ID,
    "email", user.Email,
    "duration_ms", time.Since(start).Milliseconds(),
)

slog.Error("database error",
    "err", err,
    "query", query,
    "table", "users",
)

// Group/context attributes
userLogger := slog.With(
    "service", "user-service",
    "user_id", userID,
)
userLogger.Info("processing request")   // Includes service + user_id

// Structured logging in middleware
func loggingMiddleware(logger *slog.Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            ww := middleware.NewWrapResponseWriter(w, r.ProtoMajor)
            
            next.ServeHTTP(ww, r)
            
            logger.Info("request completed",
                "method", r.Method,
                "path", r.URL.Path,
                "status", ww.Status(),
                "bytes", ww.BytesWritten(),
                "duration_ms", time.Since(start).Milliseconds(),
                "request_id", middleware.GetReqID(r.Context()),
            )
        })
    }
}
```

---

*Tài liệu liên quan: `go/01-go-basics.md` | `go/02-go-concurrency.md` | `api-design/01-rest-api.md`*
