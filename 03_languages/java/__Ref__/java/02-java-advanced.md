# Java Advanced — JVM, Concurrency, Spring

> **Tags:** `java` `jvm` `concurrency` `spring-boot` `gc` `streams` `virtual-threads`
> **Level:** Advanced | **Prerequisite:** `java/01-java-basics.md`

---

## 1. JVM Internals

```
┌─────────────────────────── JVM Memory ─────────────────────────────┐
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │                          Heap                               │    │
│  │  ┌─────────────────────┐  ┌─────────────────────────────┐  │    │
│  │  │    Young Gen        │  │         Old Gen              │  │    │
│  │  │  ┌──────┬─────────┐ │  │  (long-lived objects)       │  │    │
│  │  │  │ Eden │Survivor │ │  │                             │  │    │
│  │  │  │      │ S0 | S1 │ │  │                             │  │    │
│  │  │  └──────┴─────────┘ │  └─────────────────────────────┘  │    │
│  │  └─────────────────────┘                                    │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌───────────────┐  ┌──────────────┐  ┌────────────────────────┐   │
│  │  Metaspace    │  │ Stack        │  │ Code Cache             │   │
│  │ (class meta,  │  │ (per thread) │  │ (JIT compiled code)    │   │
│  │  static vars) │  │              │  │                        │   │
│  └───────────────┘  └──────────────┘  └────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

### Garbage Collection Tuning
```bash
# G1GC (default Java 9+) — best for most applications
java -Xms2g -Xmx8g \
     -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=200 \      # Target GC pause < 200ms
     -XX:G1HeapRegionSize=16m \
     -XX:+PrintGCDetails \
     -XX:+PrintGCDateStamps \
     -Xlog:gc*:file=gc.log:time,uptime:filecount=10,filesize=10m \
     -jar app.jar

# ZGC (Java 15+) — ultra-low pause (<10ms), good for large heaps
java -XX:+UseZGC -Xmx32g -jar app.jar

# GraalVM Native Image — no JVM, instant startup, low memory
native-image -jar app.jar    # Compile to native binary
./app   # Starts in <100ms, uses 50% less memory
```

### JVM Flags Reference
```bash
# Memory
-Xms=<size>  # Initial heap size
-Xmx=<size>  # Maximum heap size (set equal to -Xms to avoid resizing)
-Xss=<size>  # Thread stack size (default 512k-1m)
-XX:MetaspaceSize=256m
-XX:MaxMetaspaceSize=512m

# Monitoring
java.lang.management.ManagementFactory.getMemoryMXBean()  # Programmatic

# Heap dump on OOM
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/log/app/

# JMX monitoring
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.port=9999
-Dcom.sun.management.jmxremote.authenticate=false
```

---

## 2. Concurrency

### Thread Fundamentals
```java
// Runnable vs Callable
Runnable task = () -> System.out.println("Hello from thread");
new Thread(task).start();

Callable<Integer> callable = () -> {
    return 42;   // Can return value and throw exceptions
};

// ExecutorService — managed thread pools
ExecutorService executor = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors()
);

// Submit tasks
Future<String> future = executor.submit(() -> {
    Thread.sleep(1000);
    return "Result";
});

String result = future.get(2, TimeUnit.SECONDS);  // Blocks with timeout

// Proper shutdown
executor.shutdown();
executor.awaitTermination(30, TimeUnit.SECONDS);
```

### CompletableFuture — Async Composition
```java
// Chain async operations
CompletableFuture<User> future = CompletableFuture
    .supplyAsync(() -> fetchUser(userId), executor)   // Run async
    .thenApplyAsync(user -> enrichUser(user))          // Transform result
    .thenCombine(                                       // Combine two futures
        CompletableFuture.supplyAsync(() -> fetchOrders(userId)),
        (user, orders) -> new UserWithOrders(user, orders)
    )
    .exceptionally(ex -> {                             // Handle errors
        log.error("Failed", ex);
        return DEFAULT_USER;
    });

