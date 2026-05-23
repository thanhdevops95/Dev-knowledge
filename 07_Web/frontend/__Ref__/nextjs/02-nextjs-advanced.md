# Next.js Advanced

> **Tags:** `nextjs` `app-router` `server-components` `streaming` `rsc` `caching`
> **Level:** Intermediate | **Prerequisite:** `nextjs/01-nextjs-basics.md` `react/02-react-advanced.md`

---

## 1. App Router Architecture

```
app/
├── layout.tsx              # Root layout (wraps everything)
├── page.tsx                # Home page
├── loading.tsx             # Loading UI (Suspense boundary)
├── error.tsx               # Error boundary
├── not-found.tsx           # 404 page
├── globals.css
├── (marketing)/            # Route group (no URL segment)
│   ├── about/page.tsx     → /about
│   └── pricing/page.tsx   → /pricing
├── (dashboard)/
│   ├── layout.tsx          # Shared dashboard layout
│   ├── dashboard/page.tsx → /dashboard
│   └── settings/page.tsx  → /settings
├── blog/
│   ├── page.tsx           → /blog
│   ├── [slug]/
│   │   ├── page.tsx       → /blog/my-post
│   │   └── error.tsx      # Per-segment error boundary
│   └── [...tags]/
│       └── page.tsx       → /blog/tag1/tag2/...
├── api/
│   └── users/
│       ├── route.ts       → GET/POST /api/users
│       └── [id]/
│           └── route.ts   → GET/PUT/DELETE /api/users/123
└── _components/            # Co-located components (not in URL)
```

---

## 2. Server Components vs Client Components

```tsx
// SERVER COMPONENT (default in App Router)
// Runs on server, never shipped to client bundle
// Can: async/await, access DB directly, read env vars (server-side)
// Cannot: useState, useEffect, event handlers, browser APIs

// app/users/page.tsx
async function UsersPage() {
  // Direct DB access (no API needed!)
  const users = await db.query('SELECT id, name, email FROM users LIMIT 10');
  
  // Server-side data fetch
  const posts = await fetch('https://api.example.com/posts', {
    next: { revalidate: 60 }   // Cache for 60 seconds
  }).then(r => r.json());
  
  return (
    <div>
      <UserList users={users} />   {/* Server Component */}
      <LikeButton />               {/* Client Component — for interactivity */}
    </div>
  );
}

// CLIENT COMPONENT
// 'use client' directive = opt into client rendering
'use client';
import { useState } from 'react';

function LikeButton({ initialCount }: { initialCount: number }) {
  const [count, setCount] = useState(initialCount);
  return <button onClick={() => setCount(c => c + 1)}>❤️ {count}</button>;
}

// IMPORTANT: Server components can import Client components, NOT vice versa
// Passing Server Component as children to Client Component: OK!
function ServerParent() {
  return (
    <ClientProvider>
      <ServerDataComponent />   {/* Server component as children */}
    </ClientProvider>
  );
}
```

---

## 3. Data Fetching Patterns

```tsx
// 1. Parallel data fetching (avoid waterfalls)
async function DashboardPage() {
  // BAD: Sequential (waterfall)
  // const user = await getUser();
  // const orders = await getOrders(user.id);

  // GOOD: Parallel
  const [user, orders, notifications] = await Promise.all([
    getUser(),
    getOrders(),
    getNotifications(),
  ]);
  
  return <Dashboard user={user} orders={orders} notifications={notifications} />;
}

// 2. Streaming with Suspense (show parts as they load)
import { Suspense } from 'react';

async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id);  // Fast: from cache
  
  return (
    <div>
      <ProductInfo product={product} />  {/* Renders immediately */}
      
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews productId={params.id} />  {/* Slow: loads in background, streams */}
      </Suspense>
      
      <Suspense fallback={<Skeleton />}>
        <RelatedProducts productId={params.id} />  {/* Slow: independent */}
      </Suspense>
    </div>
  );
}

// Reviews is a Server Component that fetches its own data
async function Reviews({ productId }: { productId: string }) {
  const reviews = await getReviews(productId);  // Can be slow!
  return <ReviewList reviews={reviews} />;
}

// 3. Request Deduplication (fetch is deduplicated within render)
async function getUser(id: string) {
  const res = await fetch(`/api/users/${id}`);  // Deduped if called multiple times in same render!
  return res.json();
}

// 4. React cache() for non-fetch functions
import { cache } from 'react';

const getUser = cache(async (id: string) => {
  return db.users.findUnique({ where: { id } });
  // Memoized per-request (called multiple times → only one DB query)
});
```

