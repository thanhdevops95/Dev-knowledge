# 🎓 Giải quyết xung đột gộp code — Resolving Conflicts

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v2.0.0\
> **Tạo lúc:** 26/05/2026\
> **Cập nhật:** 26/05/2026\
> **Level:** Intermediate\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~20 phút\
> **Prerequisites:** [00_branching-and-merging.md](./00_branching-and-merging.md) ✅

> 🎯 *Bài học sống còn trong làm việc nhóm — Trang bị tư duy thép và kỹ thuật gỡ rối cực kỳ khoa học để giải quyết các "cuộc xung đột" (Merge Conflicts) của dòng code. Sau bài học này, bạn sẽ không bao giờ còn cảm thấy sợ hãi hay ngợp trước thông báo lỗi đỏ choét của Terminal nữa!*

---

## 🎯 Sau bài này bạn sẽ
- [ ] Hiểu rõ bản chất vì sao **Merge Conflict** xảy ra
- [ ] Thuộc làu cách đọc hiểu các ký hiệu xung đột: `<<<<<<<`, `=======`, `>>>>>>>`
- [ ] Thành thạo quy trình 4 bước giải quyết xung đột thủ công bằng tay
- [ ] Tận dụng tối đa giao diện trực quan của VS Code để gỡ Conflict siêu tốc
- [ ] Biết cách áp dụng "phép biến mất an toàn" `git merge --abort` khi bị ngợp

---

## Tình huống — Cuộc chiến ngầm của hai lập trình viên

Hãy tưởng tượng bạn và một đồng nghiệp tên Nam đang cùng làm việc trên một dự án quản lý khách sạn. Cả hai cùng được tách nhánh từ commit gốc của file `config.py` chứa cấu hình cổng kết nối (Port) của máy chủ:

```
[Commit gốc: port = 8000]
       │
       ├─── Nhánh của bạn: port = 8080 (backend chạy cổng riêng)
       │
       └─── Nhánh của Nam: port = 9000 (đổi sang cổng API)
```

Bạn hoàn thành xong trước, tự tin merge code của mình vào nhánh `main`. Nhánh `main` lúc này ghi nhận dòng code: `port = 8080`.

Chiều hôm đó, Nam cũng làm xong và gõ lệnh gộp code từ nhánh của Nam vào `main`. Ngay lập tức, màn hình Terminal của Nam hiện lên một cảnh báo màu đỏ đáng sợ:

```bash
Auto-merging config.py
CONFLICT (content): Merge conflict in config.py
Automatic merge failed; fix conflicts and then commit the result.
```

Nam hoảng hốt gọi bạn: *"Ông ơi cứu tôi! Git nó báo lỗi xung đột gì rồi, có bị mất code không ông? Tôi có nên xoá thư mục cài lại từ đầu không?!"*.

Bạn cười bình tĩnh: *"Không sao đâu bạn, đây là chuyện bình thường khi làm nhóm. Để Mr.Rom chỉ cách gỡ rối chỉ trong 1 phút!"*.

---

## 1️⃣ Tại sao Merge Conflict lại xảy ra?

Nhiều beginner nghĩ rằng Merge Conflict là một **lỗi nghiêm trọng** của Git. 

> 💡 **Sự thật cực kỳ thú vị:** Merge Conflict **không phải là lỗi**. Nó thực chất là một **tính năng bảo vệ an toàn** tối cao của Git!

Git cực kỳ thông minh trong việc tự động gộp code (Auto-merging). Nếu bạn sửa file `header.html` ở dòng số 5, đồng nghiệp Nam sửa file `footer.html` ở dòng số 50, Git sẽ tự động gộp chúng lại êm đẹp trong 1 nốt nhạc mà không cần hỏi bạn câu nào.

Tuy nhiên, khi **cả hai người cùng sửa đổi trên một dòng (hoặc các dòng sát nhau) của cùng một tệp tin**, Git sẽ bế tắc. Git không thể biết được ý định của ai là đúng đắn hơn. 
*   Nếu Git tự ý chọn cổng `8080` của bạn → Code của Nam sẽ bị mất và gãy kết nối.
*   Nếu Git tự ý chọn cổng `9000` của Nam → Code của bạn sẽ bị đè đè và lỗi.

Vì tôn trọng tuyệt đối công sức của cả hai lập trình viên, Git quyết định **dừng quá trình merge lại**, giữ nguyên hiện trường và nói: *"Tôi đã đánh dấu các chỗ đụng nhau. Hai bạn hãy ngồi lại thảo luận xem nên giữ dòng code của ai, rồi báo lại cho tôi biết nhé!"*.

---

## 2️⃣ Giải mã ký tự Conflict — "Mật thư" của Git

Khi cuộc xung đột xảy ra, Git sẽ viết trực tiếp các ký tự đánh dấu xung đột (Conflict Markers) vào bên trong tệp tin bị ảnh hưởng. Nếu bạn mở file `config.py` bằng một editor thông thường, bạn sẽ thấy nó có cấu trúc như sau:

```python
<<<<<<< HEAD
port = 8080
=======
port = 9000
>>>>>>> feature/api-port
```

