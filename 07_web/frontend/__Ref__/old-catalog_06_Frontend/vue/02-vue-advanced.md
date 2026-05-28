# Vue.js Advanced

> **Tags:** `vue` `composition-api` `pinia` `vite` `typescript` `composables`
> **Level:** Intermediate | **Prerequisite:** `vue/01-vue-basics.md`

---

## 1. Composition API — Deep Dive

```vue
<script setup lang="ts">
// <script setup> = most concise Composition API syntax
import { ref, reactive, computed, watch, watchEffect, onMounted, onUnmounted } from 'vue';

// Reactive state
const count = ref(0);           // Wraps primitives (has .value)
const user = reactive({         // For objects (NO .value)
  name: 'Alice',
  email: 'alice@example.com',
  role: 'admin' as 'admin' | 'user',
});

// Computed (cached, only re-evaluates when deps change)
const greeting = computed(() => `Hello, ${user.name}!`);
const isAdmin = computed(() => user.role === 'admin');

// Writable computed
const fullName = computed({
  get: () => `${user.firstName} ${user.lastName}`,
  set: (value: string) => {
    const [first, ...rest] = value.split(' ');
    user.firstName = first;
    user.lastName = rest.join(' ');
  },
});

// watch — explicit, lazy by default
// Watch single ref
watch(count, (newVal, oldVal) => {
  console.log(`Count changed: ${oldVal} → ${newVal}`);
});

// Watch reactive object (deep)
watch(() => user.name, (newName) => {
  console.log('Name changed:', newName);
});

// Watch multiple sources
watch([count, () => user.name], ([newCount, newName], [oldCount, oldName]) => {
  console.log(`Count: ${oldCount}→${newCount}, Name: ${oldName}→${newName}`);
});

// Options
watch(count, callback, {
  immediate: true,   // Run callback immediately on mount
  deep: true,        // Deep watch (objects)
  once: true,        // Run only once
});

// watchEffect — automatic dep tracking (runs immediately)
watchEffect(() => {
  document.title = `${user.name} | My App`;  // Tracks user.name automatically
});

// Lifecycle hooks
onMounted(() => console.log('Component mounted'));
onUnmounted(() => {
  // Cleanup (event listeners, timers, subscriptions)
});

// Props (in <script setup>)
interface Props {
  modelValue: string;         // v-model
  placeholder?: string;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Enter text...',
  disabled: false,
});

// Emits
interface Emits {
  (e: 'update:modelValue', value: string): void;
  (e: 'submit', value: string): void;
}

const emit = defineEmits<Emits>();

// Expose to parent via ref
defineExpose({
  clear: () => { emit('update:modelValue', ''); },
  focus: () => inputRef.value?.focus(),
});
</script>
```

---

## 2. Composables — Reusable Logic

```typescript
// composables/useFetch.ts
export function useFetch<T>(url: MaybeRefOrGetter<string>) {
  const data = ref<T | null>(null);
  const error = ref<Error | null>(null);
  const loading = ref(false);

  const controller = ref<AbortController | null>(null);

  async function fetchData() {
    const resolvedUrl = toValue(url);  // Unwrap ref or getter
    
    // Cancel previous request
    controller.value?.abort();
    controller.value = new AbortController();

    loading.value = true;
    error.value = null;

    try {
      const response = await fetch(resolvedUrl, {
        signal: controller.value.signal,
      });
      
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      data.value = await response.json();
    } catch (e) {
      if (e instanceof Error && e.name !== 'AbortError') {
        error.value = e;
      }
    } finally {
      loading.value = false;
    }
  }

  // Refetch when URL changes
  watch(() => toValue(url), fetchData, { immediate: true });

  onUnmounted(() => controller.value?.abort());

  return { data, error, loading, refetch: fetchData };
}

// composables/useLocalStorage.ts
export function useLocalStorage<T>(key: string, defaultValue: T) {
  const stored = localStorage.getItem(key);
  const initial = stored ? JSON.parse(stored) : defaultValue;
  
  const state = ref<T>(initial);

  watch(state, (value) => {
    localStorage.setItem(key, JSON.stringify(value));
  }, { deep: true });

  return state;
}

// composables/useIntersectionObserver.ts
export function useIntersectionObserver(
  target: Ref<Element | null>,
  callback: IntersectionObserverCallback,
  options?: IntersectionObserverInit
) {
  let observer: IntersectionObserver | null = null;

  const startObserver = () => {
    if (!target.value) return;
    observer = new IntersectionObserver(callback, options);
    observer.observe(target.value);
  };

  const stopObserver = () => observer?.disconnect();

  watch(target, (el) => {
    stopObserver();
    if (el) startObserver();
  }, { immediate: true });

  onUnmounted(stopObserver);

  return { start: startObserver, stop: stopObserver };
}

// Usage
const { data: users, loading } = useFetch<User[]>('/api/users');
const savedTheme = useLocalStorage('theme', 'light');

const cardRef = ref<Element | null>(null);
useIntersectionObserver(cardRef, ([entry]) => {
  if (entry.isIntersecting) showAnimation();
});
```

