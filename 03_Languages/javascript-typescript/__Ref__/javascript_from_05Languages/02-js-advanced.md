# JavaScript Advanced

> **Tags:** `javascript` `closures` `prototypes` `event-loop` `proxy` `generators` `this`
> **Level:** Advanced | **Prerequisite:** `javascript/01-js-basics.md`

---

## 1. Execution Context & Scope

```javascript
// Global Execution Context → Function Execution Context → Block Scope

// Hoisting
console.log(x);     // undefined (var hoisted, not value)
console.log(y);     // ReferenceError (let not hoisted to initialisation)
var x = 5;
let y = 10;

// Function hoisting (entire function hoisted)
greet();              // "Hello!" — works before declaration
function greet() { console.log("Hello!"); }

const fn = function() {};   // Not hoisted (variable hoisted, not value)
const arrow = () => {};     // Same

// Scope chain
const outer = 'outer';

function outerFn() {
  const middle = 'middle';
  
  function innerFn() {
    const inner = 'inner';
    console.log(outer);    // ✅ scope chain lookup
    console.log(middle);   // ✅
    console.log(inner);    // ✅
  }
  
  // console.log(inner);  // ❌ ReferenceError
  innerFn();
}

// Temporal Dead Zone (TDZ)
{
  // console.log(a);  // ReferenceError: can't access before initialization
  let a = 1;         // TDZ ends here
}
```

---

## 2. Closures

```javascript
// Closure = function that "remembers" its outer scope
// even after outer function has returned

function makeCounter(initial = 0) {
  let count = initial;   // Closed over
  
  return {
    increment: () => ++count,
    decrement: () => --count,
    reset: () => { count = initial; },
    value: () => count,
  };
}

const counter = makeCounter(10);
counter.increment();  // 11
counter.increment();  // 12
counter.decrement();  // 11
counter.value();      // 11

// Counter is isolated — its count is private!
const counter2 = makeCounter(0);  // Separate count

// Factory functions with closures
function createLogger(prefix) {
  const logs = [];
  
  return {
    log: (msg) => {
      const entry = `[${prefix}] ${new Date().toISOString()}: ${msg}`;
      logs.push(entry);
      console.log(entry);
    },
    getLogs: () => [...logs],    // Return copy to preserve encapsulation
    clear: () => { logs.length = 0; },
  };
}

// Classic closure bug and fix
// Bug:
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);  // 3, 3, 3 (not 0, 1, 2)
}

// Fix 1: use let (block-scoped, new binding per iteration)
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 0);  // 0, 1, 2 ✅
}

// Fix 2: IIFE to capture value
for (var i = 0; i < 3; i++) {
  (function(j) {
    setTimeout(() => console.log(j), 0);  // 0, 1, 2 ✅
  })(i);
}

// Memoization (closure-based caching)
function memoize(fn) {
  const cache = new Map();
  
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const fibonacci = memoize(function fib(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});
```

---

## 3. `this` — 4 Rules

```javascript
// Rule 1: Default binding (strict mode: undefined, non-strict: globalThis)
function showThis() {
  console.log(this);  // window (browser) or global (Node)
}
showThis();

// Rule 2: Implicit binding — left of the dot
const obj = {
  name: 'Alice',
  greet() { console.log(this.name); }
};
obj.greet();  // 'Alice' — obj is this

// Implicit binding LOST when function is extracted!
const greet = obj.greet;
greet();  // undefined (or global in sloppy mode) — no dot = no implicit binding!

// Rule 3: Explicit binding — call/apply/bind
function greet(greeting, punctuation) {
  console.log(`${greeting}, ${this.name}${punctuation}`);
}

const user = { name: 'Bob' };
greet.call(user, 'Hello', '!');      // Hello, Bob!
greet.apply(user, ['Hi', '?']);      // Hi, Bob?
const boundGreet = greet.bind(user); // Returns new function
boundGreet('Hey', '.');              // Hey, Bob.

// Rule 4: new binding
function Person(name) {
  this.name = name;
  // 'new' creates new object, assigns to this, returns automatically
}
const person = new Person('Carol');
console.log(person.name);  // 'Carol'

// ARROW FUNCTIONS: NO own 'this' — lexically inherit from surrounding scope
const timer = {
  count: 0,
  start() {
    setInterval(() => {
      this.count++;  // ✅ 'this' = timer (arrow inherits from start())
    }, 1000);
  },
  startBad() {
    setInterval(function() {
      this.count++;  // ❌ 'this' = window/undefined in strict mode
    }, 1000);
  }
};

// Priority: new > explicit > implicit > default
```

