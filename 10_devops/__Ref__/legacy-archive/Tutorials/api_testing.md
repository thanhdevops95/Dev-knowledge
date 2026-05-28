# Hướng dẫn Test API

## 📋**GIỚI THIỆU**

Tài liệu hướng dẫn test API sử dụng curl, Postman, và Python requests.

---

## 🔧**CURL CƠ BẢN**

### GET Request

```bash
# GET đơn giản
curl https://api.example.com/users
# ==> Gửi một yêu cầu HTTP GET đến API tại địa chỉ `https://api.example.com/users`. Khi lệnh này được thực thi, nó sẽ truy cập vào tài nguyên người dùng từ API và trả về dữ liệu liên quan đến người dùng trong định dạng JSON hoặc XML, tùy thuộc vào cách API được cấu hình. Đây là một cách phổ biến để kiểm tra và tương tác với các API trong phát triển phần mềm và kiểm thử tự động.

# GET với headers
curl -H "Authorization: Bearer TOKEN" https://api.example.com/users
# ==> Gửi yêu cầu GET kèm theo header xác thực Bearer Token. Điều này được sử dụng để truy cập các API được bảo vệ, nơi server yêu cầu token để xác minh danh tính của client.

# GET với query params
curl "https://api.example.com/users?page=1&limit=10"
# ==> Gửi yêu cầu GET với các tham số truy vấn (query parameters). Trong ví dụ này, `page=1` và `limit=10` được sử dụng để phân trang dữ liệu, lấy trang thứ 1 với tối đa 10 bản ghi.

# Hiển thị response headers
curl -i https://api.example.com/users
# ==> Tùy chọn `-i` hiển thị cả headers của response và body. Điều này hữu ích để kiểm tra thông tin HTTP như Content-Type, Cache-Control, và các thông tin khác từ server.

# Chỉ hiển thị headers
curl -I https://api.example.com/users
# ==> Tùy chọn `-I` (in hoa) chỉ hiển thị headers của response mà không hiển thị body. Thường dùng để kiểm tra trạng thái server nhanh chóng mà không cần tải dữ liệu lớn.

# Verbose mode (debug)
curl -v https://api.example.com/users
# ==> Tùy chọn `-v` cho phép xem chi tiết quá trình request/response bao gồm headers được gửi, headers nhận về, và dữ liệu. Rất hữu ích khi debug hoặc tìm hiểu API hoạt động như thế nào.
```

### POST Request

```bash
# POST với JSON data
curl -X POST https://api.example.com/users \
# ==> Tùy chọn `-X POST` chỉ định phương thức HTTP là POST, dùng để gửi dữ liệu mới tới server. URL `https://api.example.com/users` là endpoint nơi dữ liệu sẽ được gửi.
  -H "Content-Type: application/json" \
  # ==> Header này báo cho server biết rằng dữ liệu được gửi ở định dạng JSON. Điều này giúp server biết cách parse và xử lý dữ liệu nhận được.
  -d '{"name": "John", "email": "john@example.com"}'
  # ==> Tùy chọn `-d` (data) chứa phần thân của request với dữ liệu JSON sẽ được gửi tới server. Dữ liệu này sẽ được sử dụng để tạo một user mới với tên "John" và email "john@example.com".

# POST với form data
curl -X POST https://api.example.com/login \
# ==> Phương thức POST gửi dữ liệu tới endpoint login để xác thực người dùng.
  -d "username=admin&password=123456"
  # ==> Dữ liệu được gửi ở định dạng form data (key=value cách nhau bằng &). Đây là cách gửi dữ liệu truyền thống cho form login với username là "admin" và password là "123456".

# POST file
curl -X POST https://api.example.com/upload \
# ==> Phương thức POST gửi dữ liệu tới endpoint upload để tải lên tệp.
  -F "file=@/path/to/file.jpg"
  # ==> Tùy chọn `-F` dùng để upload file. Cú pháp `file=@/path/to/file.jpg` nói với curl rằng hãy gửi file từ đường dẫn `/path/to/file.jpg` với tên trường là "file".
