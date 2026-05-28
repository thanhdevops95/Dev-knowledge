# 07. APIs - REST, gRPC, GraphQL

[← Security](06_SECURITY.md) | [Tiếp: Real-time →](08_REALTIME.md)

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **API** | /ˌeɪpiːˈaɪ/ | Application Programming Interface - Giao diện để các phần mềm giao tiếp với nhau |
| **REST** | /rest/ | Representational State Transfer - Kiến trúc API phổ biến nhất |
| **HTTP** | - | HyperText Transfer Protocol - Giao thức truyền tải web |
| **Endpoint** | - | Điểm cuối - URL cụ thể để gọi API |
| **Resource** | - | Tài nguyên - Đối tượng dữ liệu (vd: users, orders) |
| **CRUD** | - | Create, Read, Update, Delete - 4 thao tác cơ bản với dữ liệu |
| **Stateless** | - | Không trạng thái - Mỗi request độc lập, không lưu context |
| **gRPC** | - | Google Remote Procedure Call - Framework RPC hiệu năng cao |
| **Protobuf** | - | Protocol Buffers - Định dạng dữ liệu nhị phân của Google |
| **GraphQL** | - | Ngôn ngữ truy vấn API cho phép client chọn chính xác dữ liệu cần |
| **Query** | - | Truy vấn - Đọc dữ liệu (GET trong REST) |
| **Mutation** | - | Thay đổi - Ghi/xóa dữ liệu (POST/PUT/DELETE trong REST) |
| **Status Code** | - | Mã trạng thái HTTP (200 OK, 404 Not Found, 500 Error) |
| **Idempotent** | /aɪˈdempətənt/ | Bất biến - Gọi nhiều lần cho cùng kết quả |

---

# 🤔 Tại sao DevOps cần biết về APIs?

## Nỗi đau thực tế

> "Backend team dùng gRPC, frontend team dùng REST, không ai hiểu ai"

> "API trả về 500 nhưng không biết debug từ đâu"

> "Sếp hỏi: GraphQL hay REST cho mobile app?"

## Kiến thức này giúp bạn

| Tình huống | Cần biết |
|------------|----------|
| Thiết kế API cho microservices | REST best practices, gRPC |
| Debug API errors | HTTP status codes, curl |
| Tối ưu mobile app | GraphQL (giảm over-fetching) |
| API documentation | OpenAPI/Swagger |
| Service-to-service communication | gRPC vs REST trade-offs |

API là "ngôn ngữ" mà các service dùng để giao tiếp. Hiểu về API giúp bạn thiết kế hệ thống tốt hơn và debug nhanh hơn.

---

# 🌐 API là gì?

**API (Application Programming Interface)** là một hợp đồng giữa hai thành phần phần mềm cho phép chúng giao tiếp với nhau. Trong ngữ cảnh dịch vụ web, API định nghĩa cách client và server trao đổi dữ liệu.

