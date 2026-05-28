# 🔑 RBAC & ABAC — Authorization Models

> `[INTERMEDIATE → ADVANCED]` — Kiểm soát quyền truy cập trong ứng dụng

---

## Tại sao cần Authorization Model?

**Authentication** = "Bạn là ai?" (login)
**Authorization** = "Bạn được làm gì?" (permissions)

Khi app đơn giản, check `if (user.role === 'admin')` là đủ. Nhưng khi yêu cầu phức tạp:

- "Editor chỉ sửa được bài của mình, không phải bài người khác"
- "Manager department A không xem được data department B"
- "Intern chỉ đọc được docs, không delete"
- "Premium users được upload 10GB, free users chỉ 1GB"

Bạn cần **authorization model** rõ ràng thay vì hàng trăm `if/else`.

---

## 1. RBAC — Role-Based Access Control

### Concept

Gán **roles** cho users, roles chứa **permissions**. User không có permissions trực tiếp — chỉ thông qua roles.

```
Users:           Roles:              Permissions:
┌─────────┐      ┌──────────┐        ┌──────────────────┐
│ An       │─────►│ admin    │───────►│ users:read       │
│ (admin)  │      │          │        │ users:write      │
└─────────┘      └──────────┘        │ users:delete     │
                                      │ posts:read       │
┌─────────┐      ┌──────────┐        │ posts:write      │
│ Bình     │─────►│ editor   │───────►│ posts:read       │
│ (editor) │      │          │        │ posts:write      │
└─────────┘      └──────────┘        └──────────────────┘

┌─────────┐      ┌──────────┐        ┌──────────────────┐
│ Châu     │─────►│ viewer   │───────►│ posts:read       │
│ (viewer) │      │          │        │ users:read       │
└─────────┘      └──────────┘        └──────────────────┘
```

### Implementation

```typescript
// Database schema (Prisma)
model User {
    id    String @id
    name  String
    roles UserRole[]
}

model Role {
    id          String @id
    name        String @unique  // "admin", "editor", "viewer"
    permissions RolePermission[]
    users       UserRole[]
}

model Permission {
    id       String @id
    resource String   // "posts", "users", "settings"
    action   String   // "read", "write", "delete"
    roles    RolePermission[]
    @@unique([resource, action])
}

// Middleware: check permission
function requirePermission(resource: string, action: string) {
    return async (req, res, next) => {
        const user = req.user;

        // Lấy tất cả permissions qua roles
        const userWithRoles = await prisma.user.findUnique({
            where: { id: user.id },
            include: {
                roles: {
                    include: {
                        role: {
                            include: { permissions: { include: { permission: true } } }
                        }
                    }
                }
            }
        });

        const permissions = userWithRoles.roles.flatMap(ur =>
            ur.role.permissions.map(rp => `${rp.permission.resource}:${rp.permission.action}`)
        );

        if (!permissions.includes(`${resource}:${action}`)) {
            return res.status(403).json({ error: 'Forbidden' });
        }

        next();
    };
}

// Usage
app.delete('/api/posts/:id', 
    authenticate,
    requirePermission('posts', 'delete'),
    deletePost
);
```

### Hierarchical RBAC — Kế thừa roles

```
Super Admin → Admin → Editor → Viewer

Viewer:      posts:read
Editor:      posts:read + posts:write        (kế thừa Viewer)
Admin:       + users:manage                  (kế thừa Editor)
Super Admin: + settings:manage + roles:manage (kế thừa Admin)
```

---

## 2. ABAC — Attribute-Based Access Control

### Concept

RBAC không đủ khi cần quy tắc phức tạp. ABAC kiểm tra **attributes** (thuộc tính) của user, resource, và context:

```
Policy: "User có thể edit post NẾU:"
  → user.role = "editor" (user attribute)
  → post.author = user.id (resource attribute) 
  → request.time giữa 9AM-6PM (context attribute)
  → post.status != "published" (resource attribute)
```

### Implementation

```typescript
// Policy engine
interface Policy {
    resource: string;
    action: string;
    condition: (context: PolicyContext) => boolean;
}

interface PolicyContext {
    user: { id: string; role: string; department: string };
    resource: { authorId: string; status: string; department: string };
    environment: { time: Date; ip: string };
}

const policies: Policy[] = [
    {
        resource: 'post',
        action: 'edit',
        condition: (ctx) => {
            // Admin edit mọi post
            if (ctx.user.role === 'admin') return true;
            // Editor chỉ edit post CỦA MÌNH và chưa published
            return ctx.user.role === 'editor'
                && ctx.resource.authorId === ctx.user.id
                && ctx.resource.status !== 'published';
        },
    },
    {
        resource: 'report',
        action: 'read',
        condition: (ctx) => {
            // Manager chỉ xem report CỦA department mình
            return ctx.user.role === 'manager'
                && ctx.resource.department === ctx.user.department;
        },
    },
];

function authorize(resource: string, action: string, context: PolicyContext): boolean {
    const policy = policies.find(p => p.resource === resource && p.action === action);
    if (!policy) return false;  // No policy = deny by default
    return policy.condition(context);
}

// Usage
app.put('/api/posts/:id', authenticate, async (req, res) => {
    const post = await prisma.post.findUnique({ where: { id: req.params.id } });

    const allowed = authorize('post', 'edit', {
        user: req.user,
        resource: { authorId: post.authorId, status: post.status, department: post.department },
        environment: { time: new Date(), ip: req.ip },
    });

    if (!allowed) return res.status(403).json({ error: 'Forbidden' });

    // ... update post
});
```

---

## 3. RBAC vs ABAC — Khi nào dùng gì?

| | RBAC | ABAC |
|---|---|---|
| **Complexity** | Thấp | Cao |
| **Flexibility** | Roles cố định | Policies linh hoạt |
| **Performance** | Nhanh (lookup table) | Chậm hơn (evaluate conditions) |
| **Maintenance** | Dễ (manage roles) | Khó (manage policies) |
| **Best for** | Hầu hết apps | Multi-tenant, complex business rules |
| **Example** | Admin/Editor/Viewer | "Manager department X chỉ xem data department X" |

**Thực tế**: Hầu hết apps bắt đầu với RBAC, sau đó thêm ABAC rules khi cần. Hybrid approach phổ biến nhất.

---

## 4. External Policy Engines

Khi authorization logic quá phức tạp, tách ra **policy engine riêng**:

| Tool | Ngôn ngữ | Use case |
|---|---|---|
| **Casbin** | Go/Node/Python | Library, nhúng vào app |
| **OPA (Open Policy Agent)** | Rego | Kubernetes, microservices |
| **Cerbos** | YAML policies | Self-hosted, REST API |
| **SpiceDB** | Zanzibar-style | Google Zanzibar (relationship-based) |

---

## Bài tập thực hành

- [ ] RBAC: implement Admin/Editor/Viewer roles cho blog API
- [ ] Permission middleware: reusable cho mọi endpoint
- [ ] ABAC: "Editor chỉ edit post của mình, Admin edit mọi post"
- [ ] Audit log: log mọi authorization decisions (ai, gì, khi nào, cho phép/từ chối)

---

## Tài nguyên thêm

- [Casbin](https://casbin.org/) — Authorization library (multi-language)
- [Open Policy Agent](https://www.openpolicyagent.org/) — Cloud-native policy engine
- [NIST ABAC Guide](https://csrc.nist.gov/publications/detail/sp/800-162/final)
