# 🔗 gRPC — Remote Procedure Call hiệu năng cao

> `[INTERMEDIATE → ADVANCED]` — Giao tiếp microservices type-safe, nhanh hơn REST

---

## Tại sao gRPC thay vì REST?

REST dùng JSON qua HTTP/1.1 — đơn giản nhưng có hạn chế khi microservices scale lên:

| | REST/JSON | gRPC/Protobuf |
|---|---|---|
| **Format** | JSON (text, human-readable) | Protobuf (binary, compact) |
| **Size** | ~100 bytes cho cùng data | ~30 bytes (nhỏ 3-10x) |
| **Speed** | Parse JSON chậm | Deserialize binary nhanh 5-10x |
| **Protocol** | HTTP/1.1 (1 request/connection) | HTTP/2 (multiplexed streams) |
| **Contract** | OpenAPI (optional, runtime) | Protobuf schema (bắt buộc, compile-time) |
| **Streaming** | Polling/SSE/WebSocket | Built-in bidirectional streaming |
| **Code gen** | Manual hoặc tools | Auto-generated client/server |

**Khi nào dùng gRPC:**
- Microservices nội bộ (service-to-service) — không cần human-readable
- High throughput: hàng chục nghìn requests/s
- Cần streaming: real-time data, file transfer
- Multi-language: auto-gen client cho Go, Python, Java, TypeScript...

**Khi nào KHÔNG dùng:**
- Public API (browser) — REST dễ dùng hơn cho frontend
- Simple CRUD — over-engineering
- Team nhỏ, ít services

---

## 1. Protocol Buffers — Schema language

Protobuf là ngôn ngữ để **định nghĩa data structure** và **service interface**. Compiler tự generate code cho mọi ngôn ngữ.

```protobuf
// user.proto
syntax = "proto3";

package user.v1;

// Message = data structure (giống interface/struct)
message User {
    string id = 1;          // Field number (NOT value!)
    string name = 2;
    string email = 3;
    UserRole role = 4;
    repeated string tags = 5;   // Array
    optional string bio = 6;    // Có thể null
    google.protobuf.Timestamp created_at = 7;
}

enum UserRole {
    USER_ROLE_UNSPECIFIED = 0;  // Proto3 yêu cầu 0 = default
    USER_ROLE_ADMIN = 1;
    USER_ROLE_EDITOR = 2;
    USER_ROLE_VIEWER = 3;
}

message CreateUserRequest {
    string name = 1;
    string email = 2;
    UserRole role = 3;
}

message CreateUserResponse {
    User user = 1;
}

message GetUserRequest {
    string id = 1;
}

message ListUsersRequest {
    int32 page_size = 1;
    string page_token = 2;     // Cursor-based pagination
}

message ListUsersResponse {
    repeated User users = 1;
    string next_page_token = 2;
}

// Service = API definition
service UserService {
    rpc CreateUser (CreateUserRequest) returns (CreateUserResponse);
    rpc GetUser (GetUserRequest) returns (User);
    rpc ListUsers (ListUsersRequest) returns (ListUsersResponse);
    rpc WatchUsers (WatchUsersRequest) returns (stream User);  // Server streaming!
}
```

**Tại sao field numbers (1, 2, 3...)?** Vì protobuf encode theo number, không theo name. Bạn có thể **rename** field mà không break protocol. Nhưng **KHÔNG BAO GIỜ thay đổi number** của field đã dùng!

---

## 2. Implement Server (Node.js)

```typescript
// Dùng @grpc/grpc-js + @grpc/proto-loader
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';

const packageDefinition = protoLoader.loadSync('user.proto', {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
});
const proto = grpc.loadPackageDefinition(packageDefinition).user.v1;

// Implement service methods
const userService = {
    async CreateUser(call, callback) {
        try {
            const { name, email, role } = call.request;
            const user = await db.users.create({ name, email, role });
            callback(null, { user });
        } catch (err) {
            callback({
                code: grpc.status.INTERNAL,
                message: err.message,
            });
        }
    },

    async GetUser(call, callback) {
        const user = await db.users.findById(call.request.id);
        if (!user) {
            return callback({
                code: grpc.status.NOT_FOUND,
                message: `User ${call.request.id} not found`,
            });
        }
        callback(null, user);
    },

    // Server streaming: gửi nhiều responses cho 1 request
    WatchUsers(call) {
        const subscription = eventBus.subscribe('user:created', (user) => {
            call.write(user);  // Stream từng user về client
        });

        call.on('cancelled', () => {
            subscription.unsubscribe();
        });
    },
};

// Start server
const server = new grpc.Server();
server.addService(proto.UserService.service, userService);
server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
    console.log('gRPC server running on :50051');
});
```