---

## 4. Prototype Chain

```javascript
// Every object has [[Prototype]] (internal link)
// Property lookup: own → [[Prototype]] → [[Prototype]] of [[Prototype]] → null

const animal = {
  breathe() { return 'breathing'; },
  eat() { return 'eating'; },
};

const dog = Object.create(animal);   // dog.[[Prototype]] = animal
dog.bark = function() { return 'woof'; };

dog.bark();     // Own property
dog.breathe();  // Found on animal (prototype chain)

Object.getPrototypeOf(dog) === animal;  // true

// Constructor functions + prototype
function Animal(name) {
  this.name = name;   // Instance property
}

// Shared methods on prototype (not duplicated per instance!)
Animal.prototype.toString = function() {
  return `Animal(${this.name})`;
};
Animal.prototype.describe = function() {
  return `I am ${this.name}`;
};

function Dog(name, breed) {
  Animal.call(this, name);  // Call super
  this.breed = breed;
}

Dog.prototype = Object.create(Animal.prototype);    // Inherit
Dog.prototype.constructor = Dog;                    // Fix constructor
Dog.prototype.bark = function() { return 'woof'; };

const rex = new Dog('Rex', 'Labrador');
rex.describe();   // "I am Rex" (from Animal.prototype)
rex.bark();       // "woof" (from Dog.prototype)
rex instanceof Dog;     // true
rex instanceof Animal;  // true (chain lookup)

// Class syntax = syntactic sugar over prototypes
class AnimalClass {
  #name;   // Private field (ES2022)
  
  constructor(name) {
    this.#name = name;
  }
  
  get name() { return this.#name; }
  
  describe() { return `I am ${this.#name}`; }
  
  static create(name) { return new AnimalClass(name); }
}

class DogClass extends AnimalClass {
  #breed;
  
  constructor(name, breed) {
    super(name);   // Must call before using this
    this.#breed = breed;
  }
  
  bark() { return 'woof'; }
  
  describe() {
    return `${super.describe()}, a ${this.#breed}`;
  }
}
```

---

## 5. Event Loop (Critical!)

```javascript
// JavaScript is single-threaded, but handles async via event loop:
//
// Call Stack → Web APIs (setTimeout, fetch, DOM events)
//           → Microtask Queue (Promises, queueMicrotask)
//           → Macrotask Queue (setTimeout, setInterval, I/O)
//
// Order: Call Stack empties → drain ALL microtasks → next macrotask → drain ALL microtasks → ...

console.log('1');       // Call stack — synchronous

setTimeout(() => {
  console.log('2');     // Macrotask queue
}, 0);

Promise.resolve()
  .then(() => console.log('3'))   // Microtask queue
  .then(() => console.log('4')); // Microtask queue (chained)

queueMicrotask(() => console.log('5'));   // Microtask queue

console.log('6');       // Call stack — synchronous

// Output: 1, 6, 3, 5, 4, 2
// Why: sync (1,6) → microtasks (3,5,4) → macrotask (2)

// Promise internals
console.log('sync 1');
new Promise((resolve) => {
  console.log('executor runs synchronously');
  resolve('value');
}).then(val => console.log('then:', val));
console.log('sync 2');

// Output: sync 1 → executor runs synchronously → sync 2 → then: value