Hãy cùng Mr.Rom giải mã 3 thành phần mật thư này:

| Ký tự | Ý nghĩa kỹ thuật | Ẩn dụ thực tế |
|---|---|---|
| **`<<<<<<< HEAD`** | Bắt đầu vùng code của **nhánh hiện tại** bạn đang đứng (nhánh nhận merge, ví dụ `main`). | *"Đây là dòng code ĐANG CÓ SẴN trong nhà bạn."* |
| **`=======`** | Đường ranh giới ngăn cách. Tuyệt đối không có code ở dòng này. | *"Ranh giới chia đôi hai chiến tuyến."* |
| **`>>>>>>> feature/api-port`** | Kết thúc vùng code của **nhánh nguồn đang được gộp vào** (nhánh gửi merge). | *"Đây là dòng code MỚI đang gõ cửa xin vào nhà bạn."* |

---

## 3️⃣ Quy trình 4 bước giải quyết xung đột thủ công

Khi gặp conflict, hãy hít một hơi thật sâu, giữ cái đầu lạnh và thực hiện đúng 4 bước chuẩn mực sau:

### 🚶 Bước 3.1: Định vị tệp tin bị xung đột
Gõ lệnh thần chú để tìm xem những tệp nào đang bị kẹt chưa merge được:
```bash
git status
```
Output thực tế hiển thị:
```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   config.py
```
*   **Giải thích output:** Mục màu đỏ `both modified: config.py` chỉ danh chính xác file `config.py` là nạn nhân của cuộc xung đột này.

---

### 🤝 Bước 3.2: Thảo luận và Đưa ra quyết định
Hãy quay sang Nam (hoặc nhắn tin qua Slack/Discord) để thống nhất giải pháp. Có 3 kịch bản giải quyết:
*   **Kịch bản A (Chấp nhận Local):** Giữ lại cổng `8080` của bạn, loại bỏ cổng `9000` của Nam.
*   **Kịch bản B (Chấp nhận Incoming):** Nhường Nam, giữ lại cổng `9000` của Nam, loại bỏ cổng `8080` của bạn.
*   **Kịch bản C (Kết hợp cả hai):** Nhận diện dự án cần chạy song song cả hai cấu hình, viết lại thành cấu hình linh hoạt chứa cả hai cổng.

---

### ✏️ Bước 3.3: Sửa đổi tệp tin trực tiếp
Mở file `config.py` lên bằng editor (ví dụ: VS Code). Hãy xóa hoàn toàn các dòng chứa ký tự marker (`<<<<<<<`, `=======`, `>>>>>>>`) đi.

Giả sử bạn quyết định chọn **Kịch bản A (Giữ cổng 8080 của bạn)**, bạn phải edit nội dung tệp tin trở nên sạch sẽ như thế này:
```python
port = 8080
```
*(Tuyệt đối không để sót bất kỳ dấu `=` hay `<` nào của Git, vì nếu để sót, chúng sẽ trở thành lỗi cú pháp khiến chương trình không chạy được!)*

---

### 💾 Bước 3.4: Đóng gói và Hoàn tất quá trình Merge
Sau khi đã lau dọn hiện trường sạch sẽ, bạn báo cho Git biết bạn đã giải quyết xong xung đột bằng cách đưa file vào Staging:

```bash
git add config.py
```

Hãy gõ `git status` để xem trạng thái mới nhất:
```bash
git status
```
Output thực tế hiển thị:
```
On branch main
All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)
```
*   **Giải thích output:** Dòng chữ màu xanh `All conflicts fixed but you are still merging` khẳng định bạn đã gỡ rối thành công! Giờ chỉ cần chạy lệnh commit để Git ghi nhận sự hòa giải.

Tạo commit gộp (Merge Commit):
```bash
git commit -m "merge: resolve port conflict, accept port 8080"
```
Output thực tế:
```
[main a2b3c4d] merge: resolve port conflict, accept port 8080
```
Xong! Bạn đã trở thành người hùng giải cứu code của team! 🚀

---

## 🎨 Tuyệt kỹ giải quyết xung đột bằng giao diện VS Code

Nếu bạn cảm thấy việc xóa các dòng ký hiệu `<<<<<<<` thủ công bằng tay quá mất thời gian và dễ nhầm lẫn, hãy mở thư mục dự án bằng **VS Code**. 

VS Code tích hợp sẵn một bộ công cụ trực quan (Merge Editor) cực kỳ thông minh. Khi bạn click vào file bị conflict, bạn sẽ thấy 4 nút bấm nhỏ hiển thị ngay trên đầu các dòng xung đột:

```
[Accept Current Change] | [Accept Incoming Change] | [Accept Both Changes] | [Compare Changes]
<<<<<<< HEAD
port = 8080
...
```

*   **Accept Current Change:** Tự động xóa mọi thứ khác, chỉ giữ lại code của bạn ở nhánh hiện tại (HEAD).
*   **Accept Incoming Change:** Tự động giữ lại code của nhánh đang được merge vào.
*   **Accept Both Changes:** Giữ lại cả hai dòng code của hai người.