---

## 3. 4 Communication Patterns

gRPC hỗ trợ 4 kiểu communication, mỗi kiểu cho use case khác nhau:

```
1. Unary (1 request → 1 response):
   Client ──request──► Server
   Client ◄──response── Server
   Use case: CRUD operations, simple queries

2. Server Streaming (1 request → N responses):
   Client ──request──► Server
   Client ◄──response 1── Server
   Client ◄──response 2── Server
   Client ◄──response N── Server
   Use case: Live feed, watch changes, download file

3. Client Streaming (N requests → 1 response):
   Client ──request 1──► Server
   Client ──request 2──► Server
   Client ──request N──► Server
   Client ◄──response── Server
   Use case: File upload, batch processing

4. Bidirectional Streaming (N ↔ N):
   Client ←──────────→ Server (cả 2 chiều, bất đồng bộ)
   Use case: Chat, real-time gaming, collaborative editing
```

---

## 4. Error Handling

gRPC dùng **status codes** thay vì HTTP status codes:

```typescript
// gRPC status codes (quan trọng nhất)
grpc.status.OK                // 0  — Success
grpc.status.INVALID_ARGUMENT  // 3  — Bad request (validation fail)
grpc.status.NOT_FOUND         // 5  — Resource not found
grpc.status.ALREADY_EXISTS    // 6  — Duplicate (conflict)
grpc.status.PERMISSION_DENIED // 7  — Forbidden
grpc.status.UNAUTHENTICATED   // 16 — Not authenticated
grpc.status.INTERNAL          // 13 — Internal server error
grpc.status.UNAVAILABLE       // 14 — Service unavailable (retry!)
grpc.status.DEADLINE_EXCEEDED // 4  — Timeout

// Sử dụng
callback({
    code: grpc.status.INVALID_ARGUMENT,
    message: 'Email is required',
    details: 'Field "email" must be a valid email address',
});
```

---

## 5. gRPC-Web — Dùng từ browser

Browser không hỗ trợ HTTP/2 gRPC trực tiếp. Cần proxy (Envoy, grpc-web):

```
Browser ──HTTP/1.1──► Envoy Proxy ──HTTP/2 gRPC──► Backend Service
         (gRPC-Web)                 (native gRPC)
```

Hoặc dùng **Connect** protocol (modern alternative, hoạt động cả trên browser):

```typescript
// Connect-Web (Buf): gRPC cho browser
import { createPromiseClient } from '@connectrpc/connect';
import { createGrpcWebTransport } from '@connectrpc/connect-web';
import { UserService } from './gen/user_connect';

const transport = createGrpcWebTransport({ baseUrl: 'https://api.example.com' });
const client = createPromiseClient(UserService, transport);

const user = await client.getUser({ id: '123' });
console.log(user.name);
```

---

## So sánh: REST vs gRPC vs GraphQL

| | REST | gRPC | GraphQL |
|---|---|---|---|
| **Best for** | Public APIs | Service-to-service | Flexible frontend queries |
| **Format** | JSON | Protobuf | JSON |
| **Contract** | OpenAPI (optional) | Protobuf (required) | Schema (required) |
| **Performance** | Good | Excellent | Good |
| **Streaming** | Limited | Built-in | Subscriptions |
| **Browser** | ✅ Native | ⚠️ Needs proxy | ✅ Native |
| **Learning curve** | Low | Medium | Medium |

---

## Bài tập thực hành

- [ ] Define protobuf schema cho service đơn giản (Users CRUD)
- [ ] Implement gRPC server + client (Node.js hoặc Go)
- [ ] Server streaming: watch for new users
- [ ] Compare: cùng 1 API, implement REST vs gRPC, benchmark throughput

---

## Tài nguyên thêm

- [gRPC Docs](https://grpc.io/docs/) — Official
- [Protocol Buffers Language Guide](https://protobuf.dev/programming-guides/proto3/)
- [Buf (modern protobuf tooling)](https://buf.build/) — Better DX
- [Connect (gRPC for browsers)](https://connectrpc.com/)