```

### PUT Request

```bash
curl -X PUT https://api.example.com/users/1 \
# ==> Phương thức PUT dùng để cập nhật toàn bộ thông tin của user có ID là 1. URL `/users/1` chỉ định user cụ thể cần cập nhật.
  -H "Content-Type: application/json" \
  # ==> Header Content-Type chỉ định định dạng JSON cho request.
  -d '{"name": "John Updated"}'
  # ==> Dữ liệu JSON được gửi để cập nhật thông tin user, thay thế hoàn toàn dữ liệu cũ bằng dữ liệu mới.
```

### DELETE Request

```bash
curl -X DELETE https://api.example.com/users/1
# ==> Phương thức DELETE dùng để xóa user có ID là 1. Đây là hoạt động không thuận nghịch, xóa sẽ loại bỏ hoàn toàn dữ liệu của user.
```

### PATCH Request

```bash
curl -X PATCH https://api.example.com/users/1 \
# ==> Phương thức PATCH dùng để cập nhật một phần thông tin của user ID 1 (không cần cập nhật tất cả các trường như PUT).
  -H "Content-Type: application/json" \
  # ==> Header Content-Type chỉ định định dạng JSON.
  -d '{"name": "New Name"}'
  # ==> Chỉ trường "name" được cập nhật thành "New Name", các trường khác không bị thay đổi.
```

---

## 🔐**AUTHENTICATION**

### Basic Auth

```bash
curl -u username:password https://api.example.com/users
# ==> Tùy chọn `-u` dùng để gửi Basic Authentication. Username và password được mã hóa Base64 và gửi trong header Authorization. Thích hợp cho API yêu cầu xác thực cơ bản.

# Hoặc
curl -H "Authorization: Basic base64encoded" https://api.example.com/users
# ==> Cách này cho phép gửi Basic Authentication bằng cách tự mã hóa Base64. Nếu username=admin, password=123, thì base64encoded = "YWRtaW46MTIz". Cách này cung cấp kiểm soát nhiều hơn.
```

### Bearer Token

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/users
# ==> Gửi yêu cầu với Bearer Token authentication. Token này thường được cấp sau khi login và có thời hạn hết hạn. Dùng cho API hiện đại sử dụng JWT hoặc OAuth.
```

### API Key

```bash
# Trong header
curl -H "X-API-Key: YOUR_API_KEY" https://api.example.com/users
# ==> Gửi API Key qua header HTTP tùy chỉnh "X-API-Key". Đây là phương pháp phổ biến để xác thực API mà không cần login. Server sẽ kiểm tra header này để xác minh quyền truy cập.

# Trong query param
curl "https://api.example.com/users?api_key=YOUR_API_KEY"
# ==> Gửi API Key qua URL parameter. Cách này đơn giản nhưng kém bảo mật hơn vì API Key sẽ visible trong URL logs và history. Thường dùng cho API công khai hoặc test.
```

---

## 📤**CURL OPTIONS HỮU ÍCH**

| Option | Mô tả |
|--------|-------|
| `-X METHOD` | Chỉ định HTTP method |
| `-H "Header: Value"` | Thêm header |
| `-d "data"` | Gửi data (body) |
| `-F "file=@path"` | Upload file |
| `-o file.json` | Lưu output ra file |
| `-O` | Lưu với tên gốc |
| `-i` | Hiển thị response headers |
| `-v` | Verbose mode |
| `-s` | Silent mode (không hiện progress) |
| `-L` | Follow redirects |
| `-k` | Bỏ qua SSL certificate |
| `--connect-timeout 5` | Timeout 5 giây |

---

## 🐍**PYTHON REQUESTS**

### Cài đặt

```bash
pip install requests
# ==> Lệnh này cài đặt thư viện Python "requests", một công cụ mạnh mẽ để gửi HTTP requests. Là bước chuẩn bị cần thiết trước khi sử dụng requests trong Python code.
```

### GET Request

