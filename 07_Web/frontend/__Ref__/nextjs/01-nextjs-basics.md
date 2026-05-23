# ⚡ Next.js — Full-stack React Framework

> `[INTERMEDIATE]` — From React SPA đến full-stack production app

---

## Tại sao Next.js?

- **App Router** — File-based routing, layouts, nested routes
- **Server Components** — Render trên server, zero JS bundle cho data fetching
- **Server Actions** — Form handling không cần API routes thủ công
- **SSR/SSG/ISR** — Chọn rendering strategy per-page
- **API Routes** — Backend endpoints trong cùng project
- **Production ready** — Image optimization, fonts, SEO

---

## Setup

```bash
npx create-next-app@latest my-app --typescript --tailwind --app
cd my-app
npm run dev  # http://localhost:3000
```

---

## App Router — Cấu trúc thư mục

```
app/
├── layout.tsx            # Root layout (bọc tất cả pages)
├── page.tsx              # Route: /
├── loading.tsx           # Loading UI tự động
├── error.tsx             # Error boundary tự động
├── not-found.tsx         # 404 page
│
├── (marketing)/          # Route group (không ảnh hưởng URL)
│   ├── layout.tsx
│   ├── page.tsx          # Route: /
│   └── about/
│       └── page.tsx      # Route: /about
│
├── blog/
│   ├── page.tsx          # Route: /blog
│   └── [slug]/
│       └── page.tsx      # Route: /blog/my-post
│
├── dashboard/
│   ├── layout.tsx        # Shared layout cho /dashboard/*
│   ├── page.tsx          # Route: /dashboard
│   └── settings/
│       └── page.tsx      # Route: /dashboard/settings
│
└── api/
    └── users/
        └── route.ts      # API: GET/POST /api/users
```

---

## Server vs Client Components

```typescript
// ✅ Server Component (default) — Chạy trên server
// - Fetch data trực tiếp, không cần useEffect
// - Không có state, event handlers
// - File: app/users/page.tsx (không có 'use client')

import { db } from '@/lib/db'

export default async function UsersPage() {
  // Fetch data trực tiếp — không cần fetch API
  const users = await db.user.findMany({
    where: { isActive: true },
    orderBy: { createdAt: 'desc' }
  })

  return (
    <div>
      <h1>Danh sách Users</h1>
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  )
}
```

```typescript
// ✅ Client Component — Chạy trên browser
// - Có state, event handlers, browser APIs
'use client'

import { useState } from 'react'

export function SearchBar({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('')

  return (
    <input
      value={query}
      onChange={e => setQuery(e.target.value)}
      onKeyDown={e => e.key === 'Enter' && onSearch(query)}
      placeholder="Tìm kiếm..."
    />
  )
}
```

---

## Rendering Strategies

```typescript
// Static Generation (SSG) — Mặc định, build time
export default async function BlogList() {
  const posts = await fetchPosts()  // Fetch 1 lần lúc build
  return <PostList posts={posts} />
}

// Static với revalidation (ISR)
async function fetchPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { revalidate: 3600 }  // Tái generate sau 1 giờ
  })
  return res.json()
}

// Dynamic — Server-side render mỗi request
import { cookies } from 'next/headers'

export const dynamic = 'force-dynamic'

export default async function Dashboard() {
  const sessionId = cookies().get('session_id')?.value
  const user = await getSession(sessionId)
  return <DashboardContent user={user} />
}

// Per-fetch caching control
const data1 = await fetch(url, { cache: 'force-cache' })     // Cache mãi
const data2 = await fetch(url, { cache: 'no-store' })         // Không cache
const data3 = await fetch(url, { next: { revalidate: 60 } })  // Revalidate 60s
```

---

## API Routes

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { z } from 'zod'

// GET /api/users
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const page = Number(searchParams.get('page') ?? 1)
  const limit = Number(searchParams.get('limit') ?? 20)

  const [users, total] = await prisma.$transaction([
    prisma.user.findMany({ skip: (page - 1) * limit, take: limit }),
    prisma.user.count()
  ])

  return NextResponse.json({ data: users, total, page, limit })
}