// Run all in parallel, wait for all
List<CompletableFuture<String>> futures = userIds.stream()
    .map(id -> CompletableFuture.supplyAsync(() -> fetchUser(id), executor))
    .toList();

CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]))
    .thenApply(v -> futures.stream()
        .map(CompletableFuture::join)
        .toList()
    );

// Race — take whichever completes first
CompletableFuture.anyOf(primary, fallback)
    .thenAccept(result -> processResult(result));
```

### Virtual Threads (Java 21) — Project Loom
```java
// Virtual threads: millions of concurrent threads, blocking I/O is OK!
// Platform threads: expensive (~1MB stack), limited to ~few thousands

// Before (reactive programming to avoid blocking):
// Mono.fromCallable(() -> db.find(id)).subscribeOn(Schedulers.boundedElastic())

// After (Java 21+): just write blocking code!
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 100_000; i++) {
        executor.submit(() -> {
            // This blocks! But with virtual threads, it's fine
            User user = userService.findById(i);  // DB call
            String result = httpClient.get("https://api.example.com/enrich/" + user.id);  // HTTP call
            userService.update(user.id, result);   // DB write
        });
    }
}
// 100,000 concurrent blocking operations → fine with virtual threads!

// Spring Boot 3.2+:
// spring.threads.virtual.enabled=true  → one line to enable!
```

### Synchronized & Locks
```java
// synchronized method (coarse-grained)
public synchronized void increment() {
    counter++;
}

// synchronized block (fine-grained)
public void transfer(Account from, Account to, BigDecimal amount) {
    // Order locks to prevent deadlock
    Account first = from.id < to.id ? from : to;
    Account second = from.id < to.id ? to : from;
    
    synchronized (first) {
        synchronized (second) {
            from.balance = from.balance.subtract(amount);
            to.balance = to.balance.add(amount);
        }
    }
}

// ReentrantLock — more control
private final ReentrantLock lock = new ReentrantLock();
private final Condition notEmpty = lock.newCondition();

public boolean tryPut(T item, long timeout) throws InterruptedException {
    if (lock.tryLock(timeout, TimeUnit.MILLISECONDS)) {
        try {
            queue.add(item);
            notEmpty.signalAll();
            return true;
        } finally {
            lock.unlock();
        }
    }
    return false;
}

// StampedLock — optimistic reads (Java 8+)
private final StampedLock lock = new StampedLock();

public double read() {
    long stamp = lock.tryOptimisticRead();   // No locking!
    double value = this.value;
    if (!lock.validate(stamp)) {             // Validate no write happened
        stamp = lock.readLock();             // Fall back to read lock
        try { value = this.value; }
        finally { lock.unlockRead(stamp); }
    }
    return value;
}
```

### Atomic Types
```java
import java.util.concurrent.atomic.*;

AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();
counter.addAndGet(5);
counter.compareAndSet(5, 10);   // CAS: if current == 5, set to 10

// Long accumulator — for high contention
LongAdder adder = new LongAdder();   // More efficient than AtomicLong under contention
adder.increment();
long total = adder.sum();

// AtomicReference — for object references
AtomicReference<User> currentUser = new AtomicReference<>();
currentUser.compareAndSet(expected, newUser);   // Thread-safe CAS

// VarHandle (Java 9+) — most flexible
```

---

## 3. Java Streams — Advanced

```java
// Collectors
Map<String, List<User>> byCity = users.stream()
    .collect(Collectors.groupingBy(User::getCity));

Map<String, Long> countByCity = users.stream()
    .collect(Collectors.groupingBy(User::getCity, Collectors.counting()));

Map<Boolean, List<User>> partitioned = users.stream()
    .collect(Collectors.partitioningBy(u -> u.getAge() >= 18));

// Custom collector
Collector<User, ?, Stats> statsCollector = Collector.of(
    Stats::new,
    (stats, user) -> stats.add(user),
    Stats::merge,
    Collector.Characteristics.UNORDERED
);