```python
import requests

# GET đơn giản
response = requests.get('https://api.example.com/users')
# ==> Gửi GET request đến URL và lưu response vào biến `response`. Dữ liệu nhận được có thể được truy cập qua các thuộc tính của đối tượng response.
print(response.status_code)  # 200
# ==> In mã trạng thái HTTP từ response. Giá trị 200 có nghĩa request thành công. Các mã khác như 404 (not found), 500 (server error) cho biết vấn đề nếu có.
print(response.json())       # JSON response
# ==> Phương thức `.json()` chuyển đổi response body từ JSON string thành Python dictionary. Điều này cho phép truy cập dữ liệu dễ dàng bằng key-value.

# GET với params
params = {'page': 1, 'limit': 10}
# ==> Tạo dictionary với các tham số query. Giá trị này sẽ được thêm vào URL tự động bởi requests library dưới dạng ?page=1&limit=10.
response = requests.get('https://api.example.com/users', params=params)
# ==> Gửi GET request với query parameters. Library requests sẽ tự động URL-encode params và thêm vào URL.

# GET với headers
headers = {'Authorization': 'Bearer TOKEN'}
# ==> Tạo dictionary chứa các headers HTTP cần gửi kèm request. Trong trường hợp này là token xác thức Bearer.
response = requests.get('https://api.example.com/users', headers=headers)
# ==> Gửi GET request với headers được định nghĩa trước. Headers sẽ được thêm vào request để xác thực hoặc chỉ định loại dữ liệu.
```

### POST Request

```python
import requests
# ==> Import thư viện requests để sử dụng các chức năng HTTP trong Python script.

# POST với JSON
data = {'name': 'John', 'email': 'john@example.com'}
# ==> Tạo dictionary chứa dữ liệu người dùng muốn gửi. Dictionary này sẽ được tự động chuyển đổi thành JSON format.
response = requests.post('https://api.example.com/users', json=data)
# ==> Gửi POST request với dữ liệu JSON. Tham số `json=data` tự động serializes dictionary thành JSON và set Content-Type header.

# POST với form data
data = {'username': 'admin', 'password': '123456'}
# ==> Tạo dictionary với dữ liệu form. Dữ liệu này sẽ được gửi dưới dạng application/x-www-form-urlencoded.
response = requests.post('https://api.example.com/login', data=data)
# ==> Gửi POST request với form data. Tham số `data=data` gửi dữ liệu dưới dạng URL-encoded form thay vì JSON.

# POST upload file
files = {'file': open('image.jpg', 'rb')}
# ==> Mở file 'image.jpg' ở chế độ nhị phân ('rb') và tạo dictionary để upload. 'rb' = read binary cho phép đọc file dưới dạng bytes.
response = requests.post('https://api.example.com/upload', files=files)
# ==> Gửi POST request để upload file. Tham số `files=files` báo cho requests library rằng sẽ upload multipart/form-data thay vì JSON.
```

### PUT, DELETE, PATCH

```python
import requests
# ==> Import thư viện requests để sử dụng các phương thức HTTP.

# PUT
response = requests.put(
# ==> Phương thức `.put()` gửi PUT request để cập nhật toàn bộ tài nguyên trên server.
    'https://api.example.com/users/1',
    # ==> URL endpoint chỉ định user có ID 1 cần cập nhật.
    json={'name': 'John Updated'}
    # ==> Dữ liệu JSON mới sẽ thay thế toàn bộ user record. Tham số `json=` tự động chuyển dictionary thành JSON.
)

# DELETE
response = requests.delete('https://api.example.com/users/1')
# ==> Gửi DELETE request để xóa user có ID 1. Thường không cần body cho DELETE request.

# PATCH
response = requests.patch(
# ==> Phương thức `.patch()` gửi PATCH request để cập nhật một phần dữ liệu của tài nguyên.
    'https://api.example.com/users/1',
    # ==> URL chỉ định user cần cập nhật một phần.
    json={'name': 'New Name'}
    # ==> Chỉ trường 'name' được cập nhật, các trường khác giữ nguyên.
)
```

### Xử lý Response

```python
import requests
# ==> Import thư viện requests.

response = requests.get('https://api.example.com/users')
# ==> Gửi GET request và lưu kết quả vào biến response để xử lý tiếp.

# Status code
print(response.status_code)      # 200
print(response.ok)               # True (nếu 2xx)

# Headers
print(response.headers)
print(response.headers['Content-Type'])

# Content
print(response.text)             # String
print(response.json())           # Dict (nếu JSON)
print(response.content)          # Bytes

# URL
print(response.url)
```

### Error Handling