---

## 3. Pinia — State Management

```typescript
// stores/user.ts
import { defineStore } from 'pinia';

// Option store style
export const useUserStore = defineStore('user', {
  state: (): {
    user: User | null;
    token: string | null;
    loading: boolean;
  } => ({
    user: null,
    token: localStorage.getItem('token'),
    loading: false,
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
    isAdmin: (state) => state.user?.role === 'admin',
    displayName: (state) => state.user?.name ?? 'Guest',
  },
  
  actions: {
    async login(email: string, password: string) {
      this.loading = true;
      try {
        const { user, token } = await authService.login(email, password);
        this.user = user;
        this.token = token;
        localStorage.setItem('token', token);
      } finally {
        this.loading = false;
      }
    },
    
    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('token');
    },
  },
});

// Composition store style (more flexible, recommended)
export const useProductStore = defineStore('products', () => {
  const items = ref<Product[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const total = computed(() => items.value.length);
  const inStock = computed(() => items.value.filter(p => p.stock > 0));

  async function fetchProducts(category?: string) {
    loading.value = true;
    error.value = null;
    try {
      items.value = await api.getProducts(category);
    } catch (e) {
      error.value = 'Failed to load products';
    } finally {
      loading.value = false;
    }
  }

  function addProduct(product: Product) {
    items.value.push(product);
  }

  return { items, loading, error, total, inStock, fetchProducts, addProduct };
});

// Usage in component
const userStore = useUserStore();
const productStore = useProductStore();

// Reactive access to store state
const { user, isAdmin, displayName } = storeToRefs(userStore);  // Maintains reactivity!

// But actions don't need storeToRefs
userStore.login(email, password);
```

### Pinia Plugins
```typescript
// Persist store to localStorage automatically
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

// In store:
export const useUserStore = defineStore('user', {
  state: () => ({ token: null }),
  persist: true,   // Auto-persist entire store
  // or:
  persist: {
    paths: ['token'],   // Only persist specific fields
    storage: sessionStorage,
  },
});
```

---

## 4. Vue Router Advanced

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('@/views/HomeView.vue'),
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('@/views/DashboardView.vue'),
          meta: { requiresAuth: true },   // Custom meta fields
        },
        {
          path: 'admin',
          meta: { requiresAuth: true, role: 'admin' },
          children: [
            {
              path: 'users',
              name: 'admin-users',
              component: () => import('@/views/admin/UsersView.vue'),
            },
          ],
        },
      ],
    },
    {
      path: '/blog/:slug',
      name: 'blog-post',
      component: () => import('@/views/BlogPostView.vue'),
      // Validate param
      beforeEnter: (to) => {
        if (!to.params.slug) return { name: 'blog' };
      },
    },
    {
      path: '/:pathMatch(.*)*',   // Catch-all 404
      name: 'not-found',
      component: () => import('@/views/NotFoundView.vue'),
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition;
    if (to.hash) return { el: to.hash, behavior: 'smooth' };
    return { top: 0 };
  },
});

// Navigation guards
router.beforeEach(async (to) => {
  const userStore = useUserStore();
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } };
  }
  
  if (to.meta.role && userStore.user?.role !== to.meta.role) {
    return { name: 'forbidden' };
  }
});

// Route-level progress indicator
router.beforeEach(() => NProgress.start());
router.afterEach(() => NProgress.done());
```

---

## 5. TypeScript with Vue

```typescript
// types/index.ts
export interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'user';
  createdAt: string;
}

export interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
}

// components/UserCard.vue
<script setup lang="ts">
interface Props {
  user: User;
  showActions?: boolean;
  class?: string;
}

const props = withDefaults(defineProps<Props>(), {
  showActions: true,
});

interface Emits {
  (e: 'edit', user: User): void;
  (e: 'delete', userId: number): void;
}

const emit = defineEmits<Emits>();

// Typed ref
const cardRef = ref<HTMLDivElement | null>(null);

// Typed computed
const userInitials = computed<string>(() => {
  return props.user.name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
});
</script>
```

---

## 6. Performance Optimization

```vue
<script setup>
import { defineAsyncComponent, shallowRef } from 'vue';

// Lazy load heavy components
const HeavyChart = defineAsyncComponent({
  loader: () => import('@/components/HeavyChart.vue'),
  loadingComponent: ChartSkeleton,
  errorComponent: ErrorBoundary,
  delay: 200,      // Show loading after 200ms (avoid flash)
  timeout: 10000,  // Error after 10s
});

// v-memo — memoize part of template (avoid re-rendering when deps unchanged)
</script>