```
┌────────────────────────────────────────────────────────────┐
│                    API COMMUNICATION                        │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Client (Frontend)              Server (Backend)            │
│  ┌───────────────┐             ┌───────────────┐           │
│  │               │   Request   │               │           │
│  │  Mobile App   │────────────►│   API Server  │           │
│  │  Web Browser  │             │   (Business   │           │
│  │  Other Service│◄────────────│    Logic)     │           │
│  │               │  Response   │               │           │
│  └───────────────┘             └───────────────┘           │
│                                                             │
│  API defines:                                               │
│  • What operations are available                            │
│  • What data to send                                        │
│  • What data to expect back                                 │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

# 🌐 REST (Representational State Transfer)

## REST là gì?

**REST** là một **architectural style** cho designing networked applications. REST không phải là protocol hay standard - nó là một set of constraints và principles.

RESTful APIs use **standard HTTP methods** để perform operations trên **resources** (data entities).

### REST Principles

| Principle | Explanation |
|-----------|-------------|
| **Stateless** | Mỗi request chứa tất cả info cần thiết, server không lưu client state |
| **Client-Server** | Separation of concerns, client và server evolve independently |
| **Cacheable** | Responses có thể được cached để improve performance |
| **Uniform Interface** | Consistent, standardized interface |
| **Layered System** | Client không biết talking to server hay intermediary |

### Resource-Based

REST is **resource-centric**. Everything is a resource với unique identifier (URL):

```
Resources:
/users              # Collection of users
/users/123          # Specific user (ID: 123)
/users/123/orders   # Orders belonging to user 123
/users/123/orders/456  # Specific order
```

---

## HTTP Methods (CRUD Operations)

REST uses standard HTTP methods để perform operations:

| Method | CRUD | Idempotent | Safe | Description |
|--------|------|------------|------|-------------|
| **GET** | Read | Yes | Yes | Retrieve resource (không modify) |
| **POST** | Create | No | No | Create new resource |
| **PUT** | Update | Yes | No | Replace entire resource |
| **PATCH** | Update | No | No | Partial update |
| **DELETE** | Delete | Yes | No | Remove resource |

### Idempotent vs Safe

**Idempotent**: Calling same request multiple times = same result

- GET `/users/123` → Same user every time
- DELETE `/users/123` → User deleted (subsequent calls = still deleted)

**Safe**: Request doesn't modify server state

- GET is safe (just reading)
- POST is NOT safe (creates resource)

---

## REST với curl - Chi tiết

### GET - Read Resource

```bash
# Get all users
curl -X GET https://api.example.com/users

# Get specific user
curl -X GET https://api.example.com/users/123

# With query parameters (filter, pagination)
curl -X GET "https://api.example.com/users?status=active&limit=10&page=2"

# With custom headers
curl -X GET https://api.example.com/users \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     -H "Accept: application/json"

# Verbose mode (see headers, TLS handshake)
curl -v https://api.example.com/users
```

**Response example:**

```json
{
  "data": [
    {"id": 1, "name": "John", "email": "john@example.com"},
    {"id": 2, "name": "Jane", "email": "jane@example.com"}
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100
  }
}
```

### POST - Create Resource

```bash
# Create new user
curl -X POST https://api.example.com/users \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "password": "secure123"
     }'

# Upload file
curl -X POST https://api.example.com/upload \
     -F "file=@/path/to/document.pdf"

# Form data
curl -X POST https://api.example.com/login \
     -d "username=john&password=secret"
```

**Response example (201 Created):**

```json
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### PUT - Replace Resource

```bash
# Replace entire user
curl -X PUT https://api.example.com/users/123 \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Updated",
       "email": "john.new@example.com",
       "phone": "+1234567890"
     }'
```

**Note:** PUT replaces the **entire** resource. Fields not included will be removed.

### PATCH - Partial Update

```bash
# Update only specific fields
curl -X PATCH https://api.example.com/users/123 \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Updated"
     }'
```

**Note:** PATCH only updates specified fields, keeps others unchanged.

### DELETE - Remove Resource

```bash
# Delete user
curl -X DELETE https://api.example.com/users/123

# With confirmation
curl -X DELETE https://api.example.com/users/123 \
     -H "Authorization: Bearer token..."
```

**Response:** Usually `204 No Content` or `200 OK`

---

## HTTP Status Codes

### Success (2xx)

| Code | Name | Meaning |
|------|------|---------|
| 200 | OK | Request successful |
| 201 | Created | Resource created (POST) |
| 202 | Accepted | Request accepted, processing async |
| 204 | No Content | Success, no body (DELETE) |

### Client Errors (4xx)

| Code | Name | Meaning |
|------|------|---------|
| 400 | Bad Request | Invalid request syntax |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | HTTP method not supported |
| 409 | Conflict | Resource conflict (duplicate) |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |

### Server Errors (5xx)

| Code | Name | Meaning |
|------|------|---------|
| 500 | Internal Server Error | Server crashed |
| 502 | Bad Gateway | Upstream server error |
| 503 | Service Unavailable | Server overloaded/maintenance |
| 504 | Gateway Timeout | Upstream timeout |

---

## REST Best Practices

### URL Design

