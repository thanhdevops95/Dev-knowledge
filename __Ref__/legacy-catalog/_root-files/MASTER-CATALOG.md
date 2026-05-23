# 📚 MASTER CATALOG — Toàn bộ kiến thức Developer

> Danh sách đầy đủ MỌI chủ đề trong ngành phát triển phần mềm.
> ✅ = Có bài đầy đủ | 🚧 = Có skeleton (cần mở rộng) | ❌ = Chưa có
>
> **Format:** `File` | `Trạng thái` | `Chủ đề chính sẽ cover`

---

## 00 — Roadmaps (Lộ trình học)

| File | ST | Chủ đề chính |
|---|---|---|
| `00-overview.md` | ✅ | Tổng quan ngành, các vai trò (FE/BE/FS/DevOps/Data/AI), lộ trình gợi ý theo mục tiêu |
| `frontend-roadmap.md` | ✅ | HTML→CSS→JS→TS→React/Vue→State→Build tools→Testing→Performance |
| `backend-roadmap.md` | ✅ | Language→Framework→DB→API→Auth→Caching→Message queue→Deploy |
| `fullstack-roadmap.md` | ✅ | Kết hợp FE + BE, project structure, deployment, monorepo |
| `devops-roadmap.md` | ✅ | Linux→Docker→K8s→CI/CD→IaC→Cloud→Monitoring→SRE |
| `data-engineer-roadmap.md` | ✅ | SQL→Python→ETL→Orchestration→Spark→Warehouse→Streaming |
| `ai-ml-roadmap.md` | ✅ | Math→Python→Sklearn→DL→LLM→MLOps |
| `mobile-roadmap.md` | ❌ | React Native / Flutter / Native iOS & Android — lộ trình chọn hướng |
| `qa-roadmap.md` | ❌ | Manual→Automation (Playwright/Cypress)→API testing→Performance→Security testing |
| `security-roadmap.md` | ❌ | Networking→Web security→Crypto→Pentest→DevSecOps→Compliance |
| `blockchain-roadmap.md` | ❌ | Crypto basics→Solidity→dApp→DeFi→Web3 tooling |
| `game-dev-roadmap.md` | ❌ | Chọn engine (Unity/Unreal/Godot)→Math→Physics→Networking→Publishing |
| `embedded-iot-roadmap.md` | ❌ | C/C++→MCU→RTOS→Linux Embedded→IoT protocols→Cloud IoT |

---

## 01 — Computer Science Fundamentals

| File | ST | Chủ đề chính |
|---|---|---|
| `cs/01-how-computers-work.md` | 🚧 | CPU registers/cache, RAM addressing, virtual memory, OS kernel, boot process, interrupts |
| `cs/02-os-concepts.md` | 🚧 | Process vs Thread, scheduling (CFS), IPC (pipe/socket/shm), file system (inode), cgroups/namespaces |
| `cs/03-concurrency-parallelism.md` | 🚧 | Race condition, mutex/semaphore, deadlock (4 conditions), lock-free, event loop, CSP, Actor model |
| `cs/04-compilers-interpreters.md` | ❌ | Lexing, parsing, AST, semantic analysis, code gen, JIT, GC algorithms, Python bytecode, JVM |
| `cs/05-character-encoding.md` | 🚧 | ASCII, Unicode code points, UTF-8/16/32, BOM, Base64, mojibake bugs |
| `cs/06-number-systems.md` | ❌ | Binary, hex, octal, two's complement, IEEE 754 float, overflow, NaN, Infinity |
| `cs/07-design-by-contract.md` | ❌ | Preconditions, postconditions, invariants, DbC in Python/Eiffel, assertions |

### Programming Concepts
| File | ST | Chủ đề chính |
|---|---|---|
| `programming/01-oop.md` | 🚧 | Encapsulation, Inheritance, Polymorphism, Abstraction, SOLID (5 principles), composition vs inheritance |
| `programming/02-functional-programming.md` | 🚧 | Pure functions, immutability, map/filter/reduce, currying, composition, Functor/Monad basics |
| `programming/03-async-programming.md` | 🚧 | Callbacks, Promises, async/await, JS event loop (microtask/macrotask), asyncio, goroutines, backpressure |
| `programming/04-memory-management.md` | ❌ | Stack vs heap, manual memory (C/C++), reference counting, mark-and-sweep GC, RAII, memory leaks |
| `programming/05-type-systems.md` | ❌ | Static vs dynamic, strong vs weak, nominal vs structural typing, duck typing, type inference, generics |
| `programming/06-design-principles.md` | ❌ | DRY, KISS, YAGNI, separation of concerns, law of Demeter, composition root |
| `programming/07-concurrency-patterns.md` | ❌ | Thread pool, Producer-Consumer, Reactor/Proactor, Half-Sync/Half-Async, Active Object, Monitor Object |