// Flatmap
List<String> allTags = articles.stream()
    .flatMap(a -> a.getTags().stream())  // Flatten nested lists
    .distinct()
    .sorted()
    .toList();

// Reduce
Optional<BigDecimal> total = orders.stream()
    .map(Order::getAmount)
    .reduce(BigDecimal::add);

// peek — for debugging (doesn't consume stream)
users.stream()
    .peek(u -> log.debug("Before filter: {}", u.getName()))
    .filter(User::isActive)
    .peek(u -> log.debug("After filter: {}", u.getName()))
    .toList();

// Parallel streams (use for CPU-intensive, independent operations)
long count = largeCsvData.parallelStream()
    .filter(row -> row.getValue() > 1000)
    .mapToLong(Row::getCount)
    .sum();

// Custom Spliterator for custom parallel processing
```

---

## 4. Spring Boot — Deep Dive

### Auto-configuration
```java
// Spring Boot creates beans automatically based on classpath
// You can see what was auto-configured:
// Run with --debug flag, or:

@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(App.class);
        app.run(args);
        // Check: target/classes/META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
    }
}

// Conditional beans
@Bean
@ConditionalOnProperty(name = "app.cache.enabled", havingValue = "true")
public CacheManager cacheManager() {
    return new RedisCacheManager(redisConnectionFactory);
}

@Bean
@ConditionalOnMissingBean(CacheManager.class)
public CacheManager defaultCacheManager() {
    return new ConcurrentMapCacheManager();
}

// Custom auto-configuration
@AutoConfiguration
@ConditionalOnClass(SomeLibrary.class)
@EnableConfigurationProperties(MyProperties.class)
public class MyAutoConfiguration {
    @Bean
    @ConditionalOnMissingBean
    public MyService myService(MyProperties properties) {
        return new MyService(properties);
    }
}
```

### Spring Security
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers(HttpMethod.GET, "/api/products/**").authenticated()
                .anyRequest().authenticated()
            )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .csrf(csrf -> csrf.disable())   // For stateless APIs
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            )
            .exceptionHandling(ex -> ex
                .authenticationEntryPoint(customAuthEntryPoint)
                .accessDeniedHandler(customAccessDeniedHandler)
            )
            .build();
    }

    @Bean
    public JwtDecoder jwtDecoder() {
        return NimbusJwtDecoder.withPublicKey(rsaPublicKey).build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(12);
    }
}

// Method-level security
@PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")
public User getUser(Long userId) { ... }

@PostAuthorize("returnObject.userId == authentication.principal.id")
public Order getOrder(Long orderId) { ... }
```

### Spring Data JPA — Advanced
```java
// Custom repository methods
public interface UserRepository extends JpaRepository<User, Long> {
    // Spring generates SQL from method name
    List<User> findByEmailAndActiveTrue(String email);
    
    @Query("SELECT u FROM User u WHERE u.createdAt >= :since AND SIZE(u.orders) >= :minOrders")
    List<User> findActiveUsersWithOrders(@Param("since") LocalDateTime since, 
                                         @Param("minOrders") int minOrders);
    
    // Native query
    @Query(value = "SELECT * FROM users WHERE LOWER(email) LIKE LOWER(:pattern)",
           nativeQuery = true)
    Page<User> searchByEmail(@Param("pattern") String pattern, Pageable pageable);
    
    // Projection (only fetch needed fields)
    List<UserSummary> findByActive(boolean active);
}

// Projection interface
interface UserSummary {
    Long getId();
    String getName();
    String getEmail();
}

// Specification (dynamic queries)
public class UserSpecifications {
    public static Specification<User> hasCity(String city) {
        return (root, query, cb) -> 
            city == null ? cb.conjunction() : cb.equal(root.get("city"), city);
    }
    
    public static Specification<User> isActive() {
        return (root, query, cb) -> cb.isTrue(root.get("active"));
    }
    
    public static Specification<User> olderThan(int age) {
        return (root, query, cb) -> 
            cb.lessThan(root.get("birthDate"), LocalDate.now().minusYears(age));
    }
}

// Usage
List<User> users = userRepo.findAll(
    where(hasCity("Hanoi")).and(isActive()).and(olderThan(18)),
    PageRequest.of(0, 20, Sort.by("name"))
);
```