> 💡 **Khuyên dùng:** Chỉ cần click đúng 1 click chuột vào lựa chọn mong muốn → VS Code tự động dọn sạch mọi ký tự rác giúp bạn trong 0.5 giây!

---

## 🛡️ Phép rút lui an toàn — Tránh hoảng loạn khi ngợp

Đôi khi, bạn merge một nhánh quá lớn chứa hàng chục file xung đột phức tạp đè lên nhau. Màn hình Terminal hiện đỏ lòm, code của bạn bị rối tung và bạn cảm thấy hoàn toàn mất kiểm soát.

> ⚠️ **Lời khuyên vàng của Mr.Rom:** Tuyệt đối không được hoảng sợ gõ bừa bãi các lệnh reset hay xóa file. Hãy sử dụng câu thần chú quay ngược thời gian:

```bash
git merge --abort
```

Output thực tế:
*(Terminal lập tức trở về trạng thái sạch sẽ bình thường trước khi merge)*
*   **Giải thích:** Lệnh `--abort` giống như một nút **"Hủy thao tác gộp code"**. Nó sẽ xóa toàn bộ hiện trường xung đột, đưa dự án của bạn quay trở lại trạng thái an toàn tuyệt đối trước thời điểm bạn gõ lệnh merge. Bạn có thể thư giãn đầu óc, uống một ngụm trà và bàn bạc kỹ lại với team trước khi thực hiện merge lần thứ hai.

---

## 🧠 Câu hỏi ôn tập (Self-check)

**Q1: Có thể xảy ra Merge Conflict khi tôi chỉ làm việc một mình (Solo Developer) không?**
<details>
<summary>💡 Xem giải thích</summary>

**Có.** Conflict xảy ra khi có 2 nhánh thay đổi cùng 1 dòng code. Dù bạn làm một mình, nếu bạn tạo nhánh `feature-A` sửa dòng số 5 của file `README.md`, sau đó bạn quay lại `main` cũng sửa dòng số 5 của file `README.md` đó, khi bạn merge `feature-A` vào `main`, Git vẫn báo Merge Conflict bình thường vì Git không tự ý biết bạn muốn giữ bản sửa đổi nào!

</details>

**Q2: Tại sao sau khi gỡ hết các ký hiệu conflict, tôi chạy `git commit` mà không cần thêm tham số `-m` Git vẫn tự động tạo tin nhắn commit?**
<details>
<summary>💡 Xem giải thích</summary>

Khi bạn đang ở giữa quá trình merge bị conflict và chạy lệnh `git commit` (sau khi đã `git add` để sửa lỗi), Git tự động nhận biết đây là một Merge Commit. Git sẽ tự động tạo sẵn một tin nhắn mặc định dạng `"Merge branch 'tên-nhánh' into main"`. Bạn chỉ cần lưu lại file editor mở ra là xong.

</details>

---

## 📚 Glossary

| Thuật ngữ | Ý nghĩa kỹ thuật | Ẩn dụ thực tế |
|---|---|---|
| **Merge Conflict** | Sự xung đột xảy ra khi hai thay đổi đụng nhau trên cùng một dòng code. | Hai người cùng ghi đè chữ lên một dòng của cuốn sổ tay. |
| **Conflict Markers** | Các ký tự đặc biệt (`<<<<<<<`, `=======`, `>>>>>>>`) dùng để khoanh vùng chỗ xung đột. | Biển báo ranh giới tranh chấp đất đai. |
| **`HEAD` (in conflict)** | Nhánh hiện tại bạn đang đứng nhận gộp code. | *"Đất nhà mình đang đứng."* |
| **`git merge --abort`** | Hủy bỏ hoàn toàn quá trình merge đang bị xung đột để quay về an toàn. | Nút rút quân khẩn cấp của đại tướng. |

---

## 🔗 Liên kết & Tài nguyên

### Bài học & Bài tập liên quan

| Hướng đi | Bài học / Thử thách |
|---|---|
| ⬅️ Bài trước | [00_branching-and-merging.md](./00_branching-and-merging.md) — Phân nhánh & Gộp nhánh cơ bản |
| ➡️ Bài tiếp | [02_collaborative-workflows.md](./02_collaborative-workflows.md) — Quy trình làm việc nhóm chuyên nghiệp |
| 🧪 Thử thách Labs | [lab_conflict-hero.md](../../exercises/02_intermediate/lab_conflict-hero.md) — Thực hành tự tay giải quyết Merge Conflict |
| 🧠 Trắc nghiệm | [quiz_branching-and-conflicts.md](../../exercises/02_intermediate/quiz_branching-and-conflicts.md) — Đào sâu tư duy phân nhánh |

---

## 📌 Changelog
- **v2.0.0 (26/05/2026)** — Mr.Rom biên soạn hoàn chỉnh bài học trung cấp về Merge Conflict, hướng dẫn giải mã mật thư Git, các bước resolve thủ công/VS Code và cơ chế rút lui an toàn theo chuẩn Blueprint v0.2.0.