// Starvation bug: long microtask chain blocks macrotasks
function recursivePromise() {
  return Promise.resolve().then(() => recursivePromise());
}
// This starves setTimeout/UI rendering
// Fix: use setTimeout to yield to macrotask queue occasionally
```

---

## 6. WeakMap & WeakSet

```javascript
// WeakMap/WeakSet: keys must be objects, weakly held (no memory leak)

// WeakMap — private data associated with objects
const _privateData = new WeakMap();

class MyClass {
  constructor(secret) {
    _privateData.set(this, { secret, createdAt: Date.now() });
  }
  
  getSecret() {
    return _privateData.get(this).secret;  // Access private data
  }
}

const instance = new MyClass('super-secret');
instance.getSecret();   // 'super-secret'
// When instance is garbage collected, _privateData entry is also collected!
// Regular Map would prevent GC!

// WeakSet — track visited objects without preventing GC
const seen = new WeakSet();

function processOnce(obj) {
  if (seen.has(obj)) return 'already processed';
  seen.add(obj);
  // ... process
  return 'processed';
}

// You CANNOT iterate WeakMap/WeakSet (by design)
// Regular Map/Set: iterable, strong references
// Weak variants: non-iterable, weak references (GC-friendly)
```

---

## 7. Proxy & Reflect

```javascript
// Proxy: intercept and customize operations on objects

// Validation proxy
function createValidated(schema) {
  const target = {};
  
  return new Proxy(target, {
    set(obj, prop, value) {
      if (schema[prop]) {
        const { type, required, min, max } = schema[prop];
        
        if (required && (value === undefined || value === null)) {
          throw new Error(`${prop} is required`);
        }
        if (type && typeof value !== type) {
          throw new TypeError(`${prop} must be ${type}, got ${typeof value}`);
        }
        if (min !== undefined && value < min) {
          throw new RangeError(`${prop} must be >= ${min}`);
        }
        if (max !== undefined && value > max) {
          throw new RangeError(`${prop} must be <= ${max}`);
        }
      }
      
      return Reflect.set(obj, prop, value);  // Default behavior
    },
    
    get(obj, prop) {
      if (!(prop in obj)) {
        console.warn(`Accessing undefined property: ${prop}`);
      }
      return Reflect.get(obj, prop);
    }
  });
}

const user = createValidated({
  name: { type: 'string', required: true },
  age: { type: 'number', min: 0, max: 150 },
});

user.name = 'Alice';  // OK
user.age = 30;        // OK
// user.age = -1;     // RangeError!
// user.name = 42;    // TypeError!

// Observable proxy (Vue 3-like reactivity)
function reactive(target, onChange) {
  return new Proxy(target, {
    set(obj, prop, value) {
      const old = obj[prop];
      const result = Reflect.set(obj, prop, value);
      if (old !== value) onChange(prop, value, old);
      return result;
    }
  });
}

const state = reactive({ count: 0 }, (prop, newVal, oldVal) => {
  console.log(`${prop}: ${oldVal} → ${newVal}`);
});

state.count = 1;  // "count: 0 → 1"
state.count = 5;  // "count: 1 → 5"
```

---

## 8. Generators & Iterators

```javascript
// Generator = function that can pause and resume
function* range(start, end, step = 1) {
  for (let i = start; i <= end; i += step) {
    yield i;   // Pause here, return i
  }
}

// Using generator
for (const n of range(1, 10)) {
  console.log(n);  // 1, 2, 3, ..., 10
}

const nums = [...range(0, 100, 10)];  // [0, 10, 20, ..., 100]

// Infinite generators (lazy evaluation!)
function* naturals() {
  let n = 1;
  while (true) yield n++;
}

function take(n, iterable) {
  const result = [];
  for (const item of iterable) {
    result.push(item);
    if (result.length >= n) break;
  }
  return result;
}

take(5, naturals());  // [1, 2, 3, 4, 5] — only computes as needed

// Generator for async control flow (the precursor to async/await)
function* fetchUser(id) {
  const user = yield fetch(`/api/users/${id}`);   // Pause until Promise resolves
  const orders = yield fetch(`/api/orders?user=${user.id}`);
  return { user, orders };
}