// POST /api/users
const createUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email()
})

export async function POST(request: NextRequest) {
  const body = await request.json()
  const parsed = createUserSchema.safeParse(body)
  
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.errors }, { status: 422 })
  }
  
  const user = await prisma.user.create({ data: parsed.data })
  return NextResponse.json(user, { status: 201 })
}
```

```typescript
// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await prisma.user.findUnique({ where: { id: params.id } })
  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }
  return NextResponse.json(user)
}
```

---

## Server Actions — Forms không cần API

```typescript
// app/actions/createPost.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'
import { auth } from '@/lib/auth'

export async function createPost(formData: FormData) {
  const session = await auth()
  if (!session) redirect('/login')

  const title = formData.get('title') as string
  const content = formData.get('content') as string

  // Validation
  if (!title || title.length < 5) {
    return { error: 'Tiêu đề tối thiểu 5 ký tự' }
  }

  const post = await prisma.post.create({
    data: { title, content, authorId: session.user.id }
  })

  revalidatePath('/blog')           // Invalidate cache
  redirect(`/blog/${post.id}`)     // Redirect sau khi tạo
}
```

```typescript
// app/blog/new/page.tsx
import { createPost } from '@/actions/createPost'

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input name="title" placeholder="Tiêu đề" />
      <textarea name="content" placeholder="Nội dung" />
      <button type="submit">Đăng bài</button>
    </form>
  )
}
```

---

## Metadata & SEO

```typescript
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next'

interface Props {
  params: { slug: string }
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug)
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.coverImage }],
      type: 'article',
      authors: [post.author.name],
      publishedTime: post.createdAt
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage]
    }
  }
}

// Static paths generation
export async function generateStaticParams() {
  const posts = await getAllPosts()
  return posts.map(post => ({ slug: post.slug }))
}
```

---

## Middleware — Auth, i18n, A/B Testing

```typescript
// middleware.ts (chạy trước mọi request)
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Auth protection
  const protectedPaths = ['/dashboard', '/settings', '/admin']
  const isProtected = protectedPaths.some(p => pathname.startsWith(p))

  if (isProtected) {
    const token = request.cookies.get('access_token')?.value
    if (!token) {
      return NextResponse.redirect(new URL('/login', request.url))
    }
  }

  // Add request ID header
  const requestId = crypto.randomUUID()
  const response = NextResponse.next()
  response.headers.set('X-Request-ID', requestId)
  return response
}

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)']
}
```

---

## Image & Font Optimization

```typescript
import Image from 'next/image'
import { Inter, Roboto_Mono } from 'next/font/google'

// Font optimization — tự host, không ping Google
const inter = Inter({
  subsets: ['latin', 'vietnamese'],
  display: 'swap'
})

// Image optimization — auto WebP, lazy loading, blur placeholder
function UserAvatar({ user }) {
  return (
    <Image
      src={user.avatarUrl}
      alt={`${user.name} avatar`}
      width={40}
      height={40}
      className="rounded-full"
      placeholder="blur"
      blurDataURL={user.avatarBlurHash}
    />
  )
}
```

---

## Bài tập thực hành

- [ ] Build Blog với SSG + ISR (data từ Markdown files)
- [ ] Dashboard với protected routes (Middleware + Server Components)
- [ ] E-commerce: Product listing (SSG) + Cart (Client state)
- [ ] Full-stack: Next.js + Prisma + PostgreSQL + Auth

---

## Tài nguyên thêm

- [Next.js Docs](https://nextjs.org/docs) — Rất chi tiết, có nhiều ví dụ
- [Next.js Examples](https://github.com/vercel/next.js/tree/canary/examples)
- [T3 Stack](https://create.t3.gg/) — Next.js + tRPC + Prisma + Auth
- [Vercel](https://vercel.com/) — Deploy Next.js dễ nhất