---

## 4. Caching System

Next.js has **4 caches** that interact:

```
                    ╔═══════════════════════════════════════════╗
Client              ║  Router Cache (in-memory, client-side)    ║
                    ╠═══════════════════════════════════════════╣
Network             ║  Full Route Cache (server-rendered HTML)  ║
                    ╠═══════════════════════════════════════════╣
Server              ║  React Cache (per-request memoization)    ║
                    ╠═══════════════════════════════════════════╣
               fetch║  Data Cache (across requests, persistent) ║
                    ╚═══════════════════════════════════════════╝
```

```typescript
// Data Cache — fetch options
const data = await fetch('https://api.example.com/data', {
  cache: 'no-store',            // Never cache (dynamic)
  next: { revalidate: 60 },    // Cache for 60 seconds (ISR)
  next: { revalidate: 0 },     // Never cache (same as no-store)
  next: { tags: ['products'] }, // Tag for on-demand revalidation
});

// ISR — Incremental Static Regeneration
// Page-level:
export const revalidate = 60;  // Revalidate page every 60s

// Dynamic rendering (opt out of caching)
export const dynamic = 'force-dynamic';  // Like getServerSideProps
export const dynamic = 'force-static';   // Like getStaticProps

// On-demand revalidation
import { revalidatePath, revalidateTag } from 'next/cache';
import { NextRequest } from 'next/server';

export async function POST(req: NextRequest) {
  const { tag, path } = await req.json();
  
  revalidateTag('products');           // Invalidate all fetches tagged 'products'
  revalidatePath('/products');         // Invalidate the /products page
  revalidatePath('/products', 'layout');  // Also invalidate layout
}
```

---

## 5. Server Actions

Replace API routes for form submissions and mutations:

```tsx
// app/actions.ts
'use server';   // All functions in this file are Server Actions

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export async function createPost(formData: FormData) {
  // Input validation
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;
  
  if (!title || title.length < 3) {
    return { error: 'Title must be at least 3 characters' };
  }
  
  // Auth check
  const session = await getSession();
  if (!session) redirect('/login');
  
  // DB operation
  const post = await db.posts.create({
    data: { title, content, authorId: session.userId }
  });
  
  // Revalidate pages
  revalidatePath('/blog');
  revalidatePath(`/blog/${post.slug}`);
  
  // Redirect
  redirect(`/blog/${post.slug}`);
}

// Usage 1: in <form action>
export function NewPostForm() {
  return (
    <form action={createPost}>   {/* Server Action! No event handler needed */}
      <input name="title" required minLength={3} />
      <textarea name="content" />
      <button type="submit">Create Post</button>
    </form>
  );
}

// Usage 2: with useActionState (React 19 / next-safe-action)
'use client';
import { useActionState } from 'react';

function PostForm() {
  const [state, action, isPending] = useActionState(createPost, null);
  
  return (
    <form action={action}>
      {state?.error && <p className="error">{state.error}</p>}
      <input name="title" />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
}

// Usage 3: Inline in component ('use server' in closure)
async function deletePost(id: number) {
  'use server';
  await db.posts.delete({ where: { id } });
  revalidatePath('/blog');
}

function PostActions({ post }: { post: Post }) {
  return (
    <form action={deletePost.bind(null, post.id)}>
      <button type="submit">Delete</button>
    </form>
  );
}
```

---

## 6. Route Handlers (API Routes)

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
  role: z.enum(['admin', 'user']).default('user'),
});

// GET /api/users
export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const page = parseInt(searchParams.get('page') ?? '1');
  const limit = parseInt(searchParams.get('limit') ?? '10');

  const users = await db.users.findMany({
    skip: (page - 1) * limit,
    take: limit,
    select: { id: true, email: true, name: true },
  });

  return NextResponse.json({ users, page, limit });
}

// POST /api/users
export async function POST(req: NextRequest) {
  const body = await req.json();
  
  // Validate
  const result = CreateUserSchema.safeParse(body);
  if (!result.success) {
    return NextResponse.json(
      { error: result.error.format() },
      { status: 400 }
    );
  }
  
  const user = await db.users.create({ data: result.data });
  return NextResponse.json(user, { status: 201 });
}

// app/api/users/[id]/route.ts
export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await db.users.findUnique({ where: { id: params.id } });
  
  if (!user) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }
  
  return NextResponse.json(user);
}