// Custom iterable
class Range {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }
  
  [Symbol.iterator]() {
    let current = this.start;
    const end = this.end;
    
    return {
      next() {
        if (current <= end) {
          return { value: current++, done: false };
        }
        return { value: undefined, done: true };
      }
    };
  }
}

for (const n of new Range(1, 5)) {
  console.log(n);  // 1, 2, 3, 4, 5
}

// Generator composition (yield*)
function* concat(...iterables) {
  for (const iterable of iterables) {
    yield* iterable;   // Delegate to sub-iterator
  }
}

[...concat([1, 2], [3, 4], [5, 6])];  // [1, 2, 3, 4, 5, 6]
```

---

## 9. Async Patterns

```javascript
// Promise combinators
const [user, orders, cart] = await Promise.all([
  fetchUser(id),
  fetchOrders(id),
  fetchCart(id),
]);  // All parallel, fails on first rejection

const result = await Promise.allSettled([apiCall1(), apiCall2()]);
result.forEach(r => {
  if (r.status === 'fulfilled') processResult(r.value);
  else handleError(r.reason);
});

const fastest = await Promise.race([apiCall(), timeout(5000)]);
const firstSuccess = await Promise.any([api1(), api2(), api3()]);  // First fulfilled

// Async iteration (for await...of)
async function* paginatedFetch(url) {
  let nextUrl = url;
  while (nextUrl) {
    const response = await fetch(nextUrl);
    const data = await response.json();
    yield* data.items;
    nextUrl = data.nextPageUrl;
  }
}

for await (const item of paginatedFetch('/api/items')) {
  console.log(item);  // Process each item as it fetches
}

// AbortController — cancel requests
const controller = new AbortController();
const { signal } = controller;

setTimeout(() => controller.abort(), 5000);  // Cancel after 5s

try {
  const response = await fetch('/api/data', { signal });
  const data = await response.json();
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Request was cancelled');
  }
}
```

---

## 10. Modern JavaScript Features (ES2020-2024)

```javascript
// Optional Chaining (?.)
const city = user?.address?.city;         // No error if user/address undefined
const firstTag = tags?.[0];               // Optional array access
const result = callback?.();              // Optional function call

// Nullish Coalescing (??)
const name = user.name ?? 'Anonymous';   // Only null/undefined, not 0/''
const count = data.count ?? 0;           // 0 if count is null/undefined

// Logical Assignment
user.name ??= 'Anonymous';   // Assign only if null/undefined
user.active ||= true;        // Assign only if falsy
user.score &&= user.score * 1.1; // Assign only if truthy

// Object.fromEntries (inverse of Object.entries)
const headers = new Map([['Content-Type', 'application/json'], ['Authorization', 'Bearer ...']]);
const headersObj = Object.fromEntries(headers);

const doubled = Object.fromEntries(
  Object.entries(prices).map(([key, val]) => [key, val * 2])
);

// at() — negative indexing
const last = arr.at(-1);      // Last element
const secondLast = arr.at(-2);

// Array methods
const hasError = errors.some(e => e.critical);
const allValid = fields.every(f => f.isValid());
const firstError = errors.find(e => e.code === 404);

// structuredClone — deep clone
const original = { a: 1, nested: { b: [1, 2, 3] } };
const clone = structuredClone(original);   // Deep clone (no library needed!)
clone.nested.b.push(4);
original.nested.b;  // [1, 2, 3] — not affected!

// Object.hasOwn (replaces hasOwnProperty)
Object.hasOwn(obj, 'key');  // vs obj.hasOwnProperty('key')

// Top-level await (in modules)
const config = await fetch('/api/config').then(r => r.json());
export default config;

// Error cause
try {
  await processOrder(order);
} catch (error) {
  throw new Error('Failed to process payment', { cause: error });
}

// Pattern: using cause
try {
  something();
} catch (err) {
  console.log(err.cause);  // Original error
}
```

---

*Tài liệu liên quan: `javascript/01-js-basics.md` | `typescript/01-typescript-basics.md` | `programming/03-async-programming.md`*
