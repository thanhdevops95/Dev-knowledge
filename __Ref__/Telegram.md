# Tạo bot trên Telegram (để lấy "giấy phép") và Viết code để kết nối & điều khiển bot.

Dưới đây là hướng dẫn chi tiết từng bước (step-by-step):

# Phần 1: Tạo Bot bằng BotFather trên Telegram

> **BotFather** là con bot "trùm" của Telegram, được dùng để tạo và quản lý tất cả các con bot khác.

## Tìm BotFather:

 - Mở ứng dụng Telegram trên điện thoại hoặc máy tính.

 - Tại ô tìm kiếm, nhập @BotFather (chọn kết quả có dấu tích xanh chính chủ).

 - Nhấn nút Start ở dưới cùng màn hình (hoặc gõ lệnh /start).

    Output: 
    >I can help you create and manage Telegram bots. If you're new to the Bot API, please [see the manual][https://core.telegram.org/bots].\
You can control me by sending these commands:\
\
`/newbot` - create a new bot.  <----   \
`/mybots` - edit your bots\
\
**Edit Bots**\
`/setname` - change a bot's name\
`/setdescription` - change bot description\
`/setabouttext` - change bot about info\
`/setuserpic` - change bot profile photo\
`/setcommands` - change the list of commands\
`/deletebot` - delete a bot\
\
**Bot Settings**\
`/token` - get authorization token\
`/revoke` - revoke bot access token\
`/setinline` - toggle inline mode\
`/setinlinegeo` - toggle inline location requests\
`/setinlinefeedback` - change inline feedback settings\
`/setjoingroups` - can your bot be added to groups?\
\
`/setprivacy` - toggle privacy mode in groups\
\
**Web Apps**\
`/myapps` - edit your web apps\
`/newapp` - create a new web app\
`/listapps` - get a list of your web apps\
`/editapp` - edit a web app\
`/deleteapp` - delete an existing web app\
\
**Games**\
`/mygames` - edit your games\
`/newgame` - create a new game\
`/listgames` - get a list of your games\
`/editgame` - edit a game\
`/deletegame` - delete an existing game\


## Tạo Bot mới:

 - Gõ lệnh `/newbot` và gửi cho BotFather.

 - BotFather sẽ yêu cầu bạn đặt tên hiển thị cho bot (Name). Bạn có thể đặt bất cứ tên gì bạn thích (Ví dụ: `Trợ lý của tôi`, `Thời Tiết Hôm Nay...`).

 - Tiếp theo, BotFather yêu cầu bạn tạo Username cho bot. Username này phải là duy nhất, viết liền không dấu và bắt buộc phải kết thúc bằng chữ bot (Ví dụ: `trolycuatoi_bot` hoặc `ThoiTiet123Bot`).

## Lưu lại API Token:

 - Nếu tạo username thành công, BotFather sẽ gửi cho bạn một tin nhắn chúc mừng dài._

 - Trong tin nhắn đó, hãy tìm đoạn mã (token) trông giống thế này: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`.

 - **Lưu ý cực kỳ quan trọng**: Đây là chìa khóa để điều khiển bot của bạn. **Tuyệt đối không chia sẻ mã Token này cho ai**,** nếu không họ có thể chiếm quyền điều khiển bot của bạn.

# Phần 2: Kết nối và Lập trình Bot (Sử dụng Python)
Để bot có thể đọc tin nhắn và trả lời, bạn cần viết một đoạn mã nhỏ. Phổ biến và dễ nhất cho người mới bắt đầu là dùng ngôn ngữ Python.

## Bước 1: Chuẩn bị môi trường

 - Đảm bảo máy tính của bạn đã cài đặt Python (Tải tại python.org).

 - Mở Terminal (trên Mac/Linux) hoặc Command Prompt / PowerShell (trên Windows).

 - Cài đặt thư viện pyTelegramBotAPI (một thư viện rất dễ dùng) bằng lệnh sau:

```Bash
pip install pyTelegramBotAPI
```

## Bước 2: Viết code kết nối

 - Mở một trình soạn thảo code (như VS Code, Sublime Text, hoặc Notepad).

 - Tạo một file mới tên là mybot.py và dán đoạn code sau vào:

```Python
import telebot

# 1. Điền API Token bạn vừa lấy từ BotFather vào đây
API_TOKEN = 'ĐIỀN_TOKEN_CỦA_BẠN_VÀO_ĐÂY'

# 2. Khởi tạo bot
bot = telebot.TeleBot(API_TOKEN)

# 3. Viết hàm xử lý khi người dùng gõ lệnh /start hoặc /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Bot sẽ phản hồi lại tin nhắn này
    bot.reply_to(message, "Xin chào! Mình là bot của bạn. Mình có thể nhại lại mọi thứ bạn nói!")

# 4. Viết hàm xử lý các tin nhắn văn bản bình thường (Echo bot)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Bot sẽ lấy nội dung tin nhắn của bạn và gửi lại y hệt
    bot.reply_to(message, message.text)