// Streaming response
export async function GET(req: NextRequest) {
  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      for await (const chunk of generateData()) {
        controller.enqueue(encoder.encode(chunk));
      }
      controller.close();
    }
  });
  
  return new Response(stream, {
    headers: { 'Content-Type': 'text/plain' }
  });
}
```

---

## 7. Middleware

```typescript
// middleware.ts (root of project)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { verifyToken } from './lib/auth';

export async function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  
  // A/B testing: assign variant
  if (pathname === '/home') {
    const variant = Math.random() < 0.5 ? 'a' : 'b';
    const url = req.nextUrl.clone();
    url.pathname = `/home/${variant}`;
    return NextResponse.rewrite(url);
  }
  
  // Auth check for protected routes
  if (pathname.startsWith('/dashboard')) {
    const token = req.cookies.get('session')?.value;
    
    if (!token) {
      return NextResponse.redirect(new URL('/login', req.url));
    }
    
    const user = await verifyToken(token);
    if (!user) {
      const response = NextResponse.redirect(new URL('/login', req.url));
      response.cookies.delete('session');
      return response;
    }
    
    // Pass user info via headers to Client Components
    const response = NextResponse.next();
    response.headers.set('x-user-id', user.id);
    return response;
  }
  
  // Rate limiting via edge runtime
  // Geo-routing
  const country = req.geo?.country ?? 'US';
  if (country !== 'US' && pathname === '/') {
    return NextResponse.redirect(new URL(`/${country.toLowerCase()}`, req.url));
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/home',
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ]
};
```

---

## 8. Metadata & SEO

```tsx
// app/layout.tsx — root metadata
import type { Metadata, Viewport } from 'next';

export const metadata: Metadata = {
  title: {
    template: '%s | My App',
    default: 'My App',
  },
  description: 'My awesome application',
  metadataBase: new URL('https://myapp.com'),
  openGraph: {
    siteName: 'My App',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    creator: '@myapp',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport: Viewport = {
  themeColor: '#000000',
  width: 'device-width',
  initialScale: 1,
};

// app/blog/[slug]/page.tsx — dynamic metadata
export async function generateMetadata(
  { params }: { params: { slug: string } }
): Promise<Metadata> {
  const post = await getPost(params.slug);
  
  if (!post) return { title: 'Post Not Found' };
  
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.ogImage, width: 1200, height: 630 }],
      type: 'article',
      publishedTime: post.createdAt,
    },
    alternates: {
      canonical: `/blog/${params.slug}`,
    },
  };
}
```

---

## 9. Image & Font Optimization

```tsx
import Image from 'next/image';
import { Inter, JetBrains_Mono } from 'next/font/google';

// Font optimization — zero layout shift, self-hosted
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const mono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
});

// Apply in layout
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable} ${mono.variable}`}>
      <body>{children}</body>
    </html>
  );
}

// Image optimization
<Image
  src="/hero.jpg"
  alt="Hero image"
  width={1200}
  height={600}
  priority            // Preload for LCP images
  quality={85}
  sizes="(max-width: 768px) 100vw, 1200px"
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."  // Tiny blur placeholder
/>

// Remote images (must configure domains)
// next.config.ts
module.exports = {
  images: {
    remotePatterns: [
      { protocol: 'https', hostname: 'images.unsplash.com' },
    ],
  },
};
```

---

## 10. Performance Checklist

```typescript
// next.config.ts best practices
import type { NextConfig } from 'next';

const config: NextConfig = {
  experimental: {
    ppr: true,             // Partial PreRendering (streaming static + dynamic)
    reactCompiler: true,   // Auto-memoization
  },
  
  compress: true,          // Gzip/Brotli
  
  headers: async () => [
    {
      source: '/:all*(svg|jpg|png|webp|avif)',
      headers: [
        { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }
      ],
    },
  ],
  
  // Bundle analyzer
  // ANALYZE=true npm run build
};

export default config;
```

**Performance checklist:**
- [ ] Server Components for data-heavy, non-interactive UI
- [ ] Suspense boundaries for parallel data fetching
- [ ] `next/image` for all images
- [ ] `next/font` for Google Fonts
- [ ] `next/dynamic` for heavy client-side libraries
- [ ] Proper `cache` settings on fetch()
- [ ] `revalidate` for ISR on appropriate pages
- [ ] Middleware at Edge (no cold start)
- [ ] Bundle analyzer: `npm run analyze`

---

*Tài liệu liên quan: `nextjs/01-nextjs-basics.md` | `react/02-react-advanced.md` | `react/03-react-state-management.md`*
