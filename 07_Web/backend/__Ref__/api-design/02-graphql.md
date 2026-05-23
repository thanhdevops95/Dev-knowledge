# GraphQL

> **Tags:** `graphql` `api` `schema` `resolvers` `apollo` `n+1` `dataloader`
> **Level:** Intermediate | **Prerequisite:** `api-design/01-rest-api.md`

---

## 1. GraphQL vs REST

| | REST | GraphQL |
|---|---|---|
| Data fetching | Fixed endpoints, fixed responses | Client specifies exact fields |
| Over-fetching | Common (get unused fields) | Eliminated |
| Under-fetching | Common (need multiple requests) | Eliminated — join at graph level |
| Versioning | /v1, /v2, header versioning | Deprecate fields, no versioning needed |
| Type system | Optional (OpenAPI) | **Built-in and mandatory** |
| Caching | HTTP caching (GET, ETags) | Harder (POST by default), need custom |
| N+1 problem | Not inherent | Easy to create accidentally |
| Learning curve | Low | Higher |

---

## 2. Schema Definition Language (SDL)

```graphql
# Scalar types: String, Int, Float, Boolean, ID
# ! = non-nullable (required)

type User {
  id: ID!
  name: String!
  email: String!
  age: Int                    # Nullable
  role: UserRole!
  posts: [Post!]!             # Non-null list, non-null items
  friends: [User]             # Nullable list, nullable items
  createdAt: DateTime!        # Custom scalar
  address: Address            # Nested type
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!               # Relationship
  tags: [String!]!
  publishedAt: DateTime
}

type Address {
  street: String!
  city: String!
  country: String!
}

enum UserRole {
  ADMIN
  USER
  GUEST
}

# Custom scalars
scalar DateTime
scalar JSON
scalar Upload   # File upload

# Interface
interface Node {
  id: ID!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Product implements Node & Timestamped {
  id: ID!
  name: String!
  price: Float!
  createdAt: DateTime!
  updatedAt: DateTime!
}

# Union types
union SearchResult = User | Post | Product

# Input types (for mutations)
input CreateUserInput {
  name: String!
  email: String!
  password: String!
  role: UserRole = USER   # Default value
}

input UpdateUserInput {
  name: String
  email: String
  age: Int
}

# Entry points
type Query {
  user(id: ID!): User
  users(limit: Int = 10, offset: Int = 0, role: UserRole): [User!]!
  search(query: String!): [SearchResult!]!
  me: User                # Returns authenticated user
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
  login(email: String!, password: String!): AuthPayload!
}

type AuthPayload {
  token: String!
  user: User!
}

type Subscription {
  userCreated: User!
  messageAdded(roomId: ID!): Message!
}
```

---

## 3. Queries & Mutations (Client Side)

```graphql
# Basic query
query {
  users {
    id
    name
    email
  }
}

# Query with variables (preferred — prevents injection)
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
    role
    posts {
      id
      title
    }
  }
}
# Variables: { "id": "123" }

# Aliases — get same field multiple times
query {
  admin: user(id: "1") {
    name
    email
  }
  member: user(id: "2") {
    name
    email
  }
}

# Fragments — reusable field selections
fragment UserFields on User {
  id
  name
  email
  role
}

query {
  users {
    ...UserFields
    posts {
      id
      title
    }
  }
}

# Inline fragments (for unions/interfaces)
query {
  search(query: "alice") {
    ... on User {
      name
      email
    }
    ... on Post {
      title
      content
    }
  }
}

# Mutations
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}
# Variables: { "input": { "name": "Alice", "email": "alice@example.com", "password": "..." } }

# Directives
query GetUser($id: ID!, $withPosts: Boolean!) {
  user(id: $id) {
    name
    posts @include(if: $withPosts) {  # Conditional field
      title
    }
    secret @skip(if: true)           # Always excluded
  }
}
```

---

## 4. Resolvers (Server Side — Apollo Server với Node.js)

```typescript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';

const typeDefs = `#graphql
  type User {
    id: ID!
    name: String!
    posts: [Post!]!
  }
  type Post {
    id: ID!
    title: String!
    author: User!
  }
  type Query {
    user(id: ID!): User
    users: [User!]!
  }