---

## 5. Reactive Programming — WebFlux

```java
// Project Reactor (Spring WebFlux)
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

// Mono = 0 or 1 element
// Flux = 0..N elements

@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")
    public Mono<User> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .switchIfEmpty(Mono.error(new NotFoundException("User not found")));
    }

    @GetMapping
    public Flux<User> getAllUsers() {
        return userService.findAll()
            .filter(User::isActive)
            .take(100);           // Limit results
    }

    @GetMapping(value = "/events", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<User>> userEvents() {
        return Flux.interval(Duration.ofSeconds(1))
            .flatMap(i -> userService.getRecentUsers())
            .map(user -> ServerSentEvent.builder(user).build());
    }
}

// Reactive patterns
Flux<Order> orders = orderRepository.findAll();

Mono<Stats> stats = orders
    .filter(o -> o.getStatus() == COMPLETED)
    .map(Order::getTotal)
    .reduce(new Stats(), Stats::add)
    .defaultIfEmpty(Stats.empty());

// Parallel processing
Flux.fromIterable(userIds)
    .flatMap(id -> userService.findById(id), 10)  // 10 concurrent queries
    .collectList();

// Error handling
userService.findById(id)
    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1)))
    .onErrorResume(TimeoutException.class, e -> Mono.just(User.ANONYMOUS))
    .timeout(Duration.ofSeconds(5));
```

---

## 6. Profiling & Performance

```bash
# async-profiler — CPU and allocation profiling
java -agentpath:/path/to/libasyncProfiler.so=start,event=cpu,file=cpu-profile.html

# JFR — Java Flight Recorder (no overhead, production-safe)
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr app.jar
java -XX:StartFlightRecording=disk=true,name=continuous,settings=default app.jar

# Analyze JFR
jfr print --events jdk.GarbageCollection recording.jfr
# Or: JDK Mission Control (GUI tool)

# JVM stats
jstat -gcutil <pid> 1000   # GC stats every 1 second
jmap -heap <pid>           # Heap summary

# Thread dump (for deadlock analysis)
jstack <pid>
kill -3 <pid>   # Also dumps to stdout
```

---

## 7. Testing — JUnit 5, Testcontainers

```java
// Testcontainers — real dependencies in tests
@SpringBootTest
@Testcontainers
class UserServiceIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @Container
    static RedisContainer redis = new RedisContainer("redis:7");

    @DynamicPropertySource
    static void overrideProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.redis.host", redis::getHost);
        registry.add("spring.redis.port", redis::getFirstMappedPort);
    }

    @Autowired
    UserService userService;

    @Test
    void createUser_shouldPersistToDatabase() {
        var request = new CreateUserRequest("alice@example.com", "Alice");
        User created = userService.createUser(request);

        assertThat(created.getId()).isNotNull();
        assertThat(created.getEmail()).isEqualTo("alice@example.com");
        
        // Verify in DB
        User found = userService.findById(created.getId()).orElseThrow();
        assertThat(found.getEmail()).isEqualTo("alice@example.com");
    }
}

// WireMock for HTTP mocks
@SpringBootTest
class UserClientTest {

    @RegisterExtension
    static WireMockExtension wm = WireMockExtension.newInstance()
        .options(wireMockConfig().port(8089))
        .build();

    @Test
    void shouldFetchExternalUser() {
        wm.stubFor(get("/users/1")
            .willReturn(okJson("""{"id":1,"name":"Alice"}""")));
        
        User user = userClient.fetchUser(1L);
        assertThat(user.getName()).isEqualTo("Alice");
    }
}
```

---

*Tài liệu liên quan: `java/01-java-basics.md` | `frameworks/spring-boot.md` | `cs/03-concurrency-parallelism.md`*
