# ☕ Java — Ngôn ngữ Enterprise

> `[INTERMEDIATE]` — Ngôn ngữ phổ biến nhất trong hệ thống doanh nghiệp lớn

---

## Tại sao Java?

- **Write once, run anywhere** — JVM chạy trên mọi nền tảng
- **Enterprise standard** — Banking, fintech, hệ thống lớn
- **Spring Boot** — Framework web phổ biến nhất cho Java
- **Android** — Ngôn ngữ gốc cho phát triển Android
- **Mature ecosystem** — 30 năm, cộng đồng khổng lồ

---

## Cài đặt

```bash
# Cài JDK (Java Development Kit)
# Dùng SDKMAN để quản lý phiên bản
curl -s "https://get.sdkman.io" | bash
sdk install java 21.0.0-tem

java -version
javac -version

# Build tool: Maven hoặc Gradle
sdk install maven
sdk install gradle
```

---

## Cú pháp cơ bản

```java
// HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        // Variables
        String name = "Jesse";
        int age = 25;
        double salary = 1000.50;
        boolean isActive = true;
        
        System.out.println("Xin chào, " + name);
        System.out.printf("Tuổi: %d, Lương: %.2f%n", age, salary);
        
        // String methods
        String upper = name.toUpperCase();
        boolean contains = name.contains("ess");
        String trimmed = "  hello  ".trim();
    }
}
```

---

## OOP trong Java

```java
// Abstract class
public abstract class Animal {
    private String name;
    private int age;
    
    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // Getter/Setter
    public String getName() { return name; }
    public int getAge() { return age; }
    
    // Abstract method
    public abstract String speak();
    
    @Override
    public String toString() {
        return String.format("%s (%d tuổi)", name, age);
    }
}

// Interface
public interface Trainable {
    void train(String command);
    default void printTrainable() {
        System.out.println("Có thể huấn luyện được");
    }
}

// Concrete class
public class Dog extends Animal implements Trainable {
    public Dog(String name, int age) {
        super(name, age);
    }
    
    @Override
    public String speak() {
        return getName() + " sủa: Woof!";
    }
    
    @Override
    public void train(String command) {
        System.out.println(getName() + " học lệnh: " + command);
    }
}
```

---

## Collections

```java
import java.util.*;
import java.util.stream.*;

// List
List<String> fruits = new ArrayList<>(Arrays.asList("apple", "banana", "cherry"));
fruits.add("mango");
fruits.get(0);                      // "apple"
fruits.size();                      // 4
Collections.sort(fruits);

// Map
Map<String, Integer> scores = new HashMap<>();
scores.put("Alice", 95);
scores.put("Bob", 87);
scores.getOrDefault("Charlie", 0);  // 0

// Set
Set<String> tags = new HashSet<>(Arrays.asList("java", "backend", "java"));
// {"java", "backend"} — không trùng lặp

// Stream API (Java 8+)
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

List<Integer> result = numbers.stream()
    .filter(n -> n % 2 == 0)       // [2, 4, 6, 8, 10]
    .map(n -> n * n)                // [4, 16, 36, 64, 100]
    .sorted()
    .collect(Collectors.toList());

int sum = numbers.stream()
    .reduce(0, Integer::sum);       // 55

Optional<Integer> first = numbers.stream()
    .filter(n -> n > 5)
    .findFirst();                   // Optional[6]
```

---

## Exception Handling

```java
// Checked vs Unchecked exceptions
public void readFile(String path) throws IOException {  // Checked — bắt buộc khai báo
    try {
        FileReader reader = new FileReader(path);
        // ...
    } catch (FileNotFoundException e) {
        throw new RuntimeException("File không tìm thấy: " + path, e);
    } catch (IOException e) {
        logger.error("Lỗi đọc file", e);
        throw e;
    } finally {
        // Luôn chạy
    }
}

// Try-with-resources (tự động đóng)
try (var reader = new FileReader(path);
     var buffered = new BufferedReader(reader)) {
    String line;
    while ((line = buffered.readLine()) != null) {
        System.out.println(line);
    }
}
```

---

## Modern Java (Records, Sealed Classes)

```java
// Record (Java 16+) — Immutable data class
public record User(int id, String name, String email) {}

User user = new User(1, "Jesse", "jesse@example.com");
user.name();   // "Jesse"

// Sealed class (Java 17+)
public sealed interface Shape
    permits Circle, Rectangle, Triangle {}

public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}

// Pattern matching
double area = switch (shape) {
    case Circle c -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
    case Triangle t -> /* ... */ 0;
};
```

---

## Bài tập thực hành

- [ ] Implement các Data Structures: LinkedList, Stack, Queue
- [ ] REST API đơn giản với Spring Boot
- [ ] CRUD application với Spring Boot + JPA + PostgreSQL
- [ ] Implement Design Patterns: Singleton, Factory, Observer

---

## Tài nguyên thêm

- [Java Documentation](https://docs.oracle.com/en/java/) — Oracle chính thức
- [Baeldung](https://www.baeldung.com/) — Tutorials Spring Boot tốt nhất
- [Effective Java (book)](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/) — Kinh thánh Java