`;

const resolvers = {
  Query: {
    // Root resolver — receives (parent, args, context, info)
    user: async (_, { id }, { db }) => {
      return db.users.findById(id);
    },
    users: async (_, __, { db, user }) => {
      // Check auth via context
      if (!user) throw new Error("Unauthorized");
      return db.users.findAll();
    },
  },

  // Field resolvers — called for each User
  User: {
    posts: async (parent, _, { db }) => {
      // parent = the User object
      return db.posts.findByAuthorId(parent.id);
    },
  },

  Post: {
    author: async (parent, _, { db }) => {
      return db.users.findById(parent.authorId);
    },
  },
};

const server = new ApolloServer({ typeDefs, resolvers });

const { url } = await startStandaloneServer(server, {
  context: async ({ req }) => {
    // Build context for every request
    const token = req.headers.authorization?.replace('Bearer ', '');
    const user = token ? await verifyToken(token) : null;
    return { db, user };
  },
});
```

---

## 5. N+1 Problem & DataLoader

**N+1 problem**: query 1 list → for each item, query related → N+1 DB calls total.

```typescript
// Problem: 1 query for users + N queries for posts (N = number of users)
User: {
  posts: async (parent, _, { db }) => {
    // Called N times if N users returned by parent resolver!
    return db.posts.findByAuthorId(parent.id);
    // SELECT * FROM posts WHERE author_id = 1;
    // SELECT * FROM posts WHERE author_id = 2;
    // ... N more queries
  }
}

// Solution: DataLoader — batches and caches
import DataLoader from 'dataloader';

// Batch function: receives ARRAY of keys, returns ARRAY of values
const userLoader = new DataLoader(async (userIds: readonly number[]) => {
  // ONE query for ALL users!
  const users = await db.users.findByIds([...userIds]);
  // Return in SAME ORDER as input ids
  return userIds.map(id => users.find(u => u.id === id) || null);
});

// In context (per-request — fresh cache per request!)
context: async () => ({
  db,
  loaders: {
    user: new DataLoader(batchUsers),
    post: new DataLoader(batchPosts),
  }
}),

// In resolver
Post: {
  author: async (parent, _, { loaders }) => {
    // Batched! All author lookups in one request get batched into 1 DB call
    return loaders.user.load(parent.authorId);
  }
}
```

---

## 6. Authentication & Authorization

```typescript
// Authentication in context
const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [ApolloServerPluginLandingPageLocalDefault()],
});

context: async ({ req }) => {
  const token = req.headers.authorization?.split(' ')[1];
  let currentUser = null;
  
  if (token) {
    try {
      currentUser = jwt.verify(token, process.env.JWT_SECRET) as User;
    } catch {
      throw new GraphQLError('Invalid token', {
        extensions: { code: 'UNAUTHENTICATED' }
      });
    }
  }
  
  return { currentUser, db };
},

// Authorization in resolver
Query: {
  adminData: (_, __, { currentUser }) => {
    if (!currentUser) {
      throw new GraphQLError('Must be logged in', {
        extensions: { code: 'UNAUTHENTICATED' }
      });
    }
    if (currentUser.role !== 'ADMIN') {
      throw new GraphQLError('Must be admin', {
        extensions: { code: 'FORBIDDEN' }
      });
    }
    return getAdminData();
  }
}

// Field-level authorization with directives
const typeDefs = `#graphql
  directive @auth(roles: [UserRole!]!) on FIELD_DEFINITION

  type Query {
    adminDashboard: Dashboard @auth(roles: [ADMIN])
    publicData: [Item!]!
  }
`;
```

---

## 7. Subscriptions

```typescript
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();

const schema = makeExecutableSchema({
  typeDefs: `#graphql
    type Subscription {
      messageAdded(roomId: ID!): Message!
      userOnline: User!
    }
  `,
  resolvers: {
    Subscription: {
      messageAdded: {
        subscribe: (_, { roomId }) =>
          pubsub.asyncIterator(`MESSAGE_ADDED_${roomId}`),
        resolve: (payload) => payload.messageAdded,
      },
    },
    
    Mutation: {
      sendMessage: async (_, { roomId, content }, { currentUser }) => {
        const message = await db.messages.create({ roomId, content, userId: currentUser.id });
        
        // Publish to subscribers
        pubsub.publish(`MESSAGE_ADDED_${roomId}`, { messageAdded: message });
        
        return message;
      }
    }
  }
});

// Setup WebSocket server
const httpServer = createServer(app);
const wsServer = new WebSocketServer({ server: httpServer, path: '/graphql' });
useServer({ schema }, wsServer);
```

---

## 8. Apollo Client (React)

