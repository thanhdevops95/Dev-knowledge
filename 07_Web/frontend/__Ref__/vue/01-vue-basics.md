# 💚 Vue.js 3 — Framework giao diện linh hoạt

> `[BEGINNER → INTERMEDIATE]` — Dễ học, tài liệu tiếng Việt tốt

---

## Tại sao dùng Vue?

- **Dễ học nhất** trong các framework lớn (React, Angular, Vue)
- **Composition API** — Tổ chức code theo tính năng, không theo lifecycle
- **Reactivity system** tự động, không cần boilerplate
- **File `.vue`** — Template, Script, Style trong 1 file
- **Nuxt.js** — Full-stack framework dựa trên Vue (như Next.js với React)

---

## Setup

```bash
# Tạo project mới
npm create vite@latest my-vue-app -- --template vue-ts
cd my-vue-app
npm install
npm run dev
```

---

## Single File Component (SFC)

```vue
<!-- src/components/UserCard.vue -->
<template>
  <div class="user-card" :class="{ active: isActive }">
    <img :src="user.avatar" :alt="user.name" />
    <h2>{{ user.name }}</h2>
    <p>{{ user.bio }}</p>
    <button @click="toggleActive">
      {{ isActive ? 'Đang theo dõi' : 'Theo dõi' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// Props
const props = defineProps<{
  user: {
    name: string
    bio: string
    avatar: string
  }
}>()

// Emit
const emit = defineEmits<{
  follow: [userId: string]
}>()

// State
const isActive = ref(false)

// Methods
function toggleActive() {
  isActive.value = !isActive.value
  if (isActive.value) {
    emit('follow', props.user.name)
  }
}
</script>

<style scoped>
.user-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
}

.user-card.active {
  border-color: #48bb78;
}
</style>
```

---

## Reactivity — ref và reactive

```typescript
import { ref, reactive, computed, watch, watchEffect } from 'vue'

// ref — cho primitive values (number, string, boolean)
const count = ref(0)
const name = ref('Jesse')
count.value++                // Phải dùng .value trong script
// Trong template: {{ count }} (không cần .value)

// reactive — cho objects
const state = reactive({
  user: null as User | null,
  loading: false,
  error: ''
})
state.loading = true          // Không cần .value

// computed — tính toán từ state khác, cache result
const fullName = computed(() => `${firstName.value} ${lastName.value}`)
const doubleCount = computed(() => count.value * 2)

// watch — theo dõi thay đổi
watch(count, (newVal, oldVal) => {
  console.log(`Count: ${oldVal} → ${newVal}`)
})

watch(() => state.user, (user) => {
  if (user) fetchUserPosts(user.id)
}, { immediate: true })

// watchEffect — tự detect dependencies
watchEffect(() => {
  console.log(`Count is now: ${count.value}`)
  // Tự động re-run khi count.value thay đổi
})
```

---

## Template Syntax

```vue
<template>
  <!-- v-bind: rút gọn là : -->
  <img :src="imageUrl" :alt="description" />
  <button :disabled="isLoading">Submit</button>

  <!-- v-on: rút gọn là @ -->
  <button @click="handleClick">Click me</button>
  <input @input="handleInput" @keyup.enter="submit" />

  <!-- v-model: two-way binding -->
  <input v-model="searchQuery" placeholder="Tìm kiếm..." />
  <input v-model.number="age" type="number" />
  <input v-model.trim="username" />

  <!-- v-if / v-else-if / v-else -->
  <div v-if="status === 'loading'">Đang tải...</div>
  <div v-else-if="status === 'error'">Lỗi: {{ error }}</div>
  <div v-else>{{ data }}</div>

  <!-- v-show — toggle display, không remove DOM -->
  <Tooltip v-show="isHovered" />

  <!-- v-for — lặp -->
  <ul>
    <li v-for="post in posts" :key="post.id">
      {{ post.title }}
    </li>
  </ul>

  <!-- v-for với index -->
  <div v-for="(item, index) in items" :key="item.id">
    {{ index + 1 }}. {{ item.name }}
  </div>

  <!-- Slots -->
  <BaseModal>
    <template #header>
      <h2>Tiêu đề</h2>
    </template>
    <p>Nội dung modal...</p>
    <template #footer>
      <button @click="close">Đóng</button>
    </template>
  </BaseModal>
</template>
```

---

## Lifecycle Hooks