# 5. Lệnh để giữ cho bot luôn chạy và lắng nghe tin nhắn
print("Bot đang chạy...")
bot.polling()
```

## Bước 3: Chạy Bot

 - Lưu file mybot.py lại.

 - Mở Terminal/Command Prompt, di chuyển đến thư mục chứa file mybot.py.

 - Chạy file bằng lệnh:

```Bash
python mybot.py
```
 - Nếu thấy dòng chữ "Bot đang chạy..." hiện lên, tức là bạn đã kết nối thành công!

# Phần 3: Trải nghiệm thực tế
1. Mở lại Telegram.

2. Tìm bot của bạn bằng Username bạn đã tạo ở Phần 1 (VD: @trolycuatoi_bot).

3. Nhấn Start để bắt đầu trò chuyện.

4. Gửi một tin nhắn bất kỳ (ví dụ: "Hello bot"), bot của bạn sẽ tự động phản hồi lại "Hello bot" (vì chúng ta đã viết code dạng Echo - nhại lại tin nhắn).

# Kiến thức bổ sung về cách kết nối
Có 2 phương pháp chính để kết nối bot với Telegram:

 - Polling (như cách ở trên): Code của bạn sẽ liên tục "hỏi" server Telegram xem có tin nhắn mới nào không. Cách này rất dễ cài đặt, phù hợp để test hoặc chạy bot nhỏ trên máy tính cá nhân.

 - Webhook (Nâng cao): Bạn cung cấp cho Telegram một địa chỉ URL (của server bạn). Khi có người nhắn tin cho bot, Telegram sẽ chủ động "bắn" dữ liệu về URL đó. Cách này phản hồi nhanh hơn và tiết kiệm tài nguyên máy chủ, thường dùng khi triển khai (deploy) bot lên các server thực tế (như Heroku, AWS, VPS). Mới bắt đầu thì bạn cứ dùng Polling cho quen nhé!




Thực tế, để một con bot có thể kết nối và chạy được cơ bản (như ví dụ ở phần trước), bạn chỉ cần duy nhất API Token là đủ.

Tuy nhiên, nếu bạn muốn bot thông minh hơn, quản lý chặt chẽ hơn hoặc làm những tác vụ nâng cao (như chủ động gửi thông báo, phân quyền quản trị, thêm vào nhóm), bạn sẽ cần lấy thêm các thông tin sau:

1. Chat ID (Mã số cuộc trò chuyện)
Tại sao cần: Nếu bạn chỉ dùng tính năng "ai nhắn gì, bot trả lời nấy" (reply) thì không cần Chat ID. Nhưng nếu bạn muốn bot chủ động gửi thông báo (ví dụ: đến 8h sáng bot tự động báo thức cho bạn, hoặc báo giá coin mỗi ngày) mà không cần bạn phải nhắn trước, bot bắt buộc phải biết Chat ID của bạn hoặc của nhóm để gửi tới.

Cách lấy:

Cách 1 (Dùng bot khác): Lên Telegram tìm bot có tên `@userinfobot` hoặc `@GetIDs Bot`. Bấm Start, nó sẽ trả về cho bạn một dãy số (Ví dụ: Id: 123456789). Đó chính là Chat ID cá nhân của bạn.

Cách 2 (Lấy từ code): Trong đoạn code Python, bạn có thể thêm lệnh print(message.chat.id) vào hàm xử lý tin nhắn. Mỗi khi bạn nhắn cho bot, Terminal sẽ in ra Chat ID của bạn.

2. User ID (Mã số người dùng - Dùng để phân quyền Admin)
Tại sao cần: Mặc định, bất kỳ ai có username bot của bạn đều có thể vào chat và ra lệnh cho nó. Nếu bot của bạn có các lệnh nhạy cảm (như xoá dữ liệu, khởi động lại server), bạn phải "dạy" bot chỉ nghe lời một mình bạn.

Cách làm: Bạn lấy User ID của mình (cách lấy giống hệt Chat ID cá nhân ở trên). Sau đó trong code, bạn thêm một câu lệnh điều kiện (If/Else): "Nếu ID của người gửi tin nhắn đúng bằng ID của chủ nhân thì mới thực hiện lệnh".

3. Cấu hình hiển thị và Menu Lệnh (Lấy/Tạo từ BotFather)
Quay lại cuộc trò chuyện với @BotFather, bạn có thể cung cấp thêm thông tin để con bot trông chuyên nghiệp hơn:

Menu Commands (/setcommands): Tạo một nút Menu nhỏ góc trái màn hình (hoặc khi gõ / sẽ hiện ra danh sách lệnh gợi ý). Bạn sẽ gửi danh sách lệnh cho BotFather theo cấu trúc: tên_lệnh - Mô tả chức năng.

Avatar (/setuserpic): Đặt ảnh đại diện cho bot.

Description (/setdescription): Đoạn văn bản giới thiệu hiện ra khi người dùng lần đầu tiên mở bot (trước khi bấm Start).

About Text (/setabouttext): Đoạn chữ ngắn hiện trên profile (tiểu sử) của bot.

4. Group Privacy (Quyền đọc tin nhắn trong nhóm)
Tại sao cần: Nếu bạn định thêm bot vào một Group chat.

Mặc định, bot bị "mù" với các tin nhắn bình thường trong nhóm để bảo vệ quyền riêng tư. Nó chỉ đọc được những tin nhắn bắt đầu bằng dấu / (ví dụ /help).

Nếu bạn làm bot để lọc từ ngữ bậy bạ, hoặc đếm tin nhắn, bot cần đọc được mọi tin nhắn. Bạn phải vào @BotFather, dùng lệnh /setprivacy, chọn bot của bạn và đổi trạng thái thành DISABLE.

Tóm lại: * API Token: Chìa khóa nhà (Bắt buộc phải có để vào nhà).

Chat ID / User ID: Địa chỉ phòng cụ thể và chứng minh thư (Để biết gửi tin cho ai và ai đang ra lệnh).

Các cấu hình khác: Trang trí nội thất (Làm cho bot đẹp và dễ dùng hơn).