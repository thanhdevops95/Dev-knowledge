# 📡 GraphQL — Query Language cho APIs

> `[INTERMEDIATE]` — Thay thế REST khi cần flexibility

---

## Tại sao GraphQL?

```
REST Problem:
GET /api/users/1           → { id, name, email, bio, avatar, ... }
GET /api/users/1/posts     → [{ id, title, content, ... }]
GET /api/users/1/followers → [{ id, name, ... }]
→ 3 requests! Và over-fetching (lấy thừa data)

GraphQL Solution:
POST /graphql
{
    user(id: 1) {
        name
        email
        posts(limit: 5) {
            title
        }
        followersCount
    }
}
→ 1 request! Chỉ lấy đúng data cần!
```

---

## 1. Schema Definition

```graphql
# Type definitions
type User {
    id: ID!
    name: String!
    email: String!
    avatar: String
    role: Role!
    posts(limit: Int = 10, offset: Int = 0): [Post!]!
    postsCount: Int!
    createdAt: DateTime!
}

type Post {
    id: ID!
    title: String!
    content: String!
    published: Boolean!
    author: User!
    tags: [Tag!]!
    createdAt: DateTime!
}

type Tag {
    id: ID!
    name: String!
    posts: [Post!]!
}

enum Role {
    USER
    ADMIN
    MODERATOR
}

# Input type cho mutations
input CreatePostInput {
    title: String!
    content: String!
    tags: [String!]
    published: Boolean = false
}

# Queries & Mutations
type Query {
    user(id: ID!): User
    users(page: Int = 1, limit: Int = 20): UserConnection!
    post(id: ID!): Post
    posts(filter: PostFilter): [Post!]!
    me: User
}

type Mutation {
    createPost(input: CreatePostInput!): Post!
    updatePost(id: ID!, input: UpdatePostInput!): Post!
    deletePost(id: ID!): Boolean!
    login(email: String!, password: String!): AuthPayload!
}

type Subscription {
    postCreated: Post!
    messageReceived(chatId: ID!): Message!
}

# Pagination
type UserConnection {
    edges: [UserEdge!]!
    pageInfo: PageInfo!
    totalCount: Int!
}

type UserEdge {
    node: User!
    cursor: String!
}

type PageInfo {
    hasNextPage: Boolean!
    endCursor: String
}
```

---

## 2. Resolvers — Logic xử lý

```javascript
// Apollo Server
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';

const resolvers = {
    Query: {
        user: async (_, { id }, context) => {
            return context.db.users.findById(id);
        },

        users: async (_, { page, limit }, context) => {
            const offset = (page - 1) * limit;
            const [users, total] = await Promise.all([
                context.db.users.findMany({ skip: offset, take: limit }),
                context.db.users.count(),
            ]);
            return {
                edges: users.map(u => ({ node: u, cursor: encodeCursor(u.id) })),
                pageInfo: {
                    hasNextPage: offset + limit < total,
                    endCursor: encodeCursor(users[users.length - 1]?.id),
                },
                totalCount: total,
            };
        },

        me: async (_, __, context) => {
            if (!context.user) throw new AuthenticationError('Not logged in');
            return context.db.users.findById(context.user.id);
        },
    },

    Mutation: {
        createPost: async (_, { input }, context) => {
            if (!context.user) throw new AuthenticationError('Not logged in');
            return context.db.posts.create({
                data: { ...input, authorId: context.user.id },
            });
        },

        deletePost: async (_, { id }, context) => {
            const post = await context.db.posts.findById(id);
            if (post.authorId !== context.user.id) {
                throw new ForbiddenError('Not your post');
            }
            await context.db.posts.delete(id);
            return true;
        },
    },

    // Field resolvers
    User: {
        posts: async (parent, { limit, offset }, context) => {
            return context.db.posts.findMany({
                where: { authorId: parent.id },
                take: limit,
                skip: offset,
            });
        },
        postsCount: async (parent, _, context) => {
            return context.db.posts.count({ where: { authorId: parent.id } });
        },
    },

    Post: {
        author: async (parent, _, context) => {
            return context.loaders.userLoader.load(parent.authorId);  // DataLoader!
        },
    },
};

// Server setup
const server = new ApolloServer({ typeDefs, resolvers });
await server.start();

app.use('/graphql', expressMiddleware(server, {
    context: async ({ req }) => ({
        user: await authenticateToken(req.headers.authorization),
        db: prisma,
        loaders: createLoaders(),
    }),
}));
```