```python
import requests
# ==> Import thư viện requests và các exception classes để xử lý lỗi.
from requests.exceptions import HTTPError, Timeout, RequestException
# ==> Import các lớp exception cụ thể: HTTPError (lỗi HTTP), Timeout (request quá lâu), RequestException (lỗi chung của requests).

try:
    response = requests.get(
        'https://api.example.com/users',
        timeout=5
    # ==> Tham số timeout=5 giới hạn thời gian chờ response là 5 giây. Nếu server không trả lời trong 5 giây, request sẽ bị hủy.
    )
    response.raise_for_status()  # Raise exception nếu không phải 2xx
    # ==> Phương thức `.raise_for_status()` sẽ raise HTTPError nếu status code không phải 2xx (success). Điều này giúp phát hiện lỗi HTTP.
    
except HTTPError as e:
    print(f"HTTP Error: {e}")
    # ==> Bắt lỗi HTTP (status code 4xx, 5xx) và in ra thông báo lỗi chi tiết.
except Timeout:
    print("Request timed out")
    # ==> Bắt lỗi timeout khi request vượt quá thời gian chờ được phép (5 giây trong ví dụ).
except RequestException as e:
    print(f"Error: {e}")
    # ==> Bắt các lỗi chung khác của requests library như kết nối bị từ chối, DNS resolution lỗi, v.v.
```

### Session (giữ cookies, headers)

```python
import requests
# ==> Import thư viện requests.

session = requests.Session()
# ==> Tạo một Session object. Session giữ lại cookies, headers, và authentication giữa các request, tiết kiệm time và resources.

# Đặt headers chung
session.headers.update({'Authorization': 'Bearer TOKEN'})
# ==> Phương thức `.update()` thêm header vào session. Tất cả các request sau sẽ tự động sử dụng header này mà không cần phải khai báo lại.

# Các request sau sẽ dùng headers này
response = session.get('https://api.example.com/users')
# ==> Request này sẽ tự động gửi kèm header Authorization mà không cần chỉ định lại.
response = session.get('https://api.example.com/posts')
# ==> Request thứ 2 cũng sẽ dùng chung header Authorization. Ngoài ra, session cũng sẽ giữ lại cookies từ các response trước đó.

session.close()
# ==> Đóng session để giải phóng tài nguyên. Một phương pháp tốt là dùng `with` statement để tự động đóng session.
```

---

## 📬**POSTMAN**

### Cài đặt