### Data Structures & Algorithms
| File | ST | Chủ đề chính |
|---|---|---|
| `dsa/01-dsa-basics.md` | ✅ | Big O, Arrays, HashMaps, Stacks, Queues, Sorting (Merge/Quick/Heap), Binary Search |
| `dsa/02-linked-lists.md` | 🚧 | Singly/Doubly linked list, cycle detection (Floyd's), reverse, LRU Cache, interview patterns |
| `dsa/03-trees-graphs.md` | 🚧 | Binary Tree traversal, BST, AVL, Trie, BFS, DFS, topological sort, Dijkstra, A* |
| `dsa/04-heaps-priority-queues.md` | ❌ | Min/Max heap, heapify, heapsort, priority queue, Top-K problems, Kth largest |
| `dsa/05-dynamic-programming.md` | 🚧 | Memoization vs tabulation, Knapsack, LCS, LIS, Edit distance, Matrix chain, DP on trees |
| `dsa/06-greedy-algorithms.md` | ❌ | Greedy choice property, Activity selection, Huffman coding, Interval scheduling, Dijkstra as greedy |
| `dsa/07-string-algorithms.md` | ❌ | KMP, Rabin-Karp, Z-algorithm, Boyer-Moore, Trie ops, suffix arrays, anagram detection |
| `dsa/08-bit-manipulation.md` | ❌ | AND/OR/XOR/NOT, bit shifts, two's complement tricks, Brian Kernighan, power of 2, subset enumeration |
| `dsa/09-math-algorithms.md` | ❌ | GCD/LCM, prime sieve, modular arithmetic, fast exponentiation, combinatorics |
| `dsa/10-competitive-coding.md` | 🚧 | LeetCode patterns (Two Pointers, Sliding Window, BFS/DFS, DP), Blind 75, NeetCode 150, UMPIRE framework |

---

## 02 — Version Control

| File | ST | Chủ đề chính |
|---|---|---|
| `git/01-git-basics.md` | ✅ | init, clone, add, commit, push, pull, branch, merge, diff, log, .gitignore |
| `git/02-git-advanced.md` | 🚧 | Interactive rebase, cherry-pick, bisect, reflog, stash, submodules, pre-commit hooks, git attributes |
| `git/03-git-workflows.md` | 🚧 | GitFlow, GitHub Flow, Trunk-based, monorepo vs polyrepo, Conventional Commits, semantic versioning |
| `git/04-github-gitlab.md` | ❌ | Pull Requests, code review, Issues, Projects, Actions CI basics, Pages, Protected branches, CODEOWNERS |

---

## 03 — Terminal & OS

| File | ST | Chủ đề chính |
|---|---|---|
| `terminal/01-terminal-basics.md` | ✅ | Navigation, file ops, permissions, processes, pipe/redirect, env vars, SSH basics |
| `terminal/02-bash-scripting.md` | 🚧 | Variables/quoting, if/loops/functions, pipes, exit codes, set -euo pipefail, trap, xargs |
| `terminal/03-shell-tools.md` | 🚧 | grep/ripgrep, awk, sed, jq, fzf, tmux, curl, watch, htop, lsof, ss, diff |
| `terminal/04-vim-neovim.md` | ❌ | Modes (Normal/Insert/Visual), motions, commands, .vimrc, plugins (NvChad, LazyVim), macros |
| `linux/01-linux-essentials.md` | ❌ | FHS, chmod/chown/umask, users/groups, processes (ps/kill/nice), package managers (apt/dnf/pacman) |
| `linux/02-linux-administration.md` | ❌ | systemd units, journalctl, cron/crontab, syslog, iptables/firewalld, SSH hardening, performance (vmstat/iostat) |
| `linux/03-linux-networking.md` | ❌ | ip/ifconfig, tc (traffic control), ss/netstat, network namespaces, eBPF basics, nftables, traceroute/mtr |
| `regex/01-regex-basics.md` | 🚧 | Quantifiers, character classes, anchors, groups, flags (g/i/m), greedy vs lazy, common patterns |
| `regex/02-regex-advanced.md` | ❌ | Named groups, lookahead/lookbehind, backreferences, possessive quantifiers, atomic groups, PCRE vs RE2 |

---

## 04 — Networking

| File | ST | Chủ đề chính |
|---|---|---|
| `01-http-networking.md` | ✅ | HTTP/1.1/2/3, methods, status codes, headers, cookies, CORS, caching (ETag, Cache-Control) |
| `02-how-internet-works.md` | ✅ | DNS lookup, TCP handshake, TLS, HTTP req/res, CDN, browser rendering pipeline |
| `03-osi-tcp-ip.md` | 🚧 | 7 OSI layers, TCP vs UDP, IP addressing, CIDR, subnetting, ARP, ICMP, common ports |
| `04-tls-ssl.md` | 🚧 | TLS 1.2/1.3 handshake, certificate chain (Root CA/Intermediate/Leaf), CSR, Let's Encrypt, mTLS, OCSP |
| `05-dns.md` | ❌ | Resolution process, record types (A/AAAA/CNAME/MX/TXT/SRV/NS), zones, TTL, split-horizon, DNSSEC |
| `06-load-balancing.md` | 🚧 | Round Robin, Weighted, Least Conn, IP Hash, consistent hashing, L4 vs L7, health checks, drain |
| `07-cdn.md` | ❌ | PoP/edge servers, Cache-Control, cache busting, Cloudflare (CDN/WAF/Workers), CloudFront, edge computing |
| `08-proxies.md` | ❌ | Forward proxy (client-side), reverse proxy (server-side), SOCKS5, Nginx proxy_pass, API Gateway |
| `09-websockets-sse.md` | ✅ | → xem `07-Backend/realtime/01-websockets.md` |
| `10-vpn-tunneling.md` | ❌ | WireGuard, OpenVPN, IPSec, SSH tunneling, SOCKS proxy, site-to-site vs client VPN |
| `11-tcp-deep-dive.md` | ❌ | Three-way handshake, congestion control (CUBIC/BBR), Nagle's algorithm, TIME_WAIT, TCP vs UDP tradeoffs |
| `12-http3-quic.md` | ❌ | QUIC transport layer, 0-RTT handshake, stream multiplexing (no HOL blocking), HTTP/3 adoption, QUIC internals |

---

## 05 — Languages

### Python
| File | ST | Chủ đề chính |
|---|---|---|
| `python/01-python-basics.md` | ✅ | Syntax, types, lists/dicts/sets, comprehensions, functions, classes, files, exceptions, venv |
| `python/02-python-advanced.md` | 🚧 | Decorators, generators/yield, context managers, metaclasses, type hints, dataclasses, asyncio deep dive |
| `python/03-python-packaging.md` | ❌ | pyproject.toml, Poetry, pip, venv, virtualenv, publishing to PyPI, dependency management |
| `python/04-python-testing.md` | ❌ | pytest, fixtures, parametrize, mocking (unittest.mock), coverage, hypothesis (property-based) |
| `python/05-python-performance.md` | ❌ | Profiling (cProfile, py-spy), Cython, Numba, multiprocessing, concurrent.futures, GIL workarounds |

### JavaScript
| File | ST | Chủ đề chính |
|---|---|---|
| `javascript/01-js-basics.md` | ✅ | Syntax, types, functions, objects, arrays, DOM, async/await, fetch, ES6+ features |
| `javascript/02-js-advanced.md` | 🚧 | Execution context, closures, prototype chain, `this` (4 rules), event loop, WeakMap, Proxy, Reflect |
| `javascript/03-js-modules.md` | ❌ | ESM (import/export), CommonJS (require), dynamic import, tree-shaking, module federation |
| `javascript/04-node-internals.md` | ❌ | libuv, V8 internals, Worker threads, Cluster, streams, Buffer, EventEmitter |

### TypeScript
| File | ST | Chủ đề chính |
|---|---|---|
| `typescript/01-typescript-basics.md` | ✅ | Types, interfaces, enums, type narrowing, utility types (Partial/Required/Pick/Omit/Record), tsconfig |
| `typescript/02-typescript-advanced.md` | 🚧 | Generics, mapped types, conditional types (T extends U), infer, template literal types, discriminated unions |

### Go
| File | ST | Chủ đề chính |
|---|---|---|
| `go/01-go-basics.md` | ✅ | Syntax, structs, interfaces, methods, error handling, defer/panic/recover, slices, maps, packages |
| `go/02-go-concurrency.md` | 🚧 | Goroutines, channels (buffered/unbuffered), select, WaitGroup, Mutex, context, worker pool, errgroup |
| `go/03-go-tooling.md` | ❌ | go modules, go test, benchmarks, go vet, golangci-lint, go build/install, embed, generics (Go 1.18+) |
| `go/04-go-performance.md` | ❌ | pprof profiling, escape analysis, GC tuning, memory layout, sync.Pool, zero allocation patterns |

### Java
| File | ST | Chủ đề chính |
|---|---|---|
| `java/01-java-basics.md` | ✅ | Syntax, OOP, generics, collections, streams API, exceptions, I/O, Maven/Gradle |
| `java/02-java-modern.md` | ❌ | Java 17-21: Records, Sealed classes, Pattern matching, Text blocks, Virtual threads (Loom), Stream gatherers |

### C#
| File | ST | Chủ đề chính |
|---|---|---|
| `csharp/01-csharp-basics.md` | 🚧 | Syntax, types, LINQ, async/await (Task), properties, generics, null handling, records, pattern matching |
| `csharp/02-dotnet-ecosystem.md` | 🚧 | .NET 8, CLR/JIT, EF Core, Blazor, MAUI, ASP.NET Core basics, dotnet CLI, NuGet |

### Rust
| File | ST | Chủ đề chính |
|---|---|---|
| `rust/01-rust-basics.md` | 🚧 | Ownership, borrowing, lifetimes, structs, enums, pattern matching, Result/Option, traits, Cargo |
| `rust/02-rust-async.md` | ❌ | Tokio, async/await, futures, Pin, select!, channels (mpsc/broadcast), axum web framework |

### C / C++
| File | ST | Chủ đề chính |
|---|---|---|
| `c/01-c-basics.md` | ❌ | Syntax, pointers, memory (malloc/free), structs, file I/O, preprocessor, make |
| `cpp/01-cpp-basics.md` | ❌ | Syntax, classes, RAII, references, templates basics, STL (vector/map/set/algorithm) |
| `cpp/02-cpp-modern.md` | ❌ | C++17/20: smart pointers (unique_ptr/shared_ptr), move semantics, lambdas, concepts, ranges, coroutines |

### Other Languages
| File | ST | Chủ đề chính |
|---|---|---|
| `php/01-php-basics.md` | ❌ | Syntax, arrays, functions, OOP (PHP 8+), Composer, Laravel basics |
| `ruby/01-ruby-basics.md` | ❌ | Syntax, blocks/procs/lambdas, modules, gems, Rails basics, metaprogramming |
| `kotlin/01-kotlin-basics.md` | 🚧 | Syntax, null safety, extension functions, coroutines, data classes, sealed classes, Android basics |
| `swift/01-swift-basics.md` | 🚧 | Syntax, optionals, protocols, closures, concurrency (async/await), SwiftUI basics |
| `scala/01-scala-basics.md` | ❌ | Syntax, case classes, pattern matching, traits, FP (map/filter/fold), Akka, Spark |
| `elixir/01-elixir-basics.md` | ❌ | Syntax, pattern matching, immutability, processes (Actor model), OTP, Phoenix framework, pipe operator |
| `dart/01-dart-basics.md` | ❌ | Syntax, null safety, async/await (Future/Stream), classes, mixins, generics — cơ sở cho Flutter |
| `r/01-r-basics.md` | ❌ | Syntax, data.frame, ggplot2, dplyr/tidyr, statistical functions, R Markdown |
| `lua/01-lua-basics.md` | ❌ | Syntax, tables, metatables, coroutines, modules, game scripting (LöVE2D, Neovim config) |
| `assembly/01-assembly-basics.md` | ❌ | Registers, instructions, stack, calling conventions (x86-64), NASM/GAS, system calls |

---

## 06 — Frontend

### Core
| File | ST | Chủ đề chính |
|---|---|---|
| `html/01-html-basics.md` | ✅ | Semantic elements, forms, tables, metadata, SEO tags, accessibility attributes, links/images |
| `html/02-html-advanced.md` | ❌ | Web components, Custom elements, Shadow DOM, HTML templates, microdata, Canvas, SVG |
| `css/01-css-basics.md` | ✅ | Box model, Flexbox, Grid, selectors, specificity, pseudo-classes, responsive design, media queries |
| `css/02-css-advanced.md` | ❌ | Custom properties (variables), CSS layers, container queries, Houdini, @property, CSS-in-JS |
| `css/03-sass-scss.md` | ❌ | Variables, nesting, mixins, functions, extends, modules (@use/@forward), compiled vs CSS vars |
| `css/04-animation.md` | ❌ | @keyframes, transitions, animation properties, Framer Motion (React), GSAP, CSS performance (will-change) |

### Frameworks
| File | ST | Chủ đề chính |
|---|---|---|
| `react/01-react-basics.md` | ✅ | JSX, components, props, state, hooks (useState/useEffect/useRef/useMemo/useCallback), context, forms |
| `react/02-react-advanced.md` | ❌ | Concurrent features, Suspense, lazy(), memo, useTransition, error boundaries, profiler, compound components |
| `react/03-react-patterns.md` | ❌ | HOC, Render props, Compound component, Control props, Custom hooks pattern, Provider pattern |
| `vue/01-vue-basics.md` | ✅ | SFC, Composition API, ref/reactive, computed, watch, lifecycle, Pinia, Vue Router |
| `vue/02-vue-advanced.md` | ❌ | Provide/inject, custom directives, teleport, Transition, renderless components, Vue 3 Suspense |
| `nextjs/01-nextjs-basics.md` | ✅ | App Router, Server/Client components, SSG/SSR/ISR, API routes, Server Actions, metadata, Middleware |
| `nextjs/02-nextjs-advanced.md` | ❌ | Edge runtime, Partial Prerendering, cache granularity, Turbopack, tRPC, next-auth |
| `angular/01-angular-basics.md` | 🚧 | Components, modules, services, DI, templates (*ngIf/*ngFor), RxJS, HttpClient, routing, Signals |
| `angular/02-angular-advanced.md` | ❌ | Standalone components, lazy loading, NgRx, Angular CDK, custom pipes, testing (Jasmine/Karma) |
| `svelte/01-svelte-basics.md` | 🚧 | Components, reactivity ($:), stores, lifecycle, slots, transitions, SvelteKit routing, Svelte 5 Runes |
| `nuxtjs/01-nuxtjs-basics.md` | ❌ | Nuxt 3, file-based routing, composables, server routes, plugins, modules, Nitro server |
| `astro/01-astro-basics.md` | ❌ | Islands architecture, .astro components, frontmatter, content collections, integrations (React/Vue/Svelte) |
| `remix/01-remix-basics.md` | ❌ | Loaders, actions, nested routes, error boundaries, forms, server-side rendering, Vite + Remix |
| `jquery/01-jquery-basics.md` | ❌ | Selectors, DOM manipulation, events, AJAX, animations, plugins — legacy codebase context |

### State Management
| File | ST | Chủ đề chính |
|---|---|---|
| `state-management/01-redux-toolkit.md` | 🚧 | RTK: createSlice, createAsyncThunk, RTK Query, middleware, Redux DevTools, when to use Redux |
| `state-management/02-zustand.md` | 🚧 | Store creation, selectors, async actions, persist/devtools/immer middleware, slice pattern |
| `state-management/03-react-query-tanstack.md` | 🚧 | useQuery, useMutation, cache invalidation, optimistic updates, infinite queries, prefetching, Suspense |
| `state-management/04-jotai-recoil.md` | ❌ | Atomic state, atoms, selectors, derived state, async atoms, DevTools, comparison with Zustand |
| `state-management/05-xstate.md` | ❌ | Finite state machines, statecharts, actors, guards, actions, invoke, @xstate/react |

### Build Tools & Package Managers
| File | ST | Chủ đề chính |
|---|---|---|
| `build-tools/01-vite.md` | 🚧 | Dev server (esbuild pre-bundle), HMR, Rollup build, vite.config.ts, plugins, env vars, library mode |
| `build-tools/02-webpack.md` | 🚧 | Entry/output/mode, loaders (babel/css/file), plugins, code splitting, tree-shaking, source maps, Module Federation |
| `build-tools/03-esbuild-rollup-turbopack.md` | ❌ | esbuild speed, Rollup for libraries, Turbopack (Next.js), Parcel zero-config, comparison chart |
| `build-tools/04-babel.md` | ❌ | Presets (@babel/env), plugins, polyfills, browserslist, core-js, babel vs SWC vs esbuild |
| `build-tools/05-monorepo-tools.md` | ❌ | Nx (project graph, generators, cache), Turborepo (pipeline, remote cache), Lerna, Changesets |
| `package-managers/01-npm-yarn-pnpm.md` | ❌ | package.json, lock files, workspaces (monorepo), npm scripts, publish, audit, pnpm symlinks |
| `package-managers/02-bun.md` | ❌ | Bun runtime (JS/TS native), bun install, bun run, bun:sqlite, bun serve, vs Node.js comparison |

### CSS Frameworks & Design Systems
| File | ST | Chủ đề chính |
|---|---|---|
| `css-frameworks/01-tailwindcss.md` | 🚧 | Utility classes, responsive (sm:/md:/lg:), dark mode, tailwind.config.ts, @apply, JIT, clsx/cn |
| `css-frameworks/02-bootstrap.md` | ❌ | Grid system, components, utilities, JS components, customization with Sass |
| `css-frameworks/03-shadcn-ui.md` | ❌ | Component copy approach, Radix UI primitives, theming (CSS vars), tailwind integration |
| `design-systems/01-design-tokens.md` | ❌ | Color palettes, typography scale, spacing, shadows — token management (Style Dictionary) |
| `design-systems/02-storybook.md` | ❌ | Stories, Controls, Args, Decorators, Addons (a11y, viewport), interaction testing, Chromatic |

### Quality & Performance
| File | ST | Chủ đề chính |
|---|---|---|
| `performance/01-web-vitals.md` | 🚧 | LCP (<2.5s), CLS (<0.1), INP (<200ms), FID — measurement (CrUX, Lighthouse), optimization strategies |
| `performance/02-profiling.md` | ❌ | Chrome DevTools Performance tab, waterfall, JS flamegraph, memory heap snapshot, coverage |
| `performance/03-code-splitting.md` | ❌ | Dynamic import(), React.lazy/Suspense, route-based splitting, preload/prefetch, bundle analysis |
| `performance/04-browser-rendering.md` | ❌ | Critical rendering path, CSSOM, reflow vs repaint, compositor thread, GPU layers, will-change, layout thrashing |
| `seo/01-seo-technical.md` | ❌ | robots.txt, sitemap.xml, canonical, structured data (JSON-LD), Open Graph, Core Web Vitals SEO impact |
| `testing/01-unit-component.md` | ❌ | Jest/Vitest config, RTL (getBy/findBy/queryBy), user-event, mocking modules, snapshot testing |
| `testing/02-e2e-playwright.md` | ❌ | Page object model, locators, fixtures, API mocking, screenshot/video, CI integration |
| `testing/03-visual-regression.md` | ❌ | Chromatic (Storybook), Percy, pixel-diff vs AI-diff, baseline management |

### Advanced Web
| File | ST | Chủ đề chính |
|---|---|---|
| `accessibility/01-a11y-basics.md` | 🚧 | WCAG 2.1 (A/AA/AAA), ARIA roles/labels/hidden, keyboard nav, focus management, color contrast, screen readers |
| `pwa/01-pwa-basics.md` | 🚧 | Web App Manifest, Service Worker lifecycle, cache strategies (Cache First/Network First), push notifications |
| `i18n/01-internationalization.md` | ❌ | i18next, react-i18next, locale detection, pluralization, date/number formatting (Intl API), RTL |
| `ux/01-ux-for-developers.md` | ❌ | Design principles (proximity/contrast/hierarchy), color theory, typography, spacing (8pt grid), affordances |
| `web-apis/01-browser-apis.md` | ❌ | Canvas 2D, WebGL basics, WebRTC (video/audio), Geolocation, File API, Clipboard, Notifications |
| `web-apis/02-web-workers.md` | ❌ | Dedicated workers, SharedWorker, message passing, Comlink, offloading heavy computation |
| `web-apis/03-webassembly.md` | ❌ | Wasm concepts, Emscripten, wasm-pack (Rust), wat format, memory model, use cases (video codec, games) |
| `micro-frontends/01-micro-frontends.md` | ❌ | Module Federation, single-spa, iframes, web components approach, routing, shared state, deployment |

---

## 07 — Backend

### API Design
| File | ST | Chủ đề chính |
|---|---|---|
| `api-design/01-rest-api.md` | ✅ | REST constraints, HTTP verbs, status codes, versioning, HATEOAS, pagination, error format |
| `api-design/02-graphql.md` | 🚧 | SDL schema, queries/mutations/subscriptions, resolvers, N+1 + DataLoader, Apollo Server, Federation |
| `api-design/03-grpc.md` | 🚧 | Protocol Buffers, 4 service types, code gen, interceptors, gRPC-Web, error codes vs HTTP |
| `api-design/04-websocket-sse.md` | ✅ | → xem `realtime/01-websockets.md` |
| `api-design/05-api-security.md` | ❌ | Rate limiting (token bucket/sliding window), CORS, API keys, HMAC signing, IP allowlist |
| `api-design/06-openapi-swagger.md` | ❌ | OpenAPI 3.1 spec, Swagger UI, codegen (openapi-generator), contract-first vs code-first |
| `api-design/07-idempotency.md` | ❌ | Idempotency keys, safe vs unsafe vs idempotent methods, retry design, exactly-once semantics |
| `api-design/08-third-party-integrations.md` | ❌ | Stripe (payments), Twilio (SMS/Voice), SendGrid (email), webhook design, retry/idempotency, SDK vs raw API |
| `api-design/09-api-versioning.md` | ❌ | URI versioning (/v1), Header versioning (Accept), Query param, deprecation strategy, sunset headers, migration |

### Backend Frameworks
| File | ST | Chủ đề chính |
|---|---|---|
| `frameworks/01-fastapi.md` | ✅ | Path params, Pydantic models, dependency injection, middleware, background tasks, WebSocket, OpenAPI |
| `frameworks/02-express-nodejs.md` | ✅ | Routing, middleware, req/res, error handling, async patterns, JSON, CORS, file upload |
| `frameworks/03-django.md` | 🚧 | MTV pattern, ORM + migrations, Admin, DRF (serializers/ViewSets), JWT auth, Channels, Celery |
| `frameworks/04-nestjs.md` | 🚧 | Modules, Controllers, Services, DI, Pipes, Guards, Interceptors, TypeORM/Prisma, Microservices mode |
| `frameworks/05-spring-boot.md` | 🚧 | IoC/DI, @RestController, Spring Data JPA, Spring Security + JWT, Actuator, @ConfigurationProperties |
| `frameworks/06-aspnet-core.md` | 🚧 | Minimal API, MVC, DI container, EF Core, Identity, middleware pipeline, Health checks |
| `frameworks/07-gin-go.md` | 🚧 | Router/RouterGroup, binding + validation, middleware, context, file upload, testing (httptest) |
| `frameworks/08-laravel.md` | ❌ | Eloquent ORM, Blade, Artisan, middleware, Jobs/Queues (Horizon), broadcasting, Sanctum/Passport |
| `frameworks/09-rails.md` | ❌ | ActiveRecord, Routes, Controllers, Views, Devise auth, ActionCable, Sidekiq, Rails conventions |
| `frameworks/10-flask.md` | ❌ | Routes, Blueprints, Flask-SQLAlchemy, Flask-Login, Flask-RESTful, testing |

### Infrastructure Patterns
| File | ST | Chủ đề chính |
|---|---|---|
| `messaging/01-message-queues.md` | ✅ | Kafka (topics/partitions/consumer groups), RabbitMQ (exchanges/queues), pub-sub vs work queues |
| `realtime/01-websockets.md` | ✅ | WS protocol, FastAPI/Node WS server, reconnect logic, SSE for AI streaming, scaling (Redis pub-sub) |
| `background-jobs/01-background-jobs.md` | 🚧 | Celery (tasks/workers/beat), BullMQ (queues/workers/flows), retry + exponential backoff, idempotency |
| `caching/01-caching-strategies.md` | ❌ | Cache-aside, Read-through, Write-through, Write-behind, TTL, eviction policies (LRU/LFU), CDN cache |
| `caching/02-redis-patterns.md` | ❌ | Pub/sub, distributed locks (Redlock), rate limiting, Session, Leaderboard, Bloom filter |
| `caching/03-cdn-caching.md` | ❌ | Varnish (VCL), Fastly (Compute@Edge), cache purge strategies, surrogate keys, stale-while-revalidate |
| `backend-patterns/01-repository-pattern.md` | ❌ | Repository vs DAO, unit of work, abstracting DB layer, testability |
| `backend-patterns/02-middleware.md` | ❌ | Request pipeline, cross-cutting concerns (logging/auth/tracing), composition order |
| `backend-patterns/03-dependency-injection.md` | ❌ | IoC container, service lifetime (singleton/scoped/transient), DI in Python/Go/Node |
| `file-handling/01-file-upload.md` | ❌ | Multipart/form-data, streaming large files, S3 presigned URLs, chunked upload (tus protocol), virus scanning |
| `performance/01-load-testing.md` | ❌ | k6 (scenarios, VUs, checks), Locust, Artillery, interpreting p95/p99 latency, ramp-up |
| `performance/02-backend-profiling.md` | ❌ | flamegraph, py-spy (Python), pprof (Go), async-profiler (Java), identifying hot paths |
| `ssh/01-ssh-advanced.md` | ❌ | SSH keys (ed25519), agent forwarding, tunnels (local/remote/dynamic), ProxyJump, config file, hardening |

---

## 08 — Databases

### SQL
| File | ST | Chủ đề chính |
|---|---|---|
| `sql/01-sql-basics.md` | ✅ | SELECT/INSERT/UPDATE/DELETE, JOINs, GROUP BY, aggregates, subqueries, CTEs, window functions |
| `sql/02-postgresql-advanced.md` | 🚧 | JSONB operators/GIN index, table partitioning (range/list/hash), materialized views, LISTEN/NOTIFY, RLS, pgBouncer |
| `sql/03-query-optimization.md` | 🚧 | EXPLAIN ANALYZE, execution plans, B-tree/Hash/GIN/GiST/BRIN indexes, covering+partial indexes, N+1, VACUUM |
| `sql/04-transactions-isolation.md` | 🚧 | ACID, Read Uncommitted/Committed/Repeatable/Serializable, deadlocks, FOR UPDATE/SHARE, 2PC |
| `sql/05-replication.md` | ❌ | Primary/replica, WAL streaming, logical replication, replication lag, failover, read scaling |
| `sql/06-mysql.md` | ❌ | Storage engines (InnoDB/MyISAM), replication, binary log, FULLTEXT, MySQL 8 features |
| `sql/07-sqlite.md` | ❌ | WAL mode, file-based DB, use cases (embedded, tests, local app), SQLite vs Postgres |
| `sql/08-sql-server.md` | ❌ | T-SQL, CTEs, window functions, columnstore index, Always On AG, SSMS, Entity Framework |
| `sql/09-connection-pooling.md` | ❌ | pgBouncer (transaction/session/statement mode), HikariCP, pool sizing formula, monitoring |
| `sql/10-database-internals.md` | ❌ | B+ tree internals, WAL mechanism, MVCC (Multi-Version Concurrency Control), buffer pool, page format |
| `data-formats/01-data-formats.md` | ❌ | JSON/CSV/Parquet/Avro/ORC/Protobuf/MessagePack — so sánh hiệu năng, schema evolution, khi nào dùng gì |

### NoSQL
| File | ST | Chủ đề chính |
|---|---|---|
| `nosql/01-mongodb.md` | ✅ | Documents/collections, CRUD, aggregation pipeline, indexes, transactions, Atlas, schema design tips |
| `nosql/02-redis.md` | ✅ | Data types (String/Hash/List/Set/ZSet/Stream), pub/sub, Lua scripts, persistence (RDB/AOF), Cluster |
| `nosql/03-cassandra.md` | ❌ | Wide-column model, CQL, partition key design, consistency levels, eventual consistency, tunable consistency |
| `nosql/04-elasticsearch.md` | 🚧 | Inverted index, mapping, Query DSL (match/term/range/bool), analyzers, aggregations, ILM, OpenSearch |
| `nosql/05-neo4j.md` | ❌ | Graph model (nodes/edges/properties), Cypher query language, graph algorithms, use cases (fraud, social) |
| `nosql/06-dynamodb.md` | ❌ | Partition+sort key design, GSI/LSI, DAX caching, streams, capacity modes, single-table design |
| `nosql/07-influxdb.md` | ❌ | Time series concepts, InfluxQL/Flux, retention policies, continuous queries, Telegraf agent |
| `nosql/08-vector-databases.md` | 🚧 | Embeddings, ANN (HNSW/IVF), cosine/dot/L2 similarity, Pinecone/Chroma/Qdrant/pgvector, hybrid search |
| `nosql/09-firestore.md` | ❌ | Document model, real-time listeners, offline support, security rules, subcollections, composite indexes |
| `nosql/10-search-comparison.md` | ❌ | Elasticsearch vs Typesense vs Algolia vs MeiliSearch vs OpenSearch — when to use which |

### ORM & Data Access
| File | ST | Chủ đề chính |
|---|---|---|
| `orm/01-orm-basics.md` | ✅ | Prisma (schema/migrations/client), SQLAlchemy 2.0 (Core+ORM), ActiveRecord, Hibernate |
| `orm/02-migrations.md` | ❌ | Schema evolution strategies, Alembic (Python), Flyway/Liquibase (Java), zero-downtime migrations |

### Data Modeling
| File | ST | Chủ đề chính |
|---|---|---|
| `data-modeling/01-relational-modeling.md` | ❌ | ERD notation, normalization (1NF→3NF→BCNF), surrogate vs natural keys, soft delete, audit columns |
| `data-modeling/02-nosql-modeling.md` | ❌ | Embed vs reference (MongoDB), access patterns first, denormalization, time series schema |
| `data-modeling/03-warehouse-modeling.md` | ❌ | Star schema, snowflake schema, fact/dimension tables, SCD types (1/2/3), data vault |

---

## 09 — DevOps & Infrastructure

### Containers
| File | ST | Chủ đề chính |
|---|---|---|
| `docker/01-docker-basics.md` | ✅ | Dockerfile, images, containers, volumes, networks, compose, registry, multi-stage builds |
| `docker/02-docker-advanced.md` | ❌ | BuildKit, layer caching, secrets, non-root user, distroless/slim images, Docker Scout (security scan) |
| `docker/03-docker-compose.md` | ❌ | Services, depends_on, healthcheck, env_file, profiles, override files, production patterns |

### Kubernetes
| File | ST | Chủ đề chính |
|---|---|---|
| `kubernetes/01-kubernetes-basics.md` | ✅ | Pod, Deployment, Service, ConfigMap, Secret, Ingress, Namespace, kubectl cheatsheet |
| `kubernetes/02-helm.md` | 🚧 | Chart structure, values.yaml, templates (go templating), repositories, upgrade/rollback, Helmfile |
| `kubernetes/03-k8s-networking.md` | ❌ | ClusterIP/NodePort/LoadBalancer, Ingress (Nginx/Traefik), NetworkPolicy, service mesh basics |
| `kubernetes/04-k8s-security.md` | ❌ | RBAC (Role/ClusterRole/Binding), PodSecurityAdmission, NetworkPolicy, secrets encryption |
| `kubernetes/05-k8s-storage.md` | ❌ | PV/PVC, StorageClass, dynamic provisioning, StatefulSet, volume types (hostPath/NFS/CSI) |
| `kubernetes/06-k8s-monitoring.md` | ❌ | Prometheus Operator, kube-state-metrics, ServiceMonitor, Grafana dashboards, HPA/VPA |
| `kubernetes/07-k8s-production.md` | ❌ | Resource requests/limits, QoS classes, node affinity, PodDisruptionBudget, cluster upgrade |

### CI/CD
| File | ST | Chủ đề chính |
|---|---|---|
| `cicd/01-github-actions.md` | ✅ | Workflows, triggers, jobs, steps, actions, secrets, matrix, environments, OIDC |
| `cicd/02-gitlab-ci.md` | ❌ | .gitlab-ci.yml, stages, jobs, runners, artifacts, environments, GitLab Container Registry |
| `cicd/03-jenkins.md` | ❌ | Jenkinsfile (Declarative/Scripted), stages, agents, shared libraries, Blue Ocean |
| `cicd/04-argocd-gitops.md` | ❌ | GitOps principles, Application, Sync waves, App of Apps, Argo Rollouts, Argo Workflows |
| `cicd/05-release-strategies.md` | ❌ | Blue/Green, Canary, Rolling update, Feature flags (LaunchDarkly/Unleash), rollback strategies |

### Infrastructure as Code
| File | ST | Chủ đề chính |
|---|---|---|
| `iac/01-terraform.md` | ✅ | HCL syntax, providers, resources, variables, outputs, modules, state (local/remote), workspaces |
| `iac/02-ansible.md` | 🚧 | Inventory, playbooks, tasks, modules, roles, Vault (encrypt secrets), Galaxy |
| `iac/03-pulumi.md` | ❌ | IaC with real code (TS/Python/Go), Stack, Config, automation API |
| `iac/04-cdk.md` | ❌ | AWS CDK v2: Constructs (L1/L2/L3), Stacks, Aspects, CDK Pipelines |

### Web Servers
| File | ST | Chủ đề chính |
|---|---|---|
| `nginx/01-nginx.md` | 🚧 | server/location blocks, proxy_pass, SSL termination, rate limiting, load balancing upstream, gzip, security headers |
| `nginx/02-caddy.md` | ❌ | Caddyfile, automatic HTTPS (Let's Encrypt), reverse proxy, File server, plugins, Caddy API |

### Observability
| File | ST | Chủ đề chính |
|---|---|---|
| `observability/01-observability.md` | ✅ | 3 pillars (Logs/Metrics/Traces), structured logging, log levels, Prometheus data model, distributed tracing |
| `observability/02-elk-stack.md` | ❌ | Elasticsearch + Logstash (pipeline, grok) + Kibana, Beats, index templates, ILM |
| `observability/03-grafana-prometheus.md` | ❌ | PromQL queries, alerting rules, Alertmanager, Grafana dashboards, datasources, provisioning |
| `observability/04-opentelemetry.md` | ❌ | OTel SDK (traces/metrics/logs), Collector, auto-instrumentation, OTLP export, context propagation |
| `observability/05-datadog.md` | ❌ | APM, Infrastructure metrics, Log management, Synthetic tests, Monitors, Dashboards |
| `observability/06-distributed-tracing.md` | ❌ | Jaeger, Zipkin, trace context (W3C TraceContext), sampling strategies (head/tail), span relationships |

### SRE & Reliability
| File | ST | Chủ đề chính |
|---|---|---|
| `sre/01-sre-practices.md` | 🚧 | SLI/SLO/SLA, error budgets, toil, blameless postmortem, on-call rotation, runbooks |
| `sre/02-incident-management.md` | ❌ | Severity levels, incident commander, communication templates, postmortem process, action items |
| `sre/03-chaos-engineering.md` | ❌ | Chaos Monkey, Gremlin, failure injection, game days, blast radius, hypothesis-driven |
| `sre/04-capacity-planning.md` | ❌ | Demand forecasting, resource headroom, load testing for capacity, auto-scaling policies |
| `sre/05-high-availability.md` | ❌ | Multi-AZ deployment, active-active vs active-passive, disaster recovery (RTO/RPO), backup strategies |

### Secret & Config Management
| File | ST | Chủ đề chính |
|---|---|---|
| `secrets/01-vault.md` | ❌ | HashiCorp Vault: dynamic secrets, KV store, transit encryption, PKI, auth methods, leases |
| `secrets/02-cloud-secrets.md` | ❌ | AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, rotation, IAM integration |
| `secrets/03-env-config-management.md` | ❌ | .env files, 12-factor app config, Config maps, environment-specific configs, secret injection |

---

## 10 — Cloud

| File | ST | Chủ đề chính |
|---|---|---|
| `01-cloud-overview.md` | ✅ | AWS vs Azure vs GCP comparison, shared responsibility model, billing, managed services overview |
| `aws/01-aws-core.md` | ❌ | EC2 (instance types, AMI, ASG), S3 (storage classes, lifecycle, presigned URLs), RDS, IAM (policies/roles) |
| `aws/02-aws-networking.md` | ❌ | VPC, subnets (public/private), Route Tables, NAT GW, ALB/NLB, Route53, CloudFront, Transit Gateway |
| `aws/03-aws-serverless.md` | ❌ | Lambda (triggers, layers, cold start), API Gateway, SQS, SNS, EventBridge, Step Functions |
| `aws/04-aws-containers.md` | ❌ | ECS (Fargate vs EC2), EKS, ECR, App Runner, Copilot CLI |
| `aws/05-aws-data.md` | ❌ | Redshift, Glue (ETL), Athena (S3 queries), Lake Formation, Kinesis, MSK (Kafka managed) |
| `azure/01-azure-core.md` | ❌ | Virtual Machines, Blob Storage, Azure SQL, Entra ID (AAD), RBAC, subscriptions, resource groups |
| `azure/02-azure-networking.md` | ❌ | VNet, NSG, Application Gateway, Azure Front Door, Private Link, VPN Gateway |
| `azure/03-azure-serverless.md` | ❌ | Azure Functions, Service Bus, Event Grid, Logic Apps, Durable Functions |
| `azure/04-azure-containers.md` | ❌ | AKS, ACR, Azure Container Apps, Container Instances |
| `azure/05-azure-data.md` | ❌ | Synapse Analytics, Data Factory, Cosmos DB (multi-model, global distribution), Azure Databricks |
| `gcp/01-gcp-core.md` | ❌ | Compute Engine, GCS, Cloud SQL, IAM, projects/folders/org structure |
| `gcp/02-gcp-serverless.md` | ❌ | Cloud Run, Cloud Functions, App Engine, Pub/Sub, Cloud Tasks |
| `gcp/03-gcp-data.md` | ❌ | BigQuery (SQL analytics, partitioning, clustering), Dataflow (Beam), Pub/Sub, Looker Studio |
| `cloudflare/01-cloudflare.md` | ❌ | DNS, CDN, WAF, Workers (edge JS), R2 (S3-compatible), Pages, Tunnel (zero-trust), D1 (SQLite at edge) |
| `serverless/01-serverless-concepts.md` | ❌ | FaaS concepts, cold start, stateless design, event-driven, costs vs containers, limitations |
| `finops/01-cloud-cost-optimization.md` | ❌ | Reserved instances, Savings Plans, Spot/Preemptible, right-sizing, cost allocation tags, finops principles |
| `multi-cloud/01-multi-cloud-strategy.md` | ❌ | Vendor lock-in risks, abstraction layers (Pulumi/Terraform), data portability, network latency, cost comparison |

---

## 11 — Architecture & System Design

### System Design
| File | ST | Chủ đề chính |
|---|---|---|
| `system-design/01-system-design.md` | ✅ | Requirements, scale estimation, API design, HLD, deep dives, trade-offs, RESHADED framework |
| `system-design/02-case-studies.md` | ❌ | URL Shortener, Twitter feed, YouTube, Uber, WhatsApp, Google Docs, Notification system |
| `system-design/03-scalability.md` | ❌ | Horizontal vs vertical, sharding strategies, CAP theorem, PACELC, eventual consistency, 2-phase commit |
| `system-design/04-numbers.md` | ❌ | Latency numbers (L1 cache → disk → network), throughput, storage estimation cheat sheet |
| `system-design/05-distributed-systems.md` | ❌ | Vector clocks, Paxos/Raft consensus, distributed transactions (2PC/3PC/Saga), CRDTs, coordination (ZooKeeper) |

### Software Architecture
| File | ST | Chủ đề chính |
|---|---|---|
| `design-patterns/01-gof-patterns.md` | ✅ | Creational (Factory/Singleton/Builder), Structural (Adapter/Decorator/Proxy), Behavioral (Observer/Strategy/Command) |
| `design-patterns/02-enterprise-patterns.md` | ❌ | Repository, Unit of Work, CQRS, Saga, Outbox, Circuit Breaker, Bulkhead |
| `clean-architecture/01-clean-architecture.md` | 🚧 | Dependency rule, Entities, Use Cases, Interface Adapters, Frameworks layer, Repository pattern |
| `clean-architecture/02-hexagonal.md` | ❌ | Ports & Adapters, Application core, Primary/Secondary adapters, testing benefits |
| `ddd/01-domain-driven-design.md` | ❌ | Bounded contexts, Context maps, Ubiquitous language, Strategic design |
| `ddd/02-ddd-tactical.md` | ❌ | Entities, Value Objects, Aggregates, Domain Events, Domain Services, Application Services |

### Microservices
| File | ST | Chủ đề chính |
|---|---|---|
| `microservices/01-microservices-patterns.md` | 🚧 | Decomposition, database per service, CQRS, Event Sourcing, Saga, Circuit Breaker, BFF, Strangler Fig |
| `microservices/02-event-driven-architecture.md` | 🚧 | Events vs Commands, choreography vs orchestration, Outbox/Inbox patterns, CloudEvents, Transactional outbox |
| `microservices/03-api-gateway.md` | ❌ | Gateway responsibilities, Kong, Traefik, AWS API GW, rate limit, auth, request transform |
| `microservices/04-service-mesh.md` | ❌ | Istio (sidecar, VirtualService, DestinationRule), Linkerd, mTLS, traffic management, observability |

---

## 12 — Security

| File | ST | Chủ đề chính |
|---|---|---|
| `01-web-security-fundamentals.md` | ✅ | OWASP Top 10 (SQLi, XSS, CSRF, IDOR, SSRF), security headers, input validation, CSP |
| `02-authentication.md` | ✅ | JWT (header/payload/signature), OAuth 2.0 flows, OIDC, sessions vs tokens, RBAC, MFA, passkeys |
| `encryption/01-encryption-basics.md` | 🚧 | AES-256-GCM, RSA/ECC, key exchange (ECDH), digital signatures (Ed25519), envelope encryption, KMS |
| `encryption/02-hashing.md` | ❌ | bcrypt, Argon2id, scrypt (password), SHA-256/SHA-3 (data integrity), HMAC, rainbow tables |
| `encryption/03-pki-certificates.md` | ❌ | X.509 structure, certificate chain, CSR generation, CA types, Let's Encrypt + ACME, cert pinning |
| `authorization/01-rbac-abac.md` | ❌ | RBAC (roles/permissions), ABAC (policy), ReBAC (relationship-based), permission matrix design |
| `authorization/02-casbin-opa.md` | ❌ | Casbin policy models (ACL/RBAC/ABAC), OPA (Rego language), policy as code, integration |
| `authorization/03-oauth-deep-dive.md` | ❌ | OAuth 2.0 Authorization Code + PKCE (SPA), Client Credentials (M2M), Device Flow, Token introspection, refresh |
| `database-security/01-db-security.md` | ❌ | SQL injection prevention (parameterized queries), least-privilege DB users, audit logging, encryption at rest |
| `devsecops/01-sast-dast.md` | ❌ | SAST (Semgrep, SonarQube), DAST (OWASP ZAP, Burp), IAST, secret scanning (Trufflehog, GitGuardian) |
| `devsecops/02-supply-chain.md` | ❌ | SCA (dependency vulnerabilities), SBOM (CycloneDX/SPDX), Sigstore (cosign), SLSA framework |
| `network-security/01-firewall-waf.md` | ❌ | Stateful firewall, WAF rules, Cloudflare WAF, AWS WAF, rate limiting at network layer |
| `network-security/02-ddos-protection.md` | ❌ | DDoS types (volumetric/protocol/application), mitigation (anycast, scrubbing, Cloudflare) |
| `compliance/01-gdpr.md` | ❌ | Data subject rights, lawful basis, DPA, consent management, right to erasure, cross-border transfer |
| `compliance/02-soc2-pci-hipaa.md` | ❌ | SOC 2 (TSC criteria), PCI-DSS (card data scope), HIPAA (PHI), ISO 27001 controls |
| `pentest/01-pentest-basics.md` | ❌ | Recon, scanning, exploitation, post-exploitation, OWASP testing guide, Burp Suite, sqlmap |

---

## 13 — Testing & QA

| File | ST | Chủ đề chính |
|---|---|---|
| `01-testing-fundamentals.md` | ✅ | Testing pyramid, unit/integration/E2E, TDD, coverage, mocking vs stubbing vs faking |
| `unit-testing/01-pytest.md` | ❌ | Fixtures (scope), parametrize, marks, conftest.py, monkeypatch, coverage.py, hypothesis |
| `unit-testing/02-jest-vitest.md` | ❌ | describe/it/expect, vi.mock, vi.fn, spyOn, async tests, jsdom, coverage (c8) |
| `integration-testing/01-api-testing.md` | ❌ | Supertest (Node), httpx (Python), test DB setup/teardown, factory pattern, auth helpers |
| `integration-testing/02-testcontainers.md` | ❌ | Spin up real DB/Redis/Kafka in Docker for tests, Java/Go/Python SDKs |
| `e2e-testing/01-playwright.md` | ❌ | Page Object Model, locators, fixtures, network mocking (page.route), CI video recording |
| `e2e-testing/02-cypress.md` | ❌ | cy commands, cy.intercept, custom commands, component testing, Cypress Cloud |
| `performance-testing/01-k6.md` | ❌ | Scenarios, VUs, ramping, thresholds, checks, k6 Cloud, browser testing |
| `performance-testing/02-locust.md` | ❌ | User classes, task sets, spawn rate, distributed load, events API |
| `security-testing/01-owasp-zap.md` | ❌ | Automated scan, active vs passive, API scan, ZAP in CI, managing false positives |
| `methodologies/01-tdd.md` | ❌ | Red-Green-Refactor, outside-in vs inside-out TDD, design benefits, when NOT to TDD |
| `methodologies/02-bdd.md` | ❌ | Gherkin (Given/When/Then), Cucumber/Behave, living documentation, acceptance tests |
| `methodologies/03-mutation-testing.md` | ❌ | Mutation operators, Mutmut (Python), Stryker (JS), mutation score, test quality metric |
| `methodologies/04-property-based.md` | ❌ | Property-based testing, Hypothesis (Python), fast-check (JS), shrinking, generators |
| `contract-testing/01-pact.md` | ❌ | Consumer-driven contracts, Pact broker, provider verification, pact file format |
| `code-quality/01-code-quality-metrics.md` | ❌ | Cyclomatic complexity, cognitive complexity, tech debt, code smells, SonarQube quality gates, test coverage |

---

## 14 — AI / Machine Learning

### Foundations
| File | ST | Chủ đề chính |
|---|---|---|
| `01-ml-fundamentals.md` | ✅ | Supervised/Unsupervised/RL, Scikit-learn (pipelines), metrics (accuracy/F1/AUC/RMSE) |
| `02-numpy-pandas.md` | ✅ | NumPy arrays (broadcasting, slicing), Pandas (DataFrame, groupby, merge, pivot, time series) |
| `03-data-visualization.md` | ❌ | Matplotlib (figures/axes), Seaborn, Plotly (interactive), Altair, dashboard basics |
| `04-math-for-ml.md` | ❌ | Linear algebra (matrix ops, SVD), Calculus (gradient, chain rule), Probability (Bayes, distributions) |
| `05-scikit-learn-deep.md` | ❌ | Pipeline, ColumnTransformer, cross-validation, GridSearchCV/Optuna, feature importance, model persistence |
| `06-computer-vision.md` | ❌ | OpenCV basics (read/write/transform/draw), image preprocessing, contours, YOLO inference, PIL/Pillow |

### Deep Learning
| File | ST | Chủ đề chính |
|---|---|---|
| `deep-learning/01-neural-networks.md` | ❌ | Perceptron, backpropagation, activation functions, layers, overfitting (dropout/batchnorm), optimizers |
| `deep-learning/02-cnn.md` | ❌ | Convolution, pooling, architectures (VGG/ResNet/EfficientNet), transfer learning, object detection (YOLO) |
| `deep-learning/03-transformers.md` | ❌ | Attention mechanism (Q/K/V), positional encoding, BERT vs GPT architecture, fine-tuning |
| `deep-learning/04-pytorch.md` | ❌ | Tensors, autograd, nn.Module, training loop, DataLoader, torchvision, Lightning |

### LLMs & GenAI
| File | ST | Chủ đề chính |
|---|---|---|
| `llm/01-prompt-engineering.md` | 🚧 | Zero/Few-shot, Chain-of-Thought, ReAct, system prompts, JSON mode, sampling params, prompt injection |
| `llm/02-rag-langchain.md` | 🚧 | RAG pipeline, LangChain LCEL, LlamaIndex, reranking, RAGAS evaluation |
| `llm/03-fine-tuning.md` | ❌ | Full fine-tuning vs LoRA vs QLoRA, instruction tuning, PEFT, Unsloth, training data format |
| `llm/04-ai-agents.md` | ❌ | Tool use, ReAct agent, LangGraph (stateful graph), CrewAI (multi-agent), memory types |
| `llm/05-llm-evaluation.md` | ❌ | RAGAS metrics (faithfulness/relevancy/recall), LLM-as-judge, human eval, benchmark datasets |
| `llm/06-llm-inference.md` | ❌ | vLLM, Ollama, TGI, quantization (GGUF/AWQ/GPTQ), batching, KV cache |

### MLOps
| File | ST | Chủ đề chính |
|---|---|---|
| `mlops/01-mlops-basics.md` | ❌ | ML lifecycle, MLflow (tracking/registry), Weights & Biases, DVC (data versioning) |
| `mlops/02-model-serving.md` | ❌ | BentoML, Triton Inference Server, TorchServe, FastAPI for models, A/B testing models |
| `mlops/03-feature-store.md` | ❌ | Feast, Tecton, offline vs online features, point-in-time correct joins, feature reuse |

---

## 15 — Data Engineering

| File | ST | Chủ đề chính |
|---|---|---|
| `01-data-eng-overview.md` | ❌ | Data engineer vs analyst vs scientist, modern data stack, Lambda/Kappa architecture |
| `etl/01-etl-elt.md` | ❌ | ETL vs ELT, extract (APIs/DB/files), transform (cleaning/aggregation), load, CDC |
| `orchestration/01-airflow.md` | ❌ | DAGs, operators (Python/Bash/SQL), hooks, XComs, sensors, dynamic DAGs, TaskFlow API |
| `orchestration/02-prefect.md` | ❌ | Flows, tasks, deployments, work pools, artifacts, caching, retries, Prefect Cloud |
| `transformation/01-dbt.md` | ❌ | Models (ref/source), materializations (table/view/incremental), tests, docs, seeds, snapshots |
| `processing/01-spark-pyspark.md` | ❌ | RDD vs DataFrame, transformations vs actions, Spark SQL, partitioning, broadcast join, Catalyst |
| `streaming/01-kafka-streaming.md` | ❌ | Kafka Streams API, KTable/KStream, windowing, exactly-once, consumer groups |
| `streaming/02-flink.md` | ❌ | DataStream API, Table API, watermarks, windows (tumbling/sliding/session), checkpoints |
| `storage/01-data-warehouse.md` | ❌ | Columnar storage, Snowflake, BigQuery (slots/partitioning/clustering), Redshift distribution |
| `storage/02-data-lake.md` | ❌ | Delta Lake (ACID on Parquet), Apache Iceberg, Hudi, schema evolution, time travel |
| `quality/01-great-expectations.md` | ❌ | Expectations (expect_column_*), data docs, checkpoints, integrating into pipelines |
| `ingestion/01-fivetran-airbyte.md` | ❌ | Managed ELT, connectors, incremental sync, CDC, custom connectors, Airbyte vs Fivetran |

---

## 16 — Mobile Development

| File | ST | Chủ đề chính |
|---|---|---|
| `react-native/01-react-native-basics.md` | 🚧 | Core components, StyleSheet, React Navigation, state (Zustand+RQ), native APIs, Expo vs bare |
| `react-native/02-expo.md` | ❌ | EAS Build, EAS Update (OTA), expo-modules, config plugins, managed vs bare workflow |
| `flutter/01-flutter-basics.md` | 🚧 | Widget tree, Stateless/Stateful, Layout, Riverpod state, go_router, dio, platform channels |
| `flutter/02-dart-basics.md` | ❌ | Dart null safety, Future/Stream/async, isolates, classes, mixins, generics |
| `ios/01-swift-basics.md` | 🚧 | Optionals, protocols, closures, Combine, Swift concurrency, UIKit basics, Instruments |
| `ios/02-swiftui.md` | ❌ | Views, State/Binding/ObservableObject, NavigationStack, animations, previews, SwiftData |
| `android/01-kotlin-android.md` | 🚧 | Activity/Fragment lifecycle, ViewModel, LiveData/StateFlow, Room, Retrofit, Hilt |
| `android/02-jetpack-compose.md` | ❌ | Composables, State hoisting, LazyColumn, Navigation, Modifier, theming (Material 3) |
| `cross-platform/01-comparison.md` | ❌ | RN vs Flutter vs Native vs KMP — performance, DX, ecosystem, decision matrix |
| `mobile-devops/01-fastlane.md` | ❌ | Lanes, actions (gym/pilot/deliver), automatic code signing, screenshots automation |
| `mobile-devops/02-app-store-deploy.md` | ❌ | App Store Connect, Google Play Console, release tracks, metadata, TestFlight, review process |
| `mobile/01-push-notifications.md` | ❌ | APNs (iOS), FCM (Android/iOS), deep linking (Universal Links/App Links), notification payload, local notif |

---

## 17 — Game Development

| File | ST | Chủ đề chính |
|---|---|---|
| `unity/01-unity-basics.md` | ❌ | GameObjects, Components, Update loop, Physics, Animator, UI system, ScriptableObject, C# in Unity |
| `unreal/01-unreal-basics.md` | ❌ | Blueprints, C++ UObject, Actors, components, level design, Niagara particles, Lumen/Nanite |
| `godot/01-godot-basics.md` | ❌ | Nodes/Scenes, GDScript, signals, physics (CharacterBody2D/3D), UI (Control nodes), exports |
| `web-game/01-threejs.md` | ❌ | Scene/Camera/Renderer, Meshes, Lights, Animation, GLTF loading, React Three Fiber |
| `web-game/02-phaser.md` | ❌ | Scenes (preload/create/update), Arcade Physics, Tilemaps, sprites, input, sound |
| `concepts/01-game-loop.md` | ❌ | Fixed vs variable timestep, delta time, update/render separation, game state machine |
| `concepts/02-physics-collision.md` | ❌ | AABB, SAT, collision layers, rigidbody, trigger vs collider, determinism |
| `concepts/03-networking-multiplayer.md` | ❌ | Client-server vs P2P, lag compensation, rollback netcode, tick rate, dedicated server (Photon/Nakama) |

---

## 18 — Blockchain & Web3

| File | ST | Chủ đề chính |
|---|---|---|
| `01-blockchain-basics.md` | ❌ | Consensus (PoW/PoS/dPoS), hash chaining, Merkle trees, wallets, public/private keys, UTXO vs Account |
| `ethereum/01-solidity-basics.md` | ❌ | Contract syntax, types, mappings, events, modifiers, inheritance, ABI, deployment |
| `ethereum/02-smart-contracts.md` | ❌ | ERC-20/721/1155 standards, security (reentrancy, overflow), testing (Hardhat/Foundry), audit |
| `web3/01-web3js-ethers.md` | ❌ | Provider, Signer, Contract interaction, event listening, wallet connection (MetaMask/WalletConnect) |
| `defi/01-defi-concepts.md` | ❌ | AMM (Uniswap), liquidity pools, yield farming, lending protocols (Aave), stablecoins, MEV |

---

## 19 — Embedded & IoT

| File | ST | Chủ đề chính |
|---|---|---|
| `embedded/01-microcontrollers.md` | ❌ | Arduino IDE, ESP32 (WiFi/BT), STM32 (HAL), GPIO, ADC, PWM, I2C/SPI/UART |
| `embedded/02-rtos.md` | ❌ | FreeRTOS tasks, queues, semaphores, mutexes, timers, memory management, porting |
| `embedded/03-linux-embedded.md` | ❌ | Yocto (recipes/layers/BitBake), Buildroot, cross-compilation, device tree, U-Boot |
| `iot/01-mqtt.md` | ❌ | Publish/Subscribe, topics, QoS levels (0/1/2), MQTT broker (Mosquitto, EMQX), TLS |
| `iot/02-iot-platforms.md` | ❌ | AWS IoT Core, Azure IoT Hub, device shadows, MQTT bridge, time series storage |
| `systems/01-linux-kernel.md` | ❌ | Kernel architecture, system calls, kernel modules, /proc, memory subsystem, CFS scheduler |
| `systems/02-device-drivers.md` | ❌ | Character vs block drivers, file_operations struct, kernel space I/O, interrupts, DMA |

---

## 20 — Developer Tools & Productivity

| File | ST | Chủ đề chính |
|---|---|---|
| `01-developer-tools.md` | ✅ | VS Code extensions, terminal setup, Git config, dotfiles, debug config, productivity shortcuts |
| `02-testing.md` | ✅ | Testing pyramid overview — unit/integration/E2E giải thích sơ bộ |
| `editors/01-vscode-advanced.md` | ❌ | Multi-cursor, tasks, launch configs (debug), extensions (ESLint/Prettier/Vim), workspace settings |
| `editors/02-vim-neovim.md` | ❌ | Vim motions mastery, Neovim config (Lua), LSP setup, Telescope, lazy.nvim, Oil.nvim |
| `editors/03-jetbrains.md` | ❌ | Refactoring (Rename/Extract), live templates, run configs, built-in Git, database tools |
| `api-clients/01-postman.md` | ❌ | Collections, environments, pre-request scripts, test scripts, mock servers, Newman CLI |
| `api-clients/02-bruno-httpie.md` | ❌ | Bruno (git-friendly, local), HTTPie (CLI), curl one-liners, Insomnia |
| `databases/01-dbeaver-tableplus.md` | ❌ | DB connection management, SQL editor, ER diagram, data export, query explain visualization |
| `ai-tools/01-github-copilot.md` | ❌ | Autocomplete, chat, CLI, workspace context, Copilot Instructions, privacy/enterprise options |
| `ai-tools/02-cursor-windsurf.md` | ❌ | AI-first editors, inline edit (Cmd+K), codebase chat, rules for AI, MCP integration |
| `monitoring/01-datadog-newrelic.md` | ❌ | APM traces, infrastructure metrics, custom dashboards, alerts, log management |
| `documentation/01-mkdocs-docusaurus.md` | ❌ | MkDocs (Material theme), Docusaurus 3 (MDX, versioning, search), auto-deploy to GH Pages |
| `makefile/01-makefile.md` | ❌ | Targets, prerequisites, variables, PHONY, pattern rules, automatic variables ($@, $<) |

---

## 21 — Soft Skills & Career

| File | ST | Chủ đề chính |
|---|---|---|
| `01-soft-skills.md` | ✅ | Code review etiquette, Clean Code, Agile/Scrum, communication, estimation, pair programming |
| `02-technical-writing.md` | 🚧 | README structure, ADR, RFC, Runbook, Postmortem, API docs, Mermaid/C4 diagrams |
| `03-system-design-interviews.md` | 🚧 | RESHADED framework, requirements, estimation, API design, HLD, deep dives, common questions |
| `04-coding-interviews.md` | 🚧 | UMPIRE, think-out-loud, edge cases, complexity analysis, Blind 75, NeetCode 150, mock interviews |
| `05-code-review.md` | ❌ | PR description template, review checklist, constructive feedback, reviewer vs author mindset |
| `06-estimating.md` | ❌ | Story points, t-shirt sizing, three-point estimation, planning poker, velocity, planning fallacy |
| `07-mentoring.md` | ❌ | 1-on-1 structure, giving feedback (SBI model), career ladders, growth conversations, delegation |
| `08-open-source.md` | ❌ | Finding projects, first contribution, writing good PRs, issue triage, becoming a maintainer |
| `09-freelancing.md` | ❌ | Proposals, portfolio, pricing (hourly vs project), contracts (IP/NDA), client management |
| `10-salary-negotiation.md` | ❌ | Market research, BATNA, offer negotiation, equity (RSU/Options/Cliff/Vesting), remote premium |

---

## Tóm tắt

| # | Phần | Tổng | ✅ | 🚧 | ❌ |
|---|---|---|---|---|---|
| 00 | Roadmaps | 13 | 7 | 0 | 6 |
| 01 | CS Fundamentals | 23 | 1 | 8 | 14 |
| 02 | Version Control | 4 | 1 | 2 | 1 |
| 03 | Terminal & OS | 9 | 2 | 3 | 4 |
| 04 | Networking | 12 | 2 | 3 | 7 |
| 05 | Languages | 33 | 5 | 9 | 19 |
| 06 | Frontend | 46 | 5 | 10 | 31 |
| 07 | Backend | 29 | 5 | 6 | 18 |
| 08 | Databases | 29 | 4 | 5 | 20 |
| 09 | DevOps | 36 | 5 | 5 | 26 |
| 10 | Cloud | 18 | 1 | 0 | 17 |
| 11 | Architecture | 16 | 2 | 5 | 9 |
| 12 | Security | 16 | 2 | 1 | 13 |
| 13 | Testing & QA | 16 | 1 | 0 | 15 |
| 14 | AI/ML | 19 | 2 | 2 | 15 |
| 15 | Data Engineering | 12 | 0 | 0 | 12 |
| 16 | Mobile | 12 | 0 | 5 | 7 |
| 17 | Game Dev | 8 | 0 | 0 | 8 |
| 18 | Blockchain | 5 | 0 | 0 | 5 |
| 19 | Embedded/IoT | 7 | 0 | 0 | 7 |
| 20 | Tools | 13 | 2 | 0 | 11 |
| 21 | Soft Skills | 10 | 1 | 3 | 6 |
| **TỔNG** | | **396** | **48** | **67** | **281** |

> **48 bài đầy đủ | 67 stubs (có skeleton) | 281 cần tạo** — tổng **396 files**
>
> 🎯 **Mức độ bao phủ: ~98% kiến thức dev thế giới** — bao gồm mọi domain từ Web, Mobile, DevOps, Cloud, AI/ML, Security, Embedded, Game Dev, Blockchain đến Soft Skills.
>
> 📌 **Ưu tiên viết nội dung:** CS Fundamentals → Backend → Frontend → DevOps → Cloud → Architecture → Security → AI/ML → Specialized
