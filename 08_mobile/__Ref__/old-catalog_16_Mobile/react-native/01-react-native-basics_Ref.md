# 📱 React Native cơ bản — Sức mạnh đa nền tảng

> `[INTERMEDIATE]` — Lập trình Web sang Lập trình Mobile

---

## React Native là gì?

**React Component → Native UI (iOS / Android)**

Không phải là ứng dụng Web chạy trong WebView giống Ionic / Cordova. Nó **dịch** các Component của React (như `<View>`, `<Text>`) thành các thành phần Native thực sự của Hệ điều hành.

```
Web:      React ──► DOM ──► Browser
Native:   React ──► Bridge ──► iOS/Android Native UI
```

---

## 1. Web vs Native — Sự khác biệt cốt lõi

### 1.1 Elements thay đổi hoàn toàn

| Web (React) | Mobile (React Native) | Chức năng |
|---|---|---|
| `<div>` | `<View>` | Khung chứa (Container) |
| `<p>`, `<span>`, `<h1>` | `<Text>` | Hiển thị chữ |
| `<img>` | `<Image>` | Hình ảnh |
| `<button>` | `<Button>`, `<TouchableOpacity>` | Nút bấm |
| `<input type="text">` | `<TextInput>` | Nhập liệu |
| `overflow: scroll` | `<ScrollView>`, `<FlatList>` | Cuộn danh sách |

### 1.2 Styling = Không có CSS!

React Native dùng **StyleSheet** (JavaScript Object mô phỏng CSS).
- Không có class, id, tag selector.
- **Mọi thứ đều là Flexbox theo mặc định** và hướng `flexDirection: 'column'` thay vì `row` như Web.

```jsx
// ❌ Web CSS
// .container { display: flex; align-items: center; color: red; }
// <div className="container">

// ✅ React Native
import { StyleSheet, View, Text } from 'react-native';

const styles = StyleSheet.create({
    container: {
        flex: 1,  // Chiếm toàn bộ không gian
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#f5f5f5',  // Đơn vị px viết không cần chữ 'px'
    },
    text: {
        color: 'red',
        fontSize: 18,
    }
});

function App() {
    return (
        <View style={styles.container}>
            <Text style={styles.text}>Hello World!</Text>
        </View>
    );
}
```

---

## 2. React Native CLI vs Expo

Mọi dự án bắt đầu đều phải đối mặt với lựa chọn này:

| Tính năng | Expo 💯 (Khuyên dùng) | React Native CLI |
|---|---|---|
| Cài đặt | `npx create-expo-app` (Nhanh, dễ) | `npx @react-native-community/cli init` |
| Máy Mac? | KHÔNG cần Mac vẫn code được iOS! | BẮT BUỘC phải có Mac để build iOS |
| Chạy thử | Quét QR code, chạy trên đt qua app Expo Go | Phải cài Android Studio, Xcode |
| Custom Native Code | Dùng EAS Build, Development Builds | Thoải mái sửa Objective-C / Java |
| Build Cloud | Có sẵn Expo Application Services (EAS) | Phải tự cấu hình Fastlane, CI/CD |

---

## 3. Các Components quan trọng nhất

### ScrollView vs FlatList

```jsx
// ❌ Dùng cho danh sách ngắn (< 30 items)
// Render MỌI items cùng lúc → Chậm!
<ScrollView>
    {items.map(item => <Item key={item.id} data={item} />)}
</ScrollView>

// ✅ Dùng cho danh sách dài (Hàng ngàn items)
// Chỉ render các items đang hiển thị trên màn hình → Nhanh! (Virtualization)
<FlatList
    data={items}
    keyExtractor={(item) => item.id}
    renderItem={({ item }) => <Item data={item} />}
    onEndReached={() => fetchMoreData()}  // Lazy Load
/>
```

### SafeAreaView

Bảo vệ UI khỏi bị che bởi "Tai thỏ" (Notch) hoặc Dynamic Island của iPhone.

```jsx
import { SafeAreaView } from 'react-native-safe-area-context';

export default function App() {
    return (
        <SafeAreaView style={{ flex: 1 }}>
            <Text>Không bao giờ bị chèn lên camera notch!</Text>
        </SafeAreaView>
    );
}
```

---

## 4. Navigation (Chuyển trang)

Không giống URL trên web (`react-router-dom`), Mobile dùng **Stack** (Ngăn xếp).

```bash
# Cài đặt React Navigation
npm install @react-navigation/native @react-navigation/native-stack
```

```jsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

function HomeScreen({ navigation }) {
    return (
        <Button
            title="Đi tới Cài đặt"
            onPress={() => navigation.navigate('Settings', { userId: 123 })}
        />
    );
}

function SettingsScreen({ route, navigation }) {
    const { userId } = route.params;  // Nhận data
    return (
        <View>
            <Text>User: {userId}</Text>
            <Button title="Quay lại" onPress={() => navigation.goBack()} />
        </View>
    );
}

export default function App() {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="Home">
                <Stack.Screen name="Home" component={HomeScreen} />
                <Stack.Screen name="Settings" component={SettingsScreen} />
            </Stack.Navigator>
        </NavigationContainer>
    );
}
```

---

## 5. React Native Architecture Mới (Fabric & TurboModules)

```
Từ phiên bản 0.68+, React Native thay đổi hoàn toàn kiến trúc:

Kiến trúc Cũ (Bridge):
  JS Thread ← [JSON qua Bridge (Bị nghẽn)] → Native Thread
  → Component Scroll nhanh bị lag rỗng (White blank).

Kiến trúc Mới (JSI - JavaScript Interface):
  JS Thread trực tiếp gọi API của C++ Native!
  → Đồng bộ (Synchronous), cực nhanh.
  → Fabric (UI Layer mới), TurboModules (Native Modules Lazy Load).
```

---

## Các lỗi thường gặp

```
❌ Sai: Dùng `onClick` trên thẻ `<View>`
✅ Đúng: Dùng các component touchable: `onPress` trên `<TouchableOpacity>` hoặc `<Pressable>`

❌ Sai: Layout absolute hoặc dùng width bằng `px` hay `%` rối rắm
✅ Đúng: Luôn ưu tiên Flexbox. Flexbox trong RN xử lý được 99% UI.

❌ Sai: Dùng `div` và `span` vì thói quen Web
✅ Đúng: Quen với `View` và `Text`. Sẽ báo lỗi đỏ chót nếu có tag HTML thường.
```

---

## Bài tập thực hành

- [ ] Cài app **Expo Go** trên điện thoại.
- [ ] Khởi tạo project với `npx create-expo-app MyFirstApp`.
- [ ] Làm UI màn hình đăng nhập (Input username, password, button Login). Dùng Flexbox căn giữa màn hình.
- [ ] Thêm FlatList hiển thị 100 tên giả.

---

## Tài nguyên thêm

- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [Expo Documentation](https://docs.expo.dev/)
- [React Navigation](https://reactnavigation.org/)