```typescript
import {
  onMounted,
  onUpdated,
  onUnmounted,
  onBeforeMount,
  onBeforeUpdate,
  onBeforeUnmount
} from 'vue'

// Tương đương:
// onMounted      → componentDidMount
// onUpdated      → componentDidUpdate
// onUnmounted    → componentWillUnmount

onMounted(() => {
  // DOM đã render, có thể thao tác DOM
  fetchData()
  initChart()
})

onUnmounted(() => {
  // Cleanup: clear timers, remove event listeners
  clearInterval(timer)
  window.removeEventListener('resize', handleResize)
})
```

---

## Composables — Tái sử dụng logic (như Custom Hooks)

```typescript
// composables/useFetch.ts
import { ref, type Ref } from 'vue'

interface UseFetchResult<T> {
  data: Ref<T | null>
  loading: Ref<boolean>
  error: Ref<string | null>
  refresh: () => Promise<void>
}

export function useFetch<T>(url: string): UseFetchResult<T> {
  const data = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchData() {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(url)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      data.value = await res.json()
    } catch (e) {
      error.value = e instanceof Error ? e.message : 'Lỗi không xác định'
    } finally {
      loading.value = false
    }
  }

  fetchData()

  return { data, loading, error, refresh: fetchData }
}
```

```typescript
// composables/useLocalStorage.ts
import { ref, watch } from 'vue'

export function useLocalStorage<T>(key: string, defaultValue: T) {
  const stored = localStorage.getItem(key)
  const value = ref<T>(stored ? JSON.parse(stored) : defaultValue)

  watch(value, (newVal) => {
    localStorage.setItem(key, JSON.stringify(newVal))
  }, { deep: true })

  return value
}
```

```vue
<!-- Dùng composables trong component -->
<script setup lang="ts">
import { useFetch } from '@/composables/useFetch'
import { useLocalStorage } from '@/composables/useLocalStorage'

interface Post {
  id: number
  title: string
  body: string
}

const { data: posts, loading, error } = useFetch<Post[]>('/api/posts')
const theme = useLocalStorage<'dark' | 'light'>('theme', 'light')
</script>
```

---

## Pinia — State Management

```bash
npm install pinia
```

```typescript
// stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface User {
  id: string
  name: string
  email: string
  role: 'user' | 'admin'
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)

  const isLoggedIn = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(email: string, password: string) {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    const data = await res.json()
    user.value = data.user
    token.value = data.token
  }

  function logout() {
    user.value = null
    token.value = null
  }

  return { user, token, isLoggedIn, isAdmin, login, logout }
})
```

```vue
<!-- Dùng store -->
<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

async function handleLogin() {
  await auth.login(email.value, password.value)
  router.push('/dashboard')
}
</script>

<template>
  <div v-if="auth.isLoggedIn">
    Xin chào, {{ auth.user?.name }}
  </div>
</template>
```

---

## Vue Router 4

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/dashboard',
      component: () => import('@/views/DashboardView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/users/:id',
      component: () => import('@/views/UserView.vue'),
      props: true  // Truyền params như props
    },
    {
      path: '/:pathMatch(.*)*',
      component: () => import('@/views/NotFoundView.vue')
    }
  ]
})

// Navigation guard
router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return '/login'
  }
})

export default router
```

---

## Vue vs React — So sánh

| | Vue 3 | React |
|---|---|---|
| **Learning curve** | Dễ hơn | Khó hơn |
| **Template** | HTML-based, `.vue` | JSX (JS trong JS) |
| **State** | `ref()`, `reactive()` | `useState()` |
| **Side effects** | `watch()`, `watchEffect()` | `useEffect()` |
| **Reusable logic** | Composables | Custom Hooks |
| **State Management** | Pinia | Zustand/Redux |
| **Full-stack** | Nuxt.js | Next.js |
| **Job market** | Ít hơn | Nhiều hơn |

---

## Bài tập thực hành

- [ ] Tạo component Counter với ref và computed
- [ ] Build Todo App với Pinia store
- [ ] Tạo composable `useDebounce` cho search input
- [ ] Setup Vue Router với authenticated routes

---

## Tài nguyên thêm

- [Vue.js Docs](https://vuejs.org/) — Tài liệu chính thức xuất sắc
- [Pinia Docs](https://pinia.vuejs.org/)
- [Vue Router Docs](https://router.vuejs.org/)
- [VueUse](https://vueuse.org/) — Thư viện composables cực mạnh
- [Nuxt.js](https://nuxt.com/) — Full-stack Vue framework