---

## 3. Client — React + Apollo

```jsx
import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery, useMutation } from '@apollo/client';

const client = new ApolloClient({
    uri: 'http://localhost:4000/graphql',
    cache: new InMemoryCache(),
    headers: {
        authorization: `Bearer ${token}`,
    },
});

// Query
const GET_USERS = gql`
    query GetUsers($page: Int!, $limit: Int!) {
        users(page: $page, limit: $limit) {
            edges {
                node { id, name, email, avatar }
            }
            pageInfo { hasNextPage, endCursor }
            totalCount
        }
    }
`;

function UserList() {
    const { data, loading, error, fetchMore } = useQuery(GET_USERS, {
        variables: { page: 1, limit: 20 },
    });

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    return (
        <div>
            {data.users.edges.map(({ node }) => (
                <div key={node.id}>{node.name} — {node.email}</div>
            ))}
            {data.users.pageInfo.hasNextPage && (
                <button onClick={() => fetchMore({
                    variables: { page: 2 },
                })}>
                    Load More
                </button>
            )}
        </div>
    );
}

// Mutation
const CREATE_POST = gql`
    mutation CreatePost($input: CreatePostInput!) {
        createPost(input: $input) { id, title }
    }
`;

function CreatePostForm() {
    const [createPost, { loading }] = useMutation(CREATE_POST, {
        refetchQueries: ['GetPosts'],
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        createPost({
            variables: { input: { title, content, published: true } },
        });
    };

    return <form onSubmit={handleSubmit}>...</form>;
}
```

---

## 4. N+1 Problem — DataLoader

```javascript
import DataLoader from 'dataloader';

function createLoaders() {
    return {
        userLoader: new DataLoader(async (userIds) => {
            const users = await prisma.user.findMany({
                where: { id: { in: [...userIds] } },
            });
            const userMap = new Map(users.map(u => [u.id, u]));
            return userIds.map(id => userMap.get(id));
        }),
    };
}

// Không DataLoader: 100 posts → 100 queries cho author
// Với DataLoader:   100 posts → 1 batch query (WHERE id IN (...))
```

---

## 5. REST vs GraphQL

| | REST | GraphQL |
|---|---|---|
| **Endpoints** | Nhiều (/users, /posts) | 1 (/graphql) |
| **Data** | Server quyết định | Client quyết định |
| **Over-fetching** | ❌ Thường xảy ra | ✅ Lấy đúng cần |
| **Under-fetching** | ❌ Nhiều requests | ✅ 1 request |
| **Caching** | ✅ HTTP cache dễ | ❌ Phức tạp hơn |
| **Learning** | Dễ | Trung bình |
| **Tooling** | Mature | Tốt (Apollo, Relay) |
| **Khi nào** | CRUD đơn giản, mobile | Data phức tạp, nhiều relations |

---

## Các lỗi thường gặp

```
❌ Sai: Cho phép query nested vô hạn → DoS
   { user { posts { author { posts { author { ... } } } } } }
✅ Đúng: Giới hạn depth (graphql-depth-limit)

❌ Sai: Không dùng DataLoader → N+1 queries
✅ Đúng: DataLoader cho EVERY relation resolver

❌ Sai: GraphQL cho CRUD đơn giản (overkill)
✅ Đúng: REST nếu CRUD đơn giản, GraphQL nếu data phức tạp
```

---

## Bài tập thực hành

- [ ] Setup Apollo Server: schema Users + Posts
- [ ] Implement resolvers: Query, Mutation, Field resolvers
- [ ] Client: React + Apollo — query users, create post
- [ ] DataLoader: fix N+1 cho post.author

---

## Tài nguyên thêm

- [GraphQL Docs](https://graphql.org/learn/) — Official
- [Apollo Docs](https://www.apollographql.com/docs/) — Full-stack platform
- [How to GraphQL](https://www.howtographql.com/) — Free tutorial