```
Good:
GET  /users                 # Get all users
GET  /users/123             # Get user 123
GET  /users/123/orders      # Get user 123's orders
POST /users                 # Create user
PUT  /users/123             # Update user 123

Bad:
GET  /getUsers              # Verb in URL
GET  /user/123              # Singular (should be plural)
POST /users/create          # Verb in URL
GET  /users/123/getOrders   # Verb in URL
```

### Versioning

```
URL versioning:
https://api.example.com/v1/users
https://api.example.com/v2/users

Header versioning:
Accept: application/vnd.example.v1+json
```

### Response Format

```json
{
  "data": {
    "id": 123,
    "name": "John"
  },
  "meta": {
    "page": 1,
    "total": 100
  },
  "errors": null
}
```

---

## REST Pros & Cons

| Pros | Cons |
|------|------|
| ✅ Simple, widely understood | ❌ Over-fetching (get more than needed) |
| ✅ Uses standard HTTP | ❌ Under-fetching (need multiple requests) |
| ✅ Stateless (scalable) | ❌ Multiple round trips |
| ✅ Cacheable | ❌ No real-time support |
| ✅ Human-readable (JSON) | ❌ Rigid structure |

---

# ⚡ gRPC

## gRPC là gì?

**gRPC** (gRPC Remote Procedure Call) là một **high-performance RPC framework** developed by Google.

Key characteristics:

- Uses **Protocol Buffers** for serialization (binary format, smaller than JSON)
- Uses **HTTP/2** for transport (multiplexing, streaming)
- **Strongly typed** contracts via .proto files
- **Multi-language support** (code generation)

```
┌────────────────────────────────────────────────────────────┐
│                     gRPC ARCHITECTURE                       │
├────────────────────────────────────────────────────────────┤
│                                                             │
│                  ┌──────────────────┐                      │
│                  │   .proto file    │ ◄── Define service   │
│                  │  (contract)      │     and messages     │
│                  └────────┬─────────┘                      │
│                           │                                 │
│           ┌───────────────┼───────────────┐                │
│           │               │               │                 │
│           ▼               ▼               ▼                 │
│    ┌───────────┐   ┌───────────┐   ┌───────────┐          │
│    │  Python   │   │   Java    │   │    Go     │          │
│    │  Client   │   │  Server   │   │  Server   │          │
│    │  (stub)   │   │   (impl)  │   │   (impl)  │          │
│    └───────────┘   └───────────┘   └───────────┘          │
│                                                             │
│  All generated from same .proto file                        │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## Protocol Buffers (.proto)

```protobuf
// user.proto
syntax = "proto3";

package user;

service UserService {
  rpc GetUser(GetUserRequest) returns (User);
  rpc CreateUser(CreateUserRequest) returns (User);
  rpc ListUsers(ListUsersRequest) returns (stream User);
}

message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
  repeated string roles = 4;
}

message GetUserRequest {
  int32 id = 1;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
}
```

---

## gRPC Communication Types

### Unary RPC

Standard request-response (like REST):

```
Client ──request──► Server
       ◄──response──
```

### Server Streaming

Server sends multiple responses:

```
Client ──request──► Server
       ◄──response 1──
       ◄──response 2──
       ◄──response 3──
       ◄──...──
```

### Client Streaming

Client sends multiple requests:

```
Client ──request 1──► Server
       ──request 2──►
       ──request 3──►
       ◄──response──
```

### Bidirectional Streaming

Both sides stream:

```
Client ◄══════════► Server
       (full duplex)
