# 📱 React Native cơ bản — Mobile app bằng JavaScript

> `[BEGINNER → INTERMEDIATE]` — 1 codebase, 2 platforms (iOS + Android)

---

## Tại sao React Native?

- **1 codebase** → chạy trên iOS + Android (tiết kiệm 50% effort)
- **JavaScript/TypeScript** — tận dụng kỹ năng web developer
- **Hot Reload** — xem thay đổi ngay lập tức
- Dùng bởi: Facebook, Instagram, Discord, Shopify, Bloomberg

---

## 1. React Native vs React (Web)

| | React (Web) | React Native (Mobile) |
|---|---|---|
| **Render** | DOM (div, span, p) | Native Views (View, Text) |
| **Style** | CSS files | StyleSheet (JavaScript object) |
| **Navigation** | React Router | React Navigation |
| **Touch** | onClick | onPress |
| **List** | map() | FlatList (virtualized) |
| **Output** | HTML | Native iOS/Android components |

```jsx
// React Web
<div className="container">
    <h1>Hello</h1>
    <p onClick={handleClick}>Tap me</p>
</div>

// React Native
<View style={styles.container}>
    <Text style={styles.title}>Hello</Text>
    <Pressable onPress={handlePress}>
        <Text>Tap me</Text>
    </Pressable>
</View>
```

---

## 2. Core Components

```jsx
import {
    View,           // div
    Text,           // p, span, h1
    Image,          // img
    ScrollView,     // Scrollable container
    TextInput,      // input
    Pressable,      // Button/touchable
    FlatList,       // Virtualized list (hiệu năng cao)
    StyleSheet,     // CSS-in-JS
    SafeAreaView,   // Tránh notch iPhone
} from 'react-native';

function ProfileScreen() {
    return (
        <SafeAreaView style={styles.container}>
            <Image
                source={{ uri: 'https://example.com/avatar.jpg' }}
                style={styles.avatar}
            />
            <Text style={styles.name}>Nguyễn Văn An</Text>
            <Text style={styles.bio}>Full-stack developer 🚀</Text>

            <Pressable
                style={({ pressed }) => [
                    styles.button,
                    pressed && styles.buttonPressed,
                ]}
                onPress={() => alert('Pressed!')}
            >
                <Text style={styles.buttonText}>Edit Profile</Text>
            </Pressable>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#fff',
    },
    avatar: {
        width: 120,
        height: 120,
        borderRadius: 60,
        marginBottom: 16,
    },
    name: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#1a1a1a',
    },
    bio: {
        fontSize: 16,
        color: '#666',
        marginTop: 8,
    },
    button: {
        backgroundColor: '#3b82f6',
        paddingHorizontal: 32,
        paddingVertical: 12,
        borderRadius: 8,
        marginTop: 24,
    },
    buttonPressed: {
        opacity: 0.8,
    },
    buttonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: '600',
    },
});
```

---

## 3. Flexbox Layout — Mặc định!

```jsx
// React Native mặc định flexDirection: 'column' (khác web là 'row')

const styles = StyleSheet.create({
    // Vertical layout (mặc định)
    column: {
        flex: 1,
        flexDirection: 'column',      // Mặc định
        justifyContent: 'center',
        alignItems: 'center',
    },

    // Horizontal layout
    row: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 16,
    },

    // Card
    card: {
        backgroundColor: '#fff',
        borderRadius: 12,
        padding: 16,
        marginVertical: 8,
        // Shadow (khác nhau iOS vs Android)
        shadowColor: '#000',           // iOS
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,                  // Android
    },
});
```

---

## 4. FlatList — Danh sách hiệu năng cao

```jsx
function TodoList() {
    const [todos, setTodos] = useState([
        { id: '1', text: 'Học React Native', done: false },
        { id: '2', text: 'Build todo app', done: true },
    ]);

    const renderItem = ({ item }) => (
        <Pressable
            style={styles.todoItem}
            onPress={() => toggleTodo(item.id)}
        >
            <Text style={[
                styles.todoText,
                item.done && styles.todoDone,
            ]}>
                {item.done ? '✅' : '⬜'} {item.text}
            </Text>
        </Pressable>
    );

    return (
        <FlatList
            data={todos}
            renderItem={renderItem}
            keyExtractor={(item) => item.id}
            ItemSeparatorComponent={() => <View style={styles.separator} />}
            ListEmptyComponent={() => <Text>Không có todo nào</Text>}
        />
    );
}
```

---

## 5. Navigation

```jsx
// React Navigation — thư viện navigation chuẩn
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function App() {
    return (
        <NavigationContainer>
            <Tab.Navigator>
                <Tab.Screen name="Home" component={HomeStack} />
                <Tab.Screen name="Profile" component={ProfileScreen} />
                <Tab.Screen name="Settings" component={SettingsScreen} />
            </Tab.Navigator>
        </NavigationContainer>
    );
}

function HomeStack() {
    return (
        <Stack.Navigator>
            <Stack.Screen name="List" component={ListScreen} />
            <Stack.Screen name="Detail" component={DetailScreen} />
        </Stack.Navigator>
    );
}

// Navigate between screens
function ListScreen({ navigation }) {
    return (
        <Pressable onPress={() => navigation.navigate('Detail', { id: 123 })}>
            <Text>Go to Detail</Text>
        </Pressable>
    );
}

function DetailScreen({ route }) {
    const { id } = route.params;
    return <Text>Detail for ID: {id}</Text>;
}
```

---

## 6. Platform-Specific Code

```jsx
import { Platform } from 'react-native';

const styles = StyleSheet.create({
    shadow: {
        ...Platform.select({
            ios: {
                shadowColor: '#000',
                shadowOffset: { width: 0, height: 2 },
                shadowOpacity: 0.15,
                shadowRadius: 4,
            },
            android: {
                elevation: 4,
            },
        }),
    },
});

// Hoặc tách file
// Button.ios.js
// Button.android.js
// import Button from './Button';  ← RN tự chọn đúng file!
```

---

## React Native vs Flutter vs Native

| | React Native | Flutter | Native (Swift/Kotlin) |
|---|---|---|---|
| **Ngôn ngữ** | JavaScript/TS | Dart | Swift / Kotlin |
| **UI** | Native components | Custom (Skia) | Native |
| **Performance** | Tốt | Rất tốt | Tốt nhất |
| **Hot Reload** | ✅ | ✅ | Limited |
| **Learning** | Dễ (biết React) | Trung bình | Khó (2 platforms) |
| **Dùng khi** | Team web → mobile | UI phức tạp, cross-platform | Performance critical |

---

## Các lỗi thường gặp

```
❌ Sai: Dùng ScrollView cho list dài → render TẤT CẢ items → lag
✅ Đúng: Dùng FlatList (virtualized — chỉ render items trên màn hình)

❌ Sai: Inline styles → re-create mỗi render
✅ Đúng: StyleSheet.create() → cached, tối ưu

❌ Sai: console.log trong production → memory leak
✅ Đúng: Remove hoặc dùng __DEV__ flag
```

---

## Bài tập thực hành

- [ ] Setup Expo project → Hello World → chạy trên điện thoại (Expo Go)
- [ ] Build Todo App: TextInput + FlatList + AsyncStorage
- [ ] Thêm Navigation: Tab + Stack navigator
- [ ] Fetch API + hiển thị list users với avatar

---

## Tài nguyên thêm

- [React Native Docs](https://reactnative.dev/) — Official
- [Expo Docs](https://docs.expo.dev/) — Dễ setup nhất cho beginners
- [React Navigation](https://reactnavigation.org/) — Navigation library