Tải từ [postman.com](https://www.postman.com/downloads/)

### Tạo Request

1. Click **New** → **HTTP Request**
2. Chọn method (GET, POST, PUT, DELETE)
3. Nhập URL
4. Thêm headers/body nếu cần
5. Click **Send**

### Tabs quan trọng

| Tab | Mô tả |
|-----|-------|
| **Params** | Query parameters |
| **Authorization** | Cấu hình auth |
| **Headers** | HTTP headers |
| **Body** | Request body (POST, PUT) |
| **Pre-request Script** | Script chạy trước request |
| **Tests** | Script test response |

### Body types

| Type | Dùng cho |
|------|----------|
| **form-data** | Upload file, form |
| **x-www-form-urlencoded** | Form thông thường |
| **raw (JSON)** | API với JSON |
| **binary** | File binary |

### Environment Variables

1. Click **Environments** → **New**
2. Thêm biến: `base_url = https://api.example.com`
3. Sử dụng trong request: `{{base_url}}/users`

### Collections

Nhóm các requests liên quan:
1. Click **Collections** → **New Collection**
2. Kéo các requests vào collection
3. Có thể chạy toàn bộ collection (Collection Runner)

### Tests Script (JavaScript)

```javascript
// Kiểm tra status code
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
// ==> Tạo test case kiểm tra xem status code của response có phải là 200 (success) không. Nếu không, test sẽ fail và báo lỗi.

// Kiểm tra response time
pm.test("Response time < 500ms", function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
// ==> Test kiểm tra performance của API bằng cách đo thời gian response. Nếu response time > 500ms, test sẽ fail, giúp phát hiện API chậm.

// Kiểm tra JSON response
pm.test("Response has users array", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('users');
    pm.expect(jsonData.users).to.be.an('array');
});
// ==> Test kiểm tra response JSON có chứa property 'users' hay không, và property đó phải là array. Hữu ích để validate struktur dữ liệu.

// Lưu giá trị vào biến
var jsonData = pm.response.json();
pm.environment.set("user_id", jsonData.id);
// ==> Parse JSON response và lưu giá trị id vào environment variable tên "user_id". Variable này có thể dùng lại trong các request tiếp theo với syntax {{user_id}}.
```

---

## 🔌**VSCODE EXTENSION: REST CLIENT**

### Cài đặt

1. Mở VSCode
2. Extensions → Tìm "REST Client"
3. Install

### Tạo file .http

Tạo file `api.http`:

```http
### GET Users
GET https://api.example.com/users
Authorization: Bearer {{token}}
# ==> Gửi GET request với Bearer Token lấy từ variable {{token}}.

### POST User
POST https://api.example.com/users
Content-Type: application/json
# ==> Chỉ định phương thức POST và loại dữ liệu là JSON. Dòng này là header của request.

{
    "name": "John",
    "email": "john@example.com"
}
# ==> Phần body của POST request chứa dữ liệu JSON để tạo user mới.

### PUT User
PUT https://api.example.com/users/1
Content-Type: application/json
# ==> Chỉ định phương thức PUT để cập nhật user ID 1 với dữ liệu JSON.

{
    "name": "John Updated"
}
# ==> Body chứa dữ liệu cập nhật cho user.

### DELETE User
DELETE https://api.example.com/users/1
# ==> Xóa user có ID 1. DELETE request thường không cần body.
```

### Variables

```http
@baseUrl = https://api.example.com
# ==> Định nghĩa biến @baseUrl với giá trị là URL base của API. Biến này sẽ được sử dụng lại trong nhiều request để tránh lặp lại URL dài.

@token = your-token-here
# ==> Định nghĩa biến @token lưu token xác thực. Biến này có thể được cập nhật sau khi login để dùng cho các request tiếp theo.

### GET Users
GET {{baseUrl}}/users
# ==> Sử dụng biến @baseUrl trong request. Syntax {{baseUrl}} sẽ được thay thế bằng giá trị https://api.example.com.

Authorization: Bearer {{token}}
# ==> Sử dụng biến @token trong header. Khi chạy request, {{token}} sẽ được thay thế bằng giá trị token thực tế.
```

### Chạy Request

Click **Send Request** phía trên mỗi request.

---

## 📊**HTTP STATUS CODES**

### 2xx - Success

| Code | Ý nghĩa |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |

### 3xx - Redirect

| Code | Ý nghĩa |
|------|---------|
| 301 | Moved Permanently |
| 302 | Found (Temporary Redirect) |
| 304 | Not Modified |

### 4xx - Client Error

| Code | Ý nghĩa |
|------|---------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 405 | Method Not Allowed |
| 422 | Unprocessable Entity |
| 429 | Too Many Requests |

### 5xx - Server Error

| Code | Ý nghĩa |
|------|---------|
| 500 | Internal Server Error |
| 502 | Bad Gateway |
| 503 | Service Unavailable |
| 504 | Gateway Timeout |

---

## 🧪**API CÔNG KHAI ĐỂ TEST**

| API | URL | Mô tả |
|-----|-----|-------|
| JSONPlaceholder | https://jsonplaceholder.typicode.com | Fake REST API |
| httpbin | https://httpbin.org | Test HTTP requests |
| ReqRes | https://reqres.in | Fake users API |
| Cat Facts | https://catfact.ninja | Facts về mèo |
| Pokemon API | https://pokeapi.co | Dữ liệu Pokemon |

### Ví dụ với JSONPlaceholder

```bash
# GET users
curl https://jsonplaceholder.typicode.com/users
# ==> Lấy danh sách tất cả users từ JSONPlaceholder API. API công khai này không yêu cầu xác thực, rất hữu ích để học tập và test.

# GET single user
curl https://jsonplaceholder.typicode.com/users/1
# ==> Lấy thông tin chi tiết của user có ID là 1. Cú pháp RESTful endpoint này là chuẩn mà hầu hết API hiện đại sử dụng.

# POST user
curl -X POST https://jsonplaceholder.typicode.com/users \
  -H "Content-Type: application/json" \
  # ==> Header chỉ định dữ liệu gửi ở định dạng JSON.
  -d '{"name": "Test", "email": "test@test.com"}'
  # ==> Dữ liệu JSON tạo user mới với tên "Test" và email "test@test.com". JSONPlaceholder sẽ trả lại ID được cấp cho user mới.
```

---

## **LIÊN HỆ**

*Made with ❤️ by ThanhRòm*