```

---

## gRPC vs REST Comparison

| Feature | REST | gRPC |
|---------|------|------|
| **Protocol** | HTTP/1.1 (usually) | HTTP/2 |
| **Data Format** | JSON (text) | Protocol Buffers (binary) |
| **Contract** | Optional (OpenAPI) | Required (.proto) |
| **Code Generation** | Optional | Built-in |
| **Speed** | Slower | 7-10x faster |
| **Payload Size** | Larger | ~30% smaller |
| **Streaming** | Limited | Full support |
| **Browser Support** | ✅ Native | ❌ Needs gRPC-Web |
| **Human Readable** | ✅ Yes | ❌ Binary |
| **Tooling** | Extensive | Growing |

---

## When to use gRPC?

**Use gRPC:**

- Internal **microservices** communication
- **Low latency** requirements
- **Polyglot** environments (many languages)
- **Streaming** data (real-time)
- **Mobile clients** (bandwidth sensitive)

**Use REST:**

- **Public APIs** (browser accessible)
- **Simple CRUD** operations
- **Caching** important
- **Human-readable** responses needed
- Team **unfamiliar** with gRPC

---

# 📊 GraphQL

## GraphQL là gì?

**GraphQL** là một **query language for APIs** developed by Facebook. It allows clients to **request exactly what they need** - nothing more, nothing less.

```
┌────────────────────────────────────────────────────────────┐
│                    GRAPHQL CONCEPT                          │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  Client sends query:              Server returns:           │
│  ┌─────────────────┐              ┌─────────────────┐      │
│  │ query {         │              │ {                │      │
│  │   user(id: 123) │              │   "user": {      │      │
│  │   {             │  ─────────►  │     "name": "Jo" │      │
│  │     name        │              │   }              │      │
│  │   }             │              │ }                │      │
│  │ }               │              │                  │      │
│  └─────────────────┘              └─────────────────┘      │
│                                                             │
│  Client asks for "name" → Gets only "name"                 │
│  (No over-fetching!)                                        │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## GraphQL Operations

### Query (Read)

```graphql
# Simple query
query {
  user(id: "123") {
    name
    email
  }
}

# With variables
query GetUser($userId: ID!) {
  user(id: $userId) {
    name
    email
    posts {
      title
      createdAt
    }
  }
}

# Multiple resources in one request
query {
  user(id: "123") {
    name
  }
  company(id: "456") {
    name
    employees {
      name
    }
  }
}
```

### Mutation (Write)

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}

# Variables:
{
  "input": {
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Subscription (Real-time)

```graphql
subscription OnNewMessage {
  messageAdded(roomId: "123") {
    id
    content
    sender {
      name
    }
  }
}
```

---

## REST vs GraphQL

| Feature | REST | GraphQL |
|---------|------|---------|
| **Endpoints** | Multiple (/users, /posts) | Single (/graphql) |
| **Data fetching** | Fixed structure per endpoint | Client specifies exactly |
| **Over-fetching** | Common | Avoided |
| **Under-fetching** | Multiple requests needed | One request |
| **Versioning** | URL (v1, v2) | Schema evolution |
| **Caching** | ✅ Easy (HTTP caching) | ⚠️ More complex |
| **Learning curve** | Lower | Higher |
| **Tooling** | Mature | Growing |

### Over-fetching Example

```
REST:
GET /users/123
Returns: { id, name, email, phone, address, created, updated, ... }
(But client only needs name!)

GraphQL:
query { user(id: 123) { name } }
Returns: { "user": { "name": "John" } }
(Only what was requested)
```

### Under-fetching Example

```
REST:
GET /users/123        → User data
GET /users/123/posts  → User's posts  
GET /users/123/friends → User's friends
(3 requests!)

GraphQL:
query {
  user(id: 123) {
    name
    posts { title }
    friends { name }
  }
}
(1 request!)
```

---

# 📊 API Comparison Summary

| Aspect | REST | GraphQL | gRPC |
|--------|------|---------|------|
| **Transport** | HTTP | HTTP | HTTP/2 |
| **Data Format** | JSON | JSON | Protobuf |
| **Contract** | Optional | Required (SDL) | Required (.proto) |
| **Flexibility** | Fixed endpoints | Client-driven | Fixed methods |
| **Caching** | ✅ Easy | ⚠️ Complex | ⚠️ Manual |
| **Real-time** | ❌ Polling | ✅ Subscriptions | ✅ Streaming |
| **Browser** | ✅ Native | ✅ Native | ❌ Needs proxy |
| **Best For** | Public APIs, CRUD | Complex data, mobile | Microservices |

---

[← Security](06_SECURITY.md) | [Tiếp: Real-time →](08_REALTIME.md)