```typescript
// Setup
import { ApolloClient, InMemoryCache, ApolloProvider, gql } from '@apollo/client';

const client = new ApolloClient({
  uri: 'https://api.example.com/graphql',
  cache: new InMemoryCache(),
  headers: {
    authorization: `Bearer ${localStorage.getItem('token')}`,
  },
});

// Wrap app
<ApolloProvider client={client}>
  <App />
</ApolloProvider>

// useQuery
const GET_USERS = gql`
  query GetUsers($limit: Int!) {
    users(limit: $limit) {
      id
      name
      email
    }
  }
`;

function UserList() {
  const { loading, error, data, refetch } = useQuery(GET_USERS, {
    variables: { limit: 10 },
    pollInterval: 5000,           // Refetch every 5s
    fetchPolicy: 'cache-first',   // cache-first | network-only | no-cache
  });

  if (loading) return <Loading />;
  if (error) return <Error message={error.message} />;

  return (
    <ul>
      {data.users.map(user => <UserItem key={user.id} user={user} />)}
    </ul>
  );
}

// useMutation
const CREATE_USER = gql`
  mutation CreateUser($input: CreateUserInput!) {
    createUser(input: $input) {
      id
      name
    }
  }
`;

function CreateUserForm() {
  const [createUser, { loading, error }] = useMutation(CREATE_USER, {
    // Update cache after mutation
    update(cache, { data: { createUser } }) {
      cache.modify({
        fields: {
          users(existingUsers = []) {
            const newUserRef = cache.writeFragment({
              data: createUser,
              fragment: gql`fragment NewUser on User { id name }`
            });
            return [...existingUsers, newUserRef];
          }
        }
      });
    },
    onError: (error) => console.error(error),
  });

  const handleSubmit = async (formData) => {
    await createUser({ variables: { input: formData } });
  };
}
```

---

## 9. Federation — Microservices GraphQL

Apollo Federation = combine multiple GraphQL services into one unified graph:

```typescript
// User service (subgraph)
const typeDefs = `#graphql
  type User @key(fields: "id") {
    id: ID!
    name: String!
    email: String!
  }

  type Query {
    user(id: ID!): User
    users: [User!]!
  }
`;

// Order service (references User from User subgraph)
const typeDefs = `#graphql
  extend type User @key(fields: "id") {
    id: ID! @external
    orders: [Order!]!
  }

  type Order {
    id: ID!
    total: Float!
    user: User!
  }

  type Query {
    order(id: ID!): Order
  }
`;

// Router combines all subgraphs — clients query /graphql
// Router distributes query parts to appropriate subgraphs
```

---

## 10. Performance & Best Practices

```typescript
// 1. Complexity limiting — prevent expensive queries
import { createComplexityRule } from 'graphql-query-complexity';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    createComplexityRule({
      maximumComplexity: 1000,   // Max complexity per query
      variables: {},
      onComplete: (complexity) => {
        console.log('Query Complexity:', complexity);
      },
    }),
  ],
});

// 2. Persisted queries — send query ID instead of full query
// Client: store query hash, server: look up query by hash

// 3. Depth limiting
import depthLimit from 'graphql-depth-limit';
validationRules: [depthLimit(5)]  // Max 5 levels deep

// 4. Field suggestions — disable in production (security)
// Don't expose available fields to potential attackers

// 5. Query batching — multiple operations in one HTTP request
// Apollo Client does this automatically with BatchHttpLink
```

---

## 11. Error Handling

```typescript
import { GraphQLError } from 'graphql';

// Structured errors with extensions
throw new GraphQLError('User not found', {
  extensions: {
    code: 'USER_NOT_FOUND',    // Machine-readable code
    id: userId,                // Additional context
    http: { status: 404 },     // HTTP status (Apollo-specific)
  },
});

// Error codes conventions:
// UNAUTHENTICATED  — 401
// FORBIDDEN        — 403  
// NOT_FOUND        — 404
// BAD_USER_INPUT   — 400
// INTERNAL_SERVER_ERROR — 500

// formatError — sanitize errors in production
const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError: (formattedError, error) => {
    // Don't expose internal errors
    if (process.env.NODE_ENV === 'production' && 
        !formattedError.extensions?.code) {
      return { message: 'Internal server error' };
    }
    return formattedError;
  },
});
```

---

*Tài liệu liên quan: `api-design/01-rest-api.md` | `api-design/03-grpc.md` | `state-management/03-react-query-tanstack.md`*