<template>
  <!-- Only re-render when user.id or user.name changes -->
  <div v-memo="[user.id, user.name]">
    <UserCard :user="user" />
  </div>
  
  <!-- v-once — render once, never update -->
  <StaticHeader v-once />
  
  <!-- Virtual scrolling for large lists (vue-virtual-scroller) -->
  <RecycleScroller
    class="scroller"
    :items="largeList"
    :item-size="80"
    key-field="id"
    v-slot="{ item }"
  >
    <div class="row">{{ item.name }}</div>
  </RecycleScroller>
</template>
```

### shallowRef and shallowReactive
```typescript
// Use shallowRef when you have large objects that don't need deep reactivity
const bigData = shallowRef<BigDataObject>({...});  // Only tracks reference change

// Manually trigger update when you mutate internals
bigData.value.nested.property = 'new';
triggerRef(bigData);   // Force update

// shallowReactive: only top-level reactive, nested objects are NOT reactive
const config = shallowReactive({ theme: 'dark', settings: { lang: 'vi' } });
// config.theme = 'light'  → triggers update
// config.settings.lang = 'en'  → does NOT trigger update
```

---

## 7. Teleport & Provide/Inject

```vue
<!-- Teleport content to a different DOM node -->
<template>
  <div class="button-container">
    <button @click="showModal = true">Open Modal</button>
    
    <!-- Teleport modal to body (not inside button-container!) -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-backdrop">
        <div class="modal">
          <h2>Modal Title</h2>
          <button @click="showModal = false">Close</button>
        </div>
      </div>
    </Teleport>
  </div>
</template>
```

```typescript
// Provide/Inject — pass data through component tree without props drilling

// Parent (provide)
const theme = ref<'dark' | 'light'>('dark');
const toggleTheme = () => theme.value = theme.value === 'dark' ? 'light' : 'dark';

provide('theme', { theme, toggleTheme });  // Provide reactive data

// Injection key (type-safe)
const ThemeKey: InjectionKey<{ theme: Ref<string>; toggle: () => void }> = Symbol('theme');
provide(ThemeKey, { theme, toggle: toggleTheme });

// Deep child (inject)
const { theme, toggle } = inject(ThemeKey)!;
// Or with default:
const { theme } = inject('theme', { theme: ref('light') });
```

---

## 8. Custom Directives

```typescript
// directives/vClickOutside.ts
export const vClickOutside = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    el._clickOutsideHandler = (event: Event) => {
      if (!el.contains(event.target as Node)) {
        binding.value(event);
      }
    };
    document.addEventListener('click', el._clickOutsideHandler);
  },
  unmounted(el: HTMLElement) {
    document.removeEventListener('click', el._clickOutsideHandler);
    delete el._clickOutsideHandler;
  },
};

// directives/vIntersect.ts
export const vIntersect = {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) binding.value(entry); },
      { threshold: binding.arg ?? 0.1 }
    );
    observer.observe(el);
    el._intersectObserver = observer;
  },
  unmounted(el: HTMLElement) {
    el._intersectObserver?.disconnect();
  },
};

// Register globally
// main.ts
app.directive('click-outside', vClickOutside);
app.directive('intersect', vIntersect);

// Usage
<div v-click-outside="closeMenu">
  <!-- Dropdown content -->
</div>

<div v-intersect.0.2="animateIn">
  <!-- Animates when 20% visible -->
</div>
```

---

## 9. Testing Vue Components

```typescript
// ProductCard.spec.ts
import { mount } from '@vue/test-utils';
import { createPinia, setActivePinia } from 'pinia';
import ProductCard from './ProductCard.vue';
import { useCartStore } from '@/stores/cart';

describe('ProductCard', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });
  
  const product = {
    id: 1,
    name: 'Widget Pro',
    price: 29.99,
    stock: 5,
  };

  it('renders product name and price', () => {
    const wrapper = mount(ProductCard, {
      props: { product },
    });
    
    expect(wrapper.find('[data-testid="product-name"]').text()).toBe('Widget Pro');
    expect(wrapper.find('[data-testid="product-price"]').text()).toBe('$29.99');
  });

  it('adds product to cart when buy button clicked', async () => {
    const wrapper = mount(ProductCard, { props: { product } });
    const cartStore = useCartStore();
    
    await wrapper.find('[data-testid="add-to-cart"]').trigger('click');
    
    expect(cartStore.items).toHaveLength(1);
    expect(cartStore.items[0].productId).toBe(product.id);
  });

  it('disables buy button when out of stock', () => {
    const outOfStock = { ...product, stock: 0 };
    const wrapper = mount(ProductCard, { props: { product: outOfStock } });
    
    const btn = wrapper.find('[data-testid="add-to-cart"]');
    expect(btn.attributes('disabled')).toBeDefined();
  });
});
```

---

*Tài liệu liên quan: `vue/01-vue-basics.md` | `react/02-react-advanced.md` | `typescript/02-typescript-advanced.md`*
